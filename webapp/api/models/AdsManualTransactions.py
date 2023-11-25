import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class AdManualTransactions(db.Model):
    __tablename__ = "admanualtransactions"
    idadtransaction = db.Column(db.Integer, primary_key=True, autoincrement=True)
    adid = db.Column(db.Integer)
    kodetagihan = db.Column(db.String(64))
    is_paid = db.Column(db.Boolean(), default=0)
    transactionprove = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    advertiser_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    def __init__(self, adid, kodetagihan, is_paid, transactionprove, file):
        self.adid = adid
        self.kodetagihan = kodetagihan
        self.is_paid = is_paid
        self.transactionprove = transactionprove
        self.file = file

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class AdManualTransactionsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AdManualTransactions
        sqla_session = db.session

    idadtransaction = fields.Integer(dump_only=True)
    adid = fields.Integer(required=True)
    kodetagihan = fields.String(required=True)
    is_paid = fields.Boolean(required=True)
    transactionprovea = fields.String(required=True)
    file = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    advertiser_id = fields.Integer()
