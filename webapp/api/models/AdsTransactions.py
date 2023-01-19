# this model schema is used to accept midtrans API charge/transaction response body 
import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class AdTransaction(db.Model):
    __tablename__ = "adtransaction"
    idadtransaction = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_code = db.Column(db.String)
    status_message = db.Column(db.String)
    transaction_id = db.Column(db.String)
    order_id = db.Column(db.String)
    merchant_id = db.Column(db.String)
    gross_amount = db.Column(db.String)
    currency = db.Column(db.String)
    payment_type = db.Column(db.String)
    transaction_time = db.Column(db.String)
    transaction_status = db.Column(db.String)
    signature_key = db.Column(db.String)
    expiry_time = db.Column(db.String)
    va_number = db.Column(db.String)
    bank = db.Column(db.String)
    fraud_status = db.Column(db.String)
    settlement_time = db.Column(db.String)
    paid_at = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk

    def __init__(
        self,
        status_code, status_message, transaction_id, order_id, merchant_id, gross_amount, currency, payment_type, transaction_time, transaction_status, fraud_status, signature_key, expiry_time, va_number, bank
    ):
        self.status_code = status_code
        self.status_message = status_message
        self.transaction_id = transaction_id
        self.order_id = order_id
        self.merchant_id = merchant_id
        self.gross_amount = gross_amount
        self.currency = currency
        self.payment_type = payment_type
        self.transaction_time = transaction_time
        self.transaction_status = transaction_status
        self.fraud_status = fraud_status
        self.signature_key = signature_key
        self.expiry_time = expiry_time
        self.va_number = va_number
        self.bank = bank

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class AdTransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AdTransaction
        sqla_session = db.session

    idadtransaction = fields.Integer(dump_only=True)
    status_code = fields.String()
    status_message = fields.String()
    transaction_id = fields.String()
    order_id = fields.String()
    merchant_id = fields.String()
    gross_amount = fields.String()
    currency = fields.String()
    payment_type = fields.String()
    signature_key = fields.String()
    expiry_time = fields.String()
    transaction_time = fields.String()
    transaction_status = fields.String()
    va_number = fields.String()
    bank = fields.String()
    fraud_status = fields.String()
    settlement_time = fields.String()
    paid_at = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)