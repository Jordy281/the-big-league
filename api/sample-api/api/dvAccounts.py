"""
This is the people module and supports all the REST actions for the
accounts data
"""
from api.app import db
from flask import make_response, Blueprint, abort
from flask_cors import cross_origin, CORS

#from config import db
from api.models import Partner, DvAccount, DvAccountSchema
from apifairy import authenticate, body, response, other_responses
from api.auth import loggedIn

from api.mongo_db import get_rate, create_rate, update_rate, delete_rate

import logging
logging.basicConfig(level=logging.INFO)

dv_accounts = Blueprint('dv_accounts', __name__)

@dv_accounts.route('/dvaccounts', methods=['GET'])
@loggedIn
@response(DvAccountSchema(many=True))
def all():
    """Retrieve all Dv Accounts"""
    """
    This function responds to a request for /api/dvaccounts
    with the complete lists of people
    :return:        json string of list of people
    """
    # logging.debug(request)
    # Create the list of people from our data
    return DvAccount.query.order_by(DvAccount.partner_id).all()


# TODO: We may want to change the /<account_id> to something less strict like ?account_id=<account_id>
@dv_accounts.route('/dvaccounts/<int:account_id>', methods=['GET'])
@loggedIn
@response(DvAccountSchema())
@other_responses({404: 'DV Account not found'})
def get(account_id):
    """Retrieve a DV Account by ID"""
    """
    This function responds to a request for /api/dvaccounts/{account_id}
    with one matching DV360 account from the table dv_account
    :param account_id:   Id of DV360 account to find
    :return:            DV360 
    account matching id
    """
    # Get the account requested
    account = DvAccount.query.filter(DvAccount.account_id == account_id).one_or_none()

    # Did we find a account?
    if account is not None:

        # Get the Rate:
        #Getting Rates
        rates = get_rate('DV360', account_id=account.account_id)
        if len(rates) > 0:
            # Example of rates item
            # rates[0] = {
            #   '_id': '628e7159f9873fa096d6ee7b', 
            #   'account_id': 3, 
            #   'partner_id': 1,
            #   'platform_id': 3, 
            #   'platform_name': 'Dandelion-DV-Test-Update'
            # }
            if 'rates' in rates[0]:
                account.rates = rates[0]['rates']
            else:
                account.rates = []
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
        abort(404, f"Dv account ID {account_id} does not exist")

@loggedIn
@dv_accounts.route('/dvaccounts', methods=['POST'])
@body(DvAccountSchema())
@response(DvAccountSchema(), 201)
@other_responses({400: f"DV Account add failed"})
def create_http(account):
    """Create New DV Account"""
    """
    This function creates a new account in the accounts structure
    based on the passed in account data
    :param account:  account to create in people structure
    :return:        201 on success, 409 on account exists
    """
    message, status_code = create(account)
    if status_code !=200 or status_code!=200:
        abort(status_code, message)
    return message, status_code

def create(account):
    logging.info(f"Creating DV Account: {account['platform_name']}")
    logging.debug(account)
    platform_name = account.get("platform_name")
    logging.info(f"Checking if DV Account already exists: {account['platform_name']}")
    partner_id = account.get('partner_id')
    partner = db.session.get(Partner, partner_id)
    existing_account = (
        DvAccount.query.filter(DvAccount.platform_name == platform_name)
        .one_or_none()
    )
    logging.debug("Does account exist?")
    # Can we insert this account?
    if existing_account is None:
        logging.info(f"Account {account['platform_name']} does not exist")
        rates = None
        if 'rates' in account:
            rates = account['rates']
            del account['rates']

        # Create a account instance using the schema and the passed in account
        logging.debug("Rates: deleted")
        logging.debug("Inserting DV Account")
        schema = DvAccountSchema()
        logging.debug("Schema found")
        new_account = DvAccount(**account)
        logging.debug("acc made")
        # Add the account to the database
        partner.dv_accounts.append(new_account)
        logging.debug("new account appended")
        db.session.add(partner)
        logging.debug("account added to partner")
        db.session.commit()
        logging.debug("partner committed")
        #db.session.add(new_account)
        
        acc = partner.dv_accounts[-1]
        logging.debug("Get new object commited from sql")
        if rates != None:
            logging.debug("show rates")
            data = {
                "account_id": int(acc.account_id),
                "partner_id": int(acc.partner_id),
                "platform_id": int(acc.platform_id),
                "rates": rates
            }
            if 'platform_subaccount_id' in account:
                data['platform_subaccount_id'] = int(account.platform_subaccount_id)
            create_rate('DV360', data)

        # Serialize and return the newly created account in the response
        return schema.dump(new_account), 201

    # Otherwise, nope, account exists already
    else:
        logging.error(f"DV account name already exists - {existing_account}")
        return "DV account name already exists", 400

@loggedIn
@dv_accounts.route('/dvaccounts/<int:account_id>', methods=['PUT'])
@body(DvAccountSchema())
@response(DvAccountSchema())
@other_responses({404: "DV Account not found", 409: f"DV Account name exists already"})
def update(data, account_id):
    """Update DV Account"""
    """
    This function updates an existing dv_account in the people structure
    Throws an error if a dv_account with the name we want to update to
    already exists in the database.
    :param account_id:   Id of the dv_account to update in the people structure
    :param account:      account to update
    :return:            updated account structure
    """
    # Get the account requested from the db into session
    platform_id = data.get('platform_id')
    platform_name = data.get('platform_name')
    account = db.session.get(DvAccount, account_id) or abort(404, f"DV account id {account_id} does not exist")

    # Try to find an existing account with the same name as the update
    existing_account = (
        DvAccount.query.filter(DvAccount.platform_id == platform_id)
        .one_or_none()
    )

    # Would our update create a duplicate of another account already existing?
    if (
        existing_account is not None and 
        existing_account.platform_name == platform_name and
        existing_account.account_id != account_id
    ):
        abort(400, f"DV Account Update Failed - DV platform name already exists")
        

    # Otherwise go ahead and update!
    # Otherwise go ahead and update!
    account.update(data)
    if account.platform_subaccount_id: 
        logging.debug(account.platform_subaccount_id)
        data['platform_subaccount_id'] = int(account.platform_subaccount_id)
        update_rate('DV360', data, subaccount_id=int(account.platform_subaccount_id))
    update_rate('DV360', data, account_id=int(account.account_id))
    db.session.commit()

    return account

@loggedIn
@dv_accounts.route('/dvaccounts/<int:account_id>', methods=['DELETE'])
@other_responses({404: "DV360 Account not found"})
def delete_http(account_id):
    """Delete DV360 Account"""
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
    # Get the account requested
    accounts=None
    if account_id is not None:
        accounts = DvAccount.query.filter(DvAccount.account_id == account_id).one_or_none()
        if accounts is None:
            return f"No DV account found with ID {account_id}", 404
        
        accounts = [accounts]

    elif partner_id is not None:
        accounts = DvAccount.query.filter(DvAccount.partner_id == partner_id).all()
        if accounts is None:
            return f"No DV accounts to delete for partner {partner_id}", 200

    logging.debug(accounts)
    for account in accounts:
        delete_rate('DV360', account_id=int(account.account_id))
        db.session.delete(account)
        db.session.commit()
    return "DV accounts deleted", 200