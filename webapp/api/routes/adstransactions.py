from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.AdsTransactions import AdTransaction, AdTransactionSchema
from webapp.api.models.Ads import Ad, AdSchema
from webapp.api.utils.database import db
import json

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

adtransaction_routes = Blueprint("adtransaction_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@adtransaction_routes.route("/create", methods=["POST"])
def create_adtransaction():
    try:
        data = request.get_json()
        print(data)
        adtransaction_schema = AdTransactionSchema()
        # need validation in tsub creation process
        adtransactionobj = AdTransaction(
            status_code=data["status_code"],
            status_message=data["status_message"],
            transaction_id=data["transaction_id"],
            order_id=data["order_id"],
            merchant_id=data["merchant_id"],
            gross_amount=data["gross_amount"],
            currency=data["currency"],
            payment_type=data["payment_type"],
            signature_key=data["signature_key"],
            expiry_time=data["expiry_time"],
            transaction_time=data["transaction_time"],
            transaction_status=data["transaction_status"],
            fraud_status=data["fraud_status"],
            va_number=data["va_numbers"][0]["va_number"],
            bank=data["va_numbers"][0]["bank"],
        )
        if "settlement_time" in data:
            adtransactionobj.settlement_time=data["settlement_time"]
        print("Object: ", adtransactionobj)
        existingtransaction = AdTransaction.query.all()
        existingtransaction_schema = AdTransactionSchema(
            many=True,
            only=[
                "order_id",
                "idadtransaction",
            ],
        )
        existingads = Ad.query.all()
        existingads_schema = AdSchema(
            many=True,
            only=[
                "kodetagihan",
                "idad",
            ],
        )
        ads = existingads_schema.dump(existingads)
        for item in ads:
            if item["kodetagihan"] == adtransactionobj.order_id and adtransactionobj.transaction_status == "settlement":
                adobj = Ad.query.get_or_404(item["idad"])
                adobj.is_blocked = 0
                db.session.commit()
        existingtransactions = existingtransaction_schema.dump(existingtransaction)
        transactionexist = False
        for item in existingtransactions:
            if item["order_id"] == adtransactionobj.order_id:
                update_adtransaction(item["idadtransaction"])
                transactionexist = True
                result = adtransaction_schema.dump(adtransactionobj)
        if transactionexist == False:
            adtransactionobj.create()
            result = adtransaction_schema.dump(adtransactionobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "adtransaction": result,
                "message": "An ad transaction has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@adtransaction_routes.route("/all", methods=["GET"])
def get_adtransaction():
    fetch = AdTransaction.query.all()
    adtransaction_schema = AdTransactionSchema(
        many=True,
        only=[
            "status_code",
            "status_message",
            "transaction_id",
            "order_id",
            "merchant_id",
            "gross_amount",
            "currency",
            "payment_type",
            "signature_key",
            "expiry_time",
            "transaction_time",
            "transaction_status",
            "fraud_status",
            "va_number",
            "bank",
        ],
    )
    adtransactions = adtransaction_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"adtransactions": adtransactions})


@adtransaction_routes.route("/<int:id>", methods=["GET"])
def get_specific_adtransaction(id):
    fetch = AdTransaction.query.get_or_404(id)
    adtransaction_schema = AdTransactionSchema(
        many=False,
        only=[
            "status_code",
            "status_message",
            "transaction_id",
            "order_id",
            "merchant_id",
            "gross_amount",
            "currency",
            "payment_type",
            "signature_key",
            "expiry_time",
            "transaction_time",
            "transaction_status",
            "fraud_status",
            "va_number",
            "bank",
        ],
    )
    adtransaction = adtransaction_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"adtransaction": adtransaction})


# UPDATE (U)
@adtransaction_routes.route("/update/<int:id>", methods=["PUT"])
def update_adtransaction(id):
    try:
        adtransactionobj = AdTransaction.query.get_or_404(id)
        data = request.get_json()
        if data["status_code"] is not None:
            adtransactionobj.status_code = data["status_code"]
        if data["status_message"] is not None:
            adtransactionobj.status_message = data["status_message"]
        if data["transaction_id"] is not None:
            adtransactionobj.transaction_id = data["transaction_id"]
        if data["gross_amount"] is not None:
            adtransactionobj.gross_amount = data["gross_amount"]
        if data["currency"] is not None:
            adtransactionobj.currency = data["currency"]
        if data["payment_type"] is not None:
            adtransactionobj.payment_type = data["payment_type"]
        if data["signature_key"] is not None:
            adtransactionobj.signature_key = data["signature_key"]
        if data["expiry_time"] is not None:
            adtransactionobj.expiry_time = data["expiry_time"]
        if data["transaction_time"] is not None:
            adtransactionobj.transaction_time = data["transaction_time"]
        if data["transaction_status"] is not None:
            adtransactionobj.transaction_status = data["transaction_status"]
        if data["fraud_status"] is not None:
            adtransactionobj.fraud_status = data["fraud_status"]
        if data["va_numbers"] is not None:
            adtransactionobj.va_number = data["va_numbers"][0]["va_number"]
        if data["va_numbers"] is not None:
            adtransactionobj.bank = data["va_numbers"][0]["bank"]
        if data["settlement_time"] is not None:
            adtransactionobj.settlement_time = data["settlement_time"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "message": "Ad transaction details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@adtransaction_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_adsub(id):
    current_user = get_jwt_identity()
    adtransactionobj = AdTransaction.query.get_or_404(id)
    db.session.delete(adtransactionobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={
            "logged_in_as": current_user,
            "message": "Ads transaction successfully deleted!",
        },
    )
