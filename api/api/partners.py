"""
This is the people module and supports all the REST actions for the
partners data
"""
from urllib import request
from api.app import db, ma

from flask import make_response, Blueprint, abort, request, jsonify, Response
from flask_cors import cross_origin, CORS

#from config import db
from api.models import Partner, PartnerSchema, PartnerWithAccountsSchema
from api.models import DvAccount
from api.models import CmAccount

import api.dvAccounts
import api.cmAccounts

from apifairy import authenticate, body, response, other_responses, arguments
from api.auth import loggedIn
import logging

partners = Blueprint('partners', __name__)
partner_schema = PartnerSchema()
partners_schema = PartnerSchema(many=True)

@partners.route('/partners', methods=['GET'])
@loggedIn
@response(PartnerSchema(many=True))
def all():
    """Retrieve all Partners"""
    """
    This function responds to a request for /api/partners
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    logging.debug("Getting All Partners")
    partners = Partner.query.order_by(Partner.partner_id).all()
    logging.debug(partners)
    return partners

# TODO: We may want to change the /<partner_id> to something less strict like ?partner_id=<partner_id>

@loggedIn
@partners.route('/partners/<int:partner_id>', methods=['GET'])
@response(PartnerWithAccountsSchema())
@other_responses({404: 'Partner not found'})
def get(partner_id):
    """Retrieve a Partner by ID"""
    """
    This function responds to a request for /api/partner/{partner_id}
    with one matching partner from people
    :param partner_id:   Id of partner to find
    :return:            partner matching id
    """
    # Get the partner requested
    logging.debug(f"Get partner: {partner_id}")
    partner = Partner.query.filter(Partner.partner_id == partner_id).one_or_none()
    logging.debug(partner)
    # Did we find a partner?
    if partner is not None:

        # Serialize the data for the response
        return partner

    # Otherwise, nope, didn't find that partner
    else:
        abort(404)


@loggedIn
@partners.route('/partners', methods=['POST'])
@body(PartnerWithAccountsSchema())
@response(PartnerWithAccountsSchema(), 201)
@other_responses({400: f"Adding Partner Failed"})
def create(partner):
    """Create New Partner"""
    """
    This function creates a new partner in the partners structure
    based on the passed in partner data
    :param partner:  partner to create in people structure
    :return:        201 on success, 406 on partner exists
    """
    name = partner.get("partner_name")
    logging.info(f"Creating Partner: {name}")
    logging.debug(partner)

    dv_accounts = []
    if 'dv_accounts' in partner:
        dv_accounts = partner.get("dv_accounts")
        del partner['dv_accounts']
    cm_accounts = []
    if 'cm_accounts' in partner:
        cm_accounts = partner.get("cm_accounts")
        del partner['cm_accounts']
    
    existing_partner = (
        Partner.query.filter(Partner.partner_name == name)
        .one_or_none()
    )
    # If the partner does not exist, we can insert it.
    if existing_partner is None:

        # Create a partner instance using the schema and the passed in partner
        logging.info("Adding partner to DB")
        new_partner = Partner(**partner)
        db.session.add(new_partner)
        db.session.commit()
        logging.info("Partner Added")
        for acc in dv_accounts:
            acc['partner_id'] = new_partner.partner_id
            #new_dv_account = DvAccount(**acc)
            #new_partner.dv_accounts.append(new_dv_account)
            #logging.info(f"Adding {name}'s DV360 Account {acc['platform_id']}-{acc['platform_name']}")
            #db.session.add(new_dv_account)
            logging.debug(f"Adding DV Account: {acc['platform_id']} - {acc['platform_name']}")
            logging.debug(acc)
            message, status_code = api.dvAccounts.create(acc)
            logging.debug(f"Status of adding DV Account: {status_code} - {message}")
            if status_code == 400:
                logging.error("Partner POST Failed - {message}")
                return abort(400, f"Adding Partner Failed - {message}")
        for acc in cm_accounts:
            """
            new_cm_account = CmAccount(**acc)
            new_partner.cm_accounts.append(new_cm_account)
            logging.info(f"Adding {name}'s CM360 Account {acc['platform_id']}-{acc['platform_name']}")
            db.session.add(new_cm_account)
            """
            acc['partner_id'] = new_partner.partner_id
            message, status_code = api.cmAccounts.create(acc)
            if status_code == 400:
                logging.error("Partner POST Failed - {message}")
                return abort(400, f"Adding Partner Failed - {message}")
        # Add the partner to the database
        return new_partner

    # Otherwise, nope, partner exists already
    else:
        logging.error("Partner POST Failed - partner name already exists")
        #return "Partner Name Already Exists", 400
        abort(400, "Adding Partner Failed - Partner name already exists!")

@loggedIn
@partners.route('/partners/<int:partner_id>', methods=['PUT'])
@body(PartnerSchema())
@response(PartnerSchema())
@other_responses({404: "Partner Not Found", 400: f"Partner Update Failed - <message>"})
def update(data, partner_id):
    """Update Partner"""
    """
    This function updates an existing partner in the partner structure
    Throws an error if a partner with the name we want to update to
    already exists in the database.
    :param partner_id:   Id of the partner to update in the people structure
    :param partner:      partner to update
    :return:            updated partner structure
    """
    # Get the partner requested from the db into session
    partner_name = data.get('partner_name')
    if partner_name is None or partner_name == "":
        abort(400, "Partner Update Failed - Partner name is required")
    partner = db.session.get(Partner, partner_id) or abort(404, "Partner Not Found")

    # Try to find an existing partner with the same name as the update
    existing_partner = (
        Partner.query.filter(Partner.partner_name == partner_name)
        .one_or_none()
    )

    # Would our update create a duplicate of another partner already existing?
    if (
        existing_partner is not None and 
        existing_partner.partner_name == partner_name and
        existing_partner.partner_id != partner_id
    ):
        abort(400, "Partner Update Failed - Partner name already exists")
        

    # Otherwise go ahead and update!
    partner.update(data)
    db.session.commit()

    return partner

@loggedIn
@partners.route('/partners/<int:partner_id>', methods=['DELETE'])
@other_responses({404: "Partner not found", 400: "Partner Delete Failed - <message>"})
def delete(partner_id):
    """Delete Partner"""
    """
    This function deletes a partner from the people structure
    :param partner_id:   Id of the partner to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the partner requested
    partner = Partner.query.filter(Partner.partner_id == partner_id).one_or_none()

    # Did we find a partner?
    if partner is not None:
        logging.info("Partner Found")
        message, status_code = api.dvAccounts.delete(partner_id=partner_id)
        if status_code != 200:
            abort(400, f"Partner Delete Failed - {message}")
        message, status_code = api.cmAccounts.delete(partner_id=partner_id)
        if status_code != 200:
            abort(400, f"Partner Delete Failed - {message}")
        db.session.delete(partner)
        db.session.commit()
        logging.info("Partner Deleted")
        return make_response(
            f"Partner {partner_id} deleted", 200
        )

    # Otherwise, nope, didn't find that partner
    else:
        abort(404, f"Partner id {partner_id} not found")
