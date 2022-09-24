from email.policy import default
from api.app import db, ma
from datetime import datetime
from marshmallow import fields
from api.models import DvAccountSchema, CmAccountSchema


class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class Partner(Updateable, db.Model):
    __tablename__ = "partners"
    partner_id = db.Column(db.Integer, primary_key=True)
    partner_name = db.Column(db.String(255), index=True,nullable=False)
    active = db.Column(db.Boolean, default=True)
    can_po_billing_code = db.Column(db.String(255))
    us_po_billing_code = db.Column(db.String(255))
    tax_code = db.Column(db.String(255))
    terms = db.Column(db.String(255))
    tax_reg_no = db.Column(db.String(255))
    payment_method = db.Column(db.String(255))
    preferred_delivery_method = db.Column(db.String(255))
    customer_type = db.Column(db.String(255))
    customer_language = db.Column(db.String(255))
    notes = db.Column(db.String(255))
    
    dv_accounts = db.relationship(
        "DvAccount",
        backref='partners',
        cascade='all, delete, delete-orphan',
        single_parent=True
        #order_by='desc(platform_name)'
    )
    cm_accounts = db.relationship(
        "CmAccount",
        backref='partners',
        cascade='all, delete, delete-orphan',
        single_parent=True
        #order_by='desc(platform_name)'
    )

class PartnerSchema(ma.SQLAlchemyAutoSchema):
    #def __init__(self, **kwargs):
    #    super().__init__(**kwargs)
    class Meta:
        model = Partner
        sqla_session = db.session
    
    

class PartnerWithAccountsSchema(ma.SQLAlchemyAutoSchema):
    #def __init__(self, **kwargs):
    #    super().__init__(**kwargs)
    class Meta:
        model = Partner
        sqla_session = db.session
    dv_accounts = fields.Nested("DvAccountSchema", dump_default=[], many=True)
    cm_accounts = fields.Nested("CmAccountSchema", dump_default=[], many=True)