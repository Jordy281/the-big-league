from api.app import db, ma
from datetime import date

import sqlalchemy as sqla
from sqlalchemy import orm as sqla_orm

class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class DvAccount(Updateable, db.Model):
    __tablename__ = "dv_accounts"
    # ID Assigned from our database
    account_id = db.Column(db.Integer, primary_key=True)
    # ID of the partner that owns the account
    partner_id = db.Column(
        db.Integer,
        db.ForeignKey('partners.partner_id'), 
        # nullable=False
    )
    # ID from DV360
    platform_id = db.Column(db.Integer, nullable=False)
    # Name of the Account on DV360
    platform_name = db.Column(db.String(255), nullable=False)
    # If CM account is sub account, include the sub account id

    # TODO: This should be a date column, it has no business being a string - but it only works if its a string. fml
    msa_date = db.Column(db.String(255))
    #msa_date = db.Column(db.Date)
    setup_fee = db.Column(db.Integer)
    profile_currency = db.Column(db.String(255))
    cad_billing_profile_name = db.Column(db.String(255))
    cad_billing_profile_id = db.Column(db.Integer)
    usd_billing_profile_name = db.Column(db.String(255))
    usd_billing_profile_id = db.Column(db.Integer)
    notes = db.Column(db.String(255))
    platform_subaccount_id = db.Column(db.Integer)
    # If CM account is sub account, include the sub account name
    platform_subaccount_name = db.Column(db.String(255))
    

class DvAccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DvAccount
        sqla_session = db.session
        include_fk = True
    rates = ma.List(ma.Dict,dump_default=[])
