from api.app import db, ma
from datetime import date

import sqlalchemy as sqla

class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)

class CmAccount(Updateable, db.Model):
    __tablename__ = "cm_accounts"
    # ID Assigned from our database
    account_id = db.Column(db.Integer, primary_key=True)
    # ID of the partner that owns the account
    partner_id = db.Column(
        db.Integer,
        db.ForeignKey('partners.partner_id'), 
        # nullable=False
    )
    # ID from CM
    platform_id = db.Column(db.Integer, nullable=False)
    # Name of the Account on CM
    platform_name = db.Column(db.String(255), nullable=False)
    # If CM account is sub account, include the sub account id
    platform_subaccount_id = db.Column(db.Integer)
    platform_subaccount_name = db.Column(db.String(255))
    msa_date = db.Column(db.DateTime)
    setup_fee = db.Column(db.Integer)
    notes = db.Column(db.String(255))

class CmAccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CmAccount
        include_fk = True
        sqla_session = db.session
    rates = ma.List(ma.Dict, dump_default=[])

