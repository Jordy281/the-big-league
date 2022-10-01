"""
This is the people module and supports all the REST actions for the
accounts data
"""
from api.app import db
from api.auth import loggedIn
from api.models import LinkedAccountSchema, InputLinkedAccountSchema

from flask import make_response, Blueprint, abort, request
from apifairy import body, response, other_responses

import logging
logging.basicConfig(level=logging.DEBUG)

import requests

linked_accounts = Blueprint('linked_accounts', __name__)


@linked_accounts.route('/linkedaccounts', methods=['GET'])
@loggedIn
@response(LinkedAccountSchema(many=True))
def all():
    """Retrieve all Linked Accounts"""
    """
    This function responds to a request for /api/linkedaccounts
    with the complete lists of people
    :return:        json string of list of people
    """
    docs = db.collection(u'LinkedAccounts').stream()
    all_leagues = []
    for league in [doc.to_dict() for doc in docs]:
        all_leagues.append(league)
    print(all_leagues)
    return all_leagues


# TODO: We may want to change the /<league_id> to something less strict like ?league_id=<account_id>
@linked_accounts.route('/linkedaccounts/<int:account_id>', methods=['GET'])
@loggedIn
@response(LinkedAccountSchema())
@other_responses({404: 'Linked Account not found'})
def get_http(account_id):
    """Retrieve a Linked Account by ID"""
    """
    This function responds to a request for /api/linkedaccounts/{league_id}
    with one matching league from leagues
    :param account_id:   Id of account to find
    :return:            league matching id
    """
    status_code, data, message = get(account_id)
    if status_code !=200:
        abort(status_code, message)
    return data

def get(account_id):
    # Get the partner requested
    # Get all user accounts where id is in users
    user = request.user
    print(f"User: {user}")
    #doc_ref = db.collection(u'leagues').where(user['id'],'in','users').document(league_id)
    doc_ref = db.collection(u'LinkedLeagues').document(account_id)
    doc = doc_ref.get()
    if not doc.exists:
        return 404, None, f"Linked Account with ID {account_id} does not exist"
    return 200, doc, "Linked Account returned success"

@loggedIn
@linked_accounts.route('/linkedaccounts', methods=['POST'])
@body(InputLinkedAccountSchema())
@response(LinkedAccountSchema(), 201)
@other_responses({400: f"Linked account add failed"})
def create_http(account):
    """Create New Linked Account"""
    """
    This function creates a new account in the accounts structure
    based on the passed in account data
    :param account:  account to create in people structure
    :return:        201 on success, 409 on account exists
    """
    user_id = request.user.id
    message, status_code = create(account, user_id)
    if status_code !=200 or status_code!=200:
        abort(400, message)
    return message, status_code

def create(account, owner_id = None):
    logging.info(f"Creating Linked Account: {account['host']}-{account['linked_account_id']}")
    logging.debug(account)
    logging.info(f"Checking if Linked Account already exists: {account['linked_account_id']}")
    # Check if ID already exists
    doc_ref = db.collection(u'LinkedAccounts').document(account['linked_account_id'])
    doc = doc_ref.get()
    
    if doc.exists:
        return 400, None, f"Unable to add linked account {account['linked_account_id']}, as it is already linked to another League"
    
    # Import Linked League:
    if account.get("host").lower() == "sleeper":
        # Get league details from Sleeper
        # curl "https://api.sleeper.app/v1/user/<user_id>"
        response = requests.get(f"https://api.sleeper.app/v1/league/{account['linked_account_id']}")
        data = response.json()
        
        username = data['username']
        display_name = data['display_name']
        linked_account_id = account['linked_account_id']
        host = account['host'].lower()
        avatar = data['avatar']

        data = {
            'host': host,
            'linked_account_id': linked_account_id,
            'display_name': display_name,
            'username': username,
            'avatar': avatar,
            'user_id': owner_id
        }
        db.collection(u'LinkedLeagues').document(account['linked_account_id']).set(data)
    return 201, db.collection(u'LinkedLeagues').document(account['linked_account_id']), "Linked League Addedd Successfully"

@loggedIn
@linked_accounts.route('/linkedaccounts/<int:account_id>', methods=['PUT'])
@response(LinkedAccountSchema())
@body(LinkedAccountSchema())
@other_responses({404: "Linked Account not found", 409: f"Linked Account name exists already"})
def update(account, account_id):
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
    logging.info(f"Updating Linked Account: {account['host']}-{account['linked_account_id']}")
    logging.debug(account)
    logging.info(f"Checking if Linked Account already exists: {account['linked_account_id']}")
    # Check if ID already exists
    doc_ref = db.collection(u'LinkedAccounts').document(account['linked_account_id'])
    doc = doc_ref.get()
    
    if not doc.exists:
        return abort(404, f"Unable to update linked account {account['linked_account_id']}")
    
    # Import Linked League:
    if account.get("host").lower() == "sleeper":
        # Get league details from Sleeper
        # curl "https://api.sleeper.app/v1/user/<user_id>"
        response = requests.get(f"https://api.sleeper.app/v1/league/{account['linked_account_id']}")
        data = response.json()
        
        username = data['username']
        display_name = data['display_name']
        linked_account_id = account['linked_account_id']
        host = account['host'].lower()
        avatar = data['avatar']
        owner_id = account['user_id']

        data = {
            'host': host,
            'linked_account_id': linked_account_id,
            'display_name': display_name,
            'username': username,
            'avatar': avatar,
            'user_id': owner_id
        }
        ref = db.collection(u'LinkedAccounts').document(account['linked_account_id'])

        # Set the capital field
        new_linked_account = ref.update(data)

    return new_linked_account


@loggedIn
@linked_accounts.route('/linkedaccounts/<int:account_id>', methods=['DELETE'])
@other_responses({404: "Linked Account not found"})
def delete_http(account_id):
    """Delete CM360 Account"""
    """
    This function deletes a account from the people structure
    :param account_id:   Id of the account to delete
    :return:            200 on successful delete, 404 if not found
    """
    status_code, message = delete(account_id=account_id)
    if status_code !=200:
        abort(status_code, message)
    return message, status_code

def delete(account_id=None):
    """Delete CM360 Account"""
    """
    This function can be called from either:
    - delete_http (above)
    - delete (partners.py)
    """
    status, ref, message = get(account_id)

    # Did we find a partner?
    if status == 200:
        db.collection(u'LinkedAccounts').document(account_id).delete()
        return 200, "League Deleted"
    # Otherwise, nope, didn't find that partner
    else:
        abort(404, f"League id {account_id} not found")