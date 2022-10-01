"""
This is the people module and supports all the REST actions for the
partners data
"""
from api.app import db
from api.auth import loggedIn
import api.linkedLeagues as linkedLeagues
from api.models import LeagueSchema

from flask import make_response, Blueprint, abort, request, jsonify, Response
from apifairy import authenticate, body, response, other_responses, arguments

from urllib import request

import logging
logging.basicConfig(level=logging.DEBUG)


leagues = Blueprint('leagues', __name__)

@leagues.route('/leagues', methods=['GET'])
@loggedIn
@response(LeagueSchema(many=True))
def all():
    """Retrieve All Leagues"""
    """
    This function responds to a request for /api/leagues
    with the complete lists of leagues the user has access to
    :return:        json string of list of leagues
    """
    # Create the list of people from our data

    docs = db.collection(u'Leagues').stream()
    all_leagues = []
    for league in [doc.to_dict() for doc in docs]:
        linked_leagues = [ref.get().to_dict() for ref in league['linked_leagues']]
        league['linked_leagues']=linked_leagues
        all_leagues.append(league)
        logging.debug(f"League: {league}")
    return all_leagues

# TODO: We may want to change the /<partner_id> to something less strict like ?partner_id=<partner_id>

@loggedIn
@leagues.route('/leagues/<int:league_id>', methods=['GET'])
@response(LeagueSchema())
@other_responses({404: 'League not found'})
def get(league_id):
    """Retrieve a League by ID"""
    """
    This function responds to a request for /api/leagues/{league_id}
    with one matching league from leagues
    :param league_id:   Id of league to find
    :return:            league matching id
    """
    # Get the partner requested
    # Get all user accounts where id is in users
    user = request.user
    print(f"User: {user}")
    #doc_ref = db.collection(u'leagues').where(user['id'],'in','users').document(league_id)
    doc_ref = db.collection(u'Leagues').document(league_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
        return doc.to_dict()
    else:
        print(u'No such document!')
        abort(404)

@loggedIn
@leagues.route('/leagues', methods=['POST'])
@body(LeagueSchema())
@response(LeagueSchema(), 201)
@other_responses({400: f"Adding League Failed - message"})
def create(league):
    """Create New League"""
    """
    This function creates a new partner in the partners structure
    based on the passed in partner data
    :param partner:  partner to create in people structure
    :return:        201 on success, 406 on partner exists
    """
    name = league.get("name")
    logging.info(f"Creating League: {name}")
    logging.debug(league)

    linked_leagues = []
    if 'linked_leagues' in league:
        linked_leagues = league.get("linked_leagues")
        # Insert Linked League
    
    # TODO Check if League already exists?


    # Insert Linked Leagues
    linked_league_references = []
    for linked_league in linked_leagues:

        # Does linked league already exists?
        status, ref, message = linkedLeagues.get(linked_league['league_id'])
        
        if status == 200:
            pass
            # Does it belong to a League already? 
            # yes:
                # Abort
            # no:
                # Should Linked Leagues be allowed to be orphaned?
        else:
            status, ref, message = linkedLeagues.create(linked_league)
        
        if status == 201:
           linked_league_references.append(ref)
        else:
            # TODO We need to undo the previous add if one fails
            abort(400, f"Adding League Failed - {message}")

    # Insert League
    data ={
        u'name': league.get("name"),
        u'avatar': league.get("avatar"),
        u'linked_leagues': linked_league_references,
    }

    # Add a new doc in collection 'Leagues'
    db.collection(u'Leagues').add(data)
    
@loggedIn
@leagues.route('/leagues/<int:league_id>', methods=['PUT'])
@body(LeagueSchema())
@response(LeagueSchema())
@other_responses({404: "League Not Found", 400: f"League Update Failed - <message>"})
def update(league, league_id):
    """Update League"""
    """
    This function updates an existing league in the league structure.
    :param league_id:   Id of the League to update in the people structure
    :param league:     League to update
    :return:            updated partner structure
    """

    ref = db.collection(u'Leagues').document(league_id)

    # Set the capital field
    ref.update(league)
    
    status, new_league_ref, message  = get(league_id)
    if status == 200:
        return new_league_ref.get()
    abort(400, "League could not be retrieved after updating")

@loggedIn
@leagues.route('/leagues/<int:league_id>', methods=['DELETE'])
@other_responses({404: "League not found", 400: "League Delete Failed - <message>"})
def delete(league_id):
    """Delete Partner"""
    """
    This function deletes a partner from the people structure
    :param partner_id:   Id of the partner to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the partner requested
    status, ref, message = get(league_id)

    # Did we find a partner?
    if status == 200:
        db.collection(u'Leagues').document(league_id).delete()
        return "League Deleted", 200
    # Otherwise, nope, didn't find that partner
    else:
        abort(404, f"League id {league_id} not found")
