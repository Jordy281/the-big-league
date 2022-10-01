from flask import Flask, redirect, url_for, request
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_mail import Mail
from apifairy import APIFairy
from flask_pymongo import PyMongo
from config import Config
from flask_sqlalchemy import SQLAlchemy

import logging
logging.basicConfig(level=logging.DEBUG)

db = SQLAlchemy()
ma = Marshmallow()
cors = CORS()
mail = Mail()
apifairy = APIFairy()
mongo = PyMongo()



# Initialize Firebase authentication
import firebase_admin
default_app = firebase_admin.initialize_app()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # extensions
    db.init_app(app)
    ma.init_app(app)
    mongo.init_app(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors.init_app(app)
    CORS(app)
    apifairy.init_app(app)

    # blueprints
    from api.errors import errors
    app.register_blueprint(errors)

    from api.partners import partners
    app.register_blueprint(partners, url_prefix='/api')

    from api.dvAccounts import dv_accounts
    app.register_blueprint(dv_accounts, url_prefix='/api')

    from api.cmAccounts import cm_accounts
    app.register_blueprint(cm_accounts, url_prefix='/api')
    #from api.fake import fake
    #app.register_blueprint(fake)
    """
    # define the shell context
    @app.shell_context_processor
    def shell_context():  # pragma: no cover
        ctx = {'db': db}
        for attr in dir(models):
            model = getattr(models, attr)
            if hasattr(model, '__bases__') and \
                    db.Model in getattr(model, '__bases__'):
                ctx[attr] = model
        return ctx
    """

    @app.route('/')
    def index():  # pragma: no cover
        return redirect(url_for('apifairy.docs'))
    
    @app.after_request
    def after_request(response):
        # Werkzeu sometimes does not flush the request body so we do it here
        request.get_data()
        return response
    
    # GCP's API Gateway does not support CORS. The only known workaround right now can be found here:
    # https://medium.com/call-for-atlas/connect-a-webapp-with-cors-and-google-api-gateway-94121ee74794
    CORS_HEADERS = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Max-Age": "3600",
    }
    @app.route('/handlecors', methods=['OPTIONS'])
    def handle_cors():
        return ("", 200, CORS_HEADERS)

    return app