"""
This is the people module and supports all the REST actions for the
accounts data
"""
from api.app import db
from flask import make_response, Blueprint, abort
from flask_cors import cross_origin, CORS


#from config import db
from api.models import Partner, CmAccount, CmAccountSchema
from apifairy import body, response, other_responses
from api.auth import loggedIn

from api.mongo_db import get_rate, create_rate, update_rate, delete_rate

import logging

cm_accounts = Blueprint('cm_accounts', __name__)
account_schema = CmAccountSchema()
accounts_schema = CmAccountSchema(many=True)

@cm_accounts.route('/cmaccounts', methods=['GET'])
@loggedIn
@response(accounts_schema)
def all():
    """Retrieve all Cm Accounts"""
    """
    This function responds to a request for /api/cmaccounts
    with the complete lists of people
    :return:        json string of list of people
    """
    #print(request)
    # Create the list of people from our data
    return CmAccount.query.order_by(CmAccount.partner_id).all()


# TODO: We may want to change the /<account_id> to something less strict like ?account_id=<account_id>
@cm_accounts.route('/cmaccounts/<int:account_id>', methods=['GET'])
@loggedIn
@response(account_schema)
@other_responses({404: 'CM Account not found'})
def get(account_id):
    """Retrieve a CM Account by ID"""
    """
    This function responds to a request for /api/cmaccounts/{account_id}
    with one matching CM360 account from the table cm_account
    :param account_id:   Id of CM360 account to find
    :return:            CM360 
    account matching id
    """
    # Get the account requested
    account = CmAccount.query.filter(CmAccount.account_id == account_id).one_or_none()

    # Did we find a account?
    if account is not None:
        #Getting Rates
        rates = get_rate('CM360', account_id=account.account_id)
        if len(rates) > 0:
            account.rates = rates[0]['rates']
        else:
            account.rates = []
        # For each rate
        for rate in account.rates:
            # For each field in rate
            for rate_key in rate:
                if rate[rate_key] is None:
                    rate[rate_key] = ''

        # Serialize the data for the response
        return account

    # Otherwise, nope, didn't find that account
    else:
        abort(404)

@loggedIn
@cm_accounts.route('/cmaccounts', methods=['POST'])
@body(account_schema)
@response(account_schema, 201)
@other_responses({400: f"CM account add failed"})
def create_http(account):
    """Create New CM Account"""
    """
    This function creates a new account in the accounts structure
    based on the passed in account data
    :param account:  account to create in people structure
    :return:        201 on success, 409 on account exists
    """
    message, status_code = create(account)
    if status_code !=200 or status_code!=200:
        abort(400, message)
    return message, status_code

def create(account):
    platform_name = account.get("platform_name")
    partner_id = account.get('partner_id')
    partner = db.session.get(Partner, partner_id) or abort(404)

    logging.info(f"Creating CM Account: {account['platform_name']}")

    existing_account = (
        CmAccount.query.filter(CmAccount.platform_name == platform_name)
        .one_or_none()
    )

    # Can we insert this account?
    if existing_account is None:
        rates = None
        if 'rates' in account:
            rates = account['rates']
            del account['rates']

        # Create a account instance using the schema and the passed in account
        schema = CmAccountSchema()
        new_account = CmAccount(**account)
        # Add the account to the database
        partner.cm_accounts.append(new_account)
        db.session.add(partner)
        db.session.commit()
        
        acc = partner.cm_accounts[-1]
        if rates != None:
            data = {
                "account_id": int(acc.account_id),
                "partner_id": int(acc.partner_id),
                "platform_id": int(acc.platform_id),
                "rates": rates
            }
            if 'platform_subaccount_id' in account:
                data['platform_subaccount_id'] = int(account.platform_subaccount_id)
            create_rate('CM360', data)

        # Serialize and return the newly created account in the response
        return schema.dump(new_account), 201

    # Otherwise, nope, account exists already
    else:
        logging.error(f"CM account ID already exists - {existing_account}")
        return "CM account name already exists", 400

@loggedIn
@cm_accounts.route('/cmaccounts/<int:account_id>', methods=['PUT'])
@response(CmAccountSchema())
@body(CmAccountSchema())
@other_responses({404: "CM Account not found", 409: f"CM Account name exists already"})
def update(data, account_id):
    """Update CM Account"""
    """
    This function updates an existing cm_account in the people structure
    Throws an error if a cm_account with the name we want to update to
    already exists in the database.
    :param account_id:   Id of the cm_account to update in the people structure
    :param account:      account to update
    :return:            updated account structure
    """
    # Get the account requested from the db into session
    platform_id = data.get('platform_id')
    platform_name = data.get('platform_name')
    account = db.session.get(CmAccount, account_id) or abort(404)

    # Try to find an existing account with the same name as the update
    existing_account = (
        CmAccount.query.filter(CmAccount.platform_id == platform_id)
        .one_or_none()
    )

    # Would our update create a duplicate of another account already existing?
    if (
        existing_account is not None and 
        existing_account.platform_name == platform_name and
        existing_account.account_id != account_id
    ):
        abort(409)
        

    # Otherwise go ahead and update!
    # Otherwise go ahead and update!
    account.update(data)
    if account.platform_subaccount_id: 
        logging.debug(account.platform_subaccount_id)
        data['platform_subaccount_id'] = int(account.platform_subaccount_id)
        update_rate('CM360', data, subaccount_id=int(account.platform_subaccount_id))
    update_rate('CM360', data, account_id=int(account.account_id))
    db.session.commit()

    return account

@loggedIn
@cm_accounts.route('/cmaccounts/<int:account_id>', methods=['DELETE'])
@other_responses({404: "CM360 Account not found"})
def delete_http(account_id):
    """Delete CM360 Account"""
    """
    This function deletes a account from the people structure
    :param account_id:   Id of the account to delete
    :return:            200 on successful delete, 404 if not found
    """
    message,status_code = delete(account_id=account_id)
    if status_code !=200 or status_code!=200:
        abort(status_code, message)
    return message, status_code

def delete(account_id=None, partner_id=None):
    """Delete CM360 Account"""
    """
    This function can be called from either:
    - delete_http (above)
    - delete (partners.py)
    """
    # Get the account requested
    accounts=None

    if account_id is not None:
        accounts = CmAccount.query.filter(CmAccount.account_id == account_id).one_or_none()
        if accounts is None:
            return f"No CM account found with ID {account_id}", 404
        accounts = [accounts]
    
    elif partner_id is not None:
        accounts = CmAccount.query.filter(CmAccount.partner_id == partner_id).all()
        if accounts is None:
            return f"No CM accounts to delete for partner {partner_id}", 200
    
    logging.debug(accounts)
    for account in accounts:
        db.session.delete(account)
        delete_rate('CM360', account_id=int(account.account_id))
        db.session.commit()
    return "CM accounts deleted", 200