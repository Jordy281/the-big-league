import pytest
from api.models import Partner, DvAccount, CmAccount
from api import create_app, db, ma, mongo
from config import Config
import os

class TestConfig(Config):
    SERVER_NAME = 'localhost.localdomain:5000'
    TESTING = True
    DISABLE_AUTH = True
    ALCHEMICAL_DATABASE_URL = 'sqlite://'

    # Get the folder of the top-level directory of this project
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # Update later by using a random number generator and moving
    # the actual key outside of the source code under version control
    SECRET_KEY = 'bad_secret_key'
    DEBUG = True

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app_test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Enable the TESTING flag to disable the error catching during request handling
    # so that you get better error reports when performing test requests against the application.

    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False

    mongo_host = os.environ.get('MONGO_HOST')
    mongo_port = os.environ.get('MONGO_PORT')
    mongo_username = os.environ.get('MONGO_USERNAME')
    mongo_password = os.environ.get('MONGO_PASSWORD')
    MONGO_URI = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/test_partners"


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(config_class=TestConfig)

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    dv_account1 = DvAccount(platform_name='init-dvAccount1', platform_id=1)
    dv_account2 = DvAccount(platform_name='init-dvAccount2', platform_id=2)
    cm_account1 = CmAccount(platform_name='init-cmAccount1', platform_id=1)
    cm_account2 = CmAccount(platform_name='init-cmAccount2', platform_id=2)

    user1 = Partner(partner_name='init-partner1', active=True, dv_accounts=[dv_account1, dv_account2], cm_accounts=[])
    user2 = Partner(partner_name='init-partner2', active=False, dv_accounts=[], cm_accounts=[cm_account1, cm_account2])
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    # Create the rates and pymongo
    mongo_client = mongo.db

    rates =[
        {
            "account_id": 1,
            "partner_id": 1,
            "platform_id": 1,
            "rates": [
                {
                    "max_usage_rate_threshold": None,
                    "max_usage_rate_threshold_unit": None,
                    "platform_tech_fee": 1,
                    "tier": "Self-Serve",
                    "total_media_fee": 1,
                    "trueview_pg_direct_tech_fee": 1
                }
            ]
        },
        {
            "account_id": 2,
            "partner_id": 2,
            "platform_id": 2,
            "rates": [
                {
                    "max_usage_rate_threshold": None,
                    "max_usage_rate_threshold_unit": None,
                    "platform_tech_fee": 2,
                    "tier": "Managed",
                    "total_media_fee": 2,
                    "trueview_pg_direct_tech_fee": 2
                }
            ]
        }
        
    ]
    result = mongo_client['dvRates'].insert_many(rates)    

    yield  # this is where the testing happens!

    db.drop_all()
    mongo_client['dvRates'].delete_many({})


@pytest.fixture(scope='module')
def partner():
    partner = Partner(partner_name='Dandelion-Test', active=True, dv_accounts=[], cm_accounts=[])
    return partner

@pytest.fixture(scope='module')
def dvAccount():
    return DvAccount(platform_name='DV-Account', platform_id=1234)

@pytest.fixture(scope='module')
def cmAccount():
    return CmAccount(platform_name='CM-Account', platform_id=9876)

@pytest.fixture(scope='module')
def partner_with_all_accounts(dvAccount, cmAccount):
    return Partner(partner_name='Dandelion-Test', active=True, dv_accounts=[dvAccount], cm_accounts=[cmAccount])


