"""
This is the people module and supports all the REST actions for the
accounts data
"""
from api.app import db
from api.auth import loggedIn
from api.models import LinkedLeagueSchema
import api.linkedAccounts


from flask import make_response, Blueprint, abort, request
from apifairy import authenticate, body, response, other_responses

import requests

import logging
logging.basicConfig(level=logging.DEBUG)

linked_leagues = Blueprint('linked_leagues', __name__)

@linked_leagues.route('/linkedleagues', methods=['GET'])
@loggedIn
@response(LinkedLeagueSchema(many=True))
def all():
    """Retrieve all Linked Leagues"""
    """
    This function responds to a request for /api/linkedleague
    with the complete lists of people
    :return:        json string of list of people
    """
    docs = db.collection(u'LinkedLeagues').stream()
    all_leagues = []
    for league in [doc.to_dict() for doc in docs]:
        all_leagues.append(league)
    print(all_leagues)
    return all_leagues



# TODO: We may want to change the /<account_id> to something less strict like ?account_id=<account_id>
@linked_leagues.route('/linkedleagues/<int:league_id>', methods=['GET'])
@loggedIn
@response(LinkedLeagueSchema())
@other_responses({404: 'DV Account not found'})
def get_http(league_id):
    """Create New Linked League"""
    """
    This function creates a new account in the accounts structure
    based on the passed in account data
    :param account:  account to create in people structure
    :return:        201 on success, 409 on account exists
    """
    status_code, data, message = create(league_id)
    if status_code !=200 or status_code!=201:
        abort(status_code, message)
    return status_code, data, message

def get(league_id):
    """Retrieve a Linked League by ID"""
    """
    This function responds to a request for /api/linkedleagues/{league_id}
    with one matching league from leagues
    :param league_id:   Id of league to find
    :return:            league matching id
    """
    # Get the partner requested
    # Get all user accounts where id is in users
    user = request.user
    print(f"User: {user}")
    #doc_ref = db.collection(u'leagues').where(user['id'],'in','users').document(league_id)
    doc_ref = db.collection(u'LinkedLeagues').document(league_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
        return doc.to_dict()
    else:
        print(u'No such document!')
        abort(404)
    
@loggedIn
@linked_leagues.route('/linkedleague', methods=['POST'])
#@body(DvAccountSchema())
#@response(DvAccountSchema(), 201)
@other_responses({400: f"Linked League add failed"})
def create_http(linked_league):
    """Create New Linked League"""
    """
    This function creates a new account in the accounts structure
    based on the passed in account data
    :param account:  account to create in people structure
    :return:        201 on success, 409 on account exists
    """
    status_code, data, message = create(linked_league)
    if status_code!=201:
        abort(status_code, message)
    return status_code, data, message

def create(linked_league):
    """
    This function creates a new account in the accounts structure
    based on the passed in account data 
    :param linked league: object containing host and league id looking like
    {
        host: "Sleeper",
        league_id: "21341324134"
    }
    """
    logging.info(f"Creating Linked League: {linked_league['host']}-{linked_league['league_id']}")
    logging.debug(linked_league)
    logging.info(f"Checking if Linked League already exists: {linked_league['league_id']}")
    
    # Check if ID already exists
    doc_ref = db.collection(u'LinkedLeagues').document(linked_league['league_id'])
    doc = doc_ref.get()
    
    if doc.exists:
        return 400, None, f"Unable to add linked league {linked_league['league_id']}, as it is already linked to another League"
    
    # Import Linked League:
    if linked_league.get("host").lower() == "sleeper":
        # Get league details from Sleeper
        # curl "https://api.sleeper.app/v1/league/<league_id>"
        response = requests.get(f"https://api.sleeper.app/v1/league/{linked_league['league_id']}")
        data = response.json()
        name = data['name']
        host = linked_league['host'].lower()
        avatar = data['avatar']
        league_id = linked_league['league_id']

        # For each member in the league
        # curl "https://api.sleeper.app/v1/league/<league_id>/users"
        league_members=[]
        response = requests.get(f"https://api.sleeper.app/v1/league/{linked_league['league_id']}/users")
        league_members = response.json()
        linked_account_references = []
        for user in league_members:
            # is member in Linked accounts?
            doc_ref = db.collection(u'LinkedAccounts').document(user['user_id'])
            doc = doc_ref.get()
            
            if not doc.exists:
                status, doc_ref, message = api.linkedAccounts.create()
                if status != 201:
                    #TODO: Undo any Linked accounts that were added
                    return status, None, message

            linked_account_references.append({user['user_id']:doc_ref})
        data = {
            'name': data['name'],
            'host': linked_league['host'].lower(),
            'avatar': data['avatar'],
            'league_id': linked_league['league_id'],
            'members': linked_account_references,
        }
        db.collection(u'LinkedLeagues').document(linked_league['league_id']).set(data)
        document_reference = db.collection(u'LinkedLeagues').document(linked_league['league_id'])
    return 201, document_reference, "Linked League Addedd Successfully"

@loggedIn
@linked_leagues.route('/linked_league/<int:league_id>', methods=['PUT'])
@body(LinkedLeagueSchema())
@response(LinkedLeagueSchema())
@other_responses({404: "Linked League not found", 409: f"Linked League Update Failed"})
def update(league, league_id):
    """Update DV Account"""
    """
    This function updates an existing dv_account in the people structure
    Throws an error if a dv_account with the name we want to update to
    already exists in the database.
    :param account_id:   Id of the dv_account to update in the people structure
    :param account:      account to update
    :return:            updated account structure
    """
    ref = db.collection(u'Leagues').document(league_id)

    # Set the capital field
    ref.update(league)
    
    status, new_league_ref, message  = get(league_id)
    if status == 200:
        return new_league_ref.get()
    abort(400, "League could not be retrieved after updating")

@loggedIn
@linked_leagues.route('/linked_league/<int:league_id>', methods=['DELETE'])
@other_responses({404: "Linked League not found"})
def delete_http(league_id):
    """Delete DV360 Account"""
    """
    This function deletes a account from the people structure
    :param league_id:   Id of the account to delete
    :return:            200 on successful delete, 404 if not found
    """
    message,status_code = delete(league_id)
    if status_code !=200 or status_code!=200:
        abort(status_code, message)
    return message, status_code

def delete(league_id=None):
    # Get the account requested
    # Get the partner requested
    status, ref, message = get(league_id)

    # Did we find a partner?
    if status == 200:
        db.collection(u'Leagues').document(league_id).delete()
        return 200, "League Deleted"
    # Otherwise, nope, didn't find that partner
    else:
        abort(404, f"League id {league_id} not found")