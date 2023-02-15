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
        if "status_code" in data and data["status_code"] is not None:
            if data["status_code"] != "":
                adtransactionobj.status_code = data["status_code"]
        if "status_message" in data and data["status_message"] is not None:
            if data["status_message"] != "":
                adtransactionobj.status_message = data["status_message"]
        if "transaction_id" in data and data["transaction_id"] is not None:
            if data["transaction_id"] != "":
                adtransactionobj.transaction_id = data["transaction_id"]
        if "gross_amount" in data and data["gross_amount"] is not None:
            if data["gross_amount"] != "":
                adtransactionobj.gross_amount = data["gross_amount"]
        if "currency" in data and data["currency"] is not None:
            if data["currency"] != "":
                adtransactionobj.currency = data["currency"]
        if "payment_type" in data and data["payment_type"] is not None:
            if data["payment_type"] != "":
                adtransactionobj.payment_type = data["payment_type"]
        if "signature_key" in data and data["signature_key"] is not None:
            if data["signature_key"] != "":
                adtransactionobj.signature_key = data["signature_key"]
        if "expiry_time" in data and data["expiry_time"] is not None:
            if data["expiry_time"] != "":
                adtransactionobj.expiry_time = data["expiry_time"]
        if "transaction_time" in data and data["transaction_time"] is not None:
            if data["transaction_time"] != "":
                adtransactionobj.transaction_time = data["transaction_time"]
        if "transaction_status" in data and data["transaction_status"] is not None:
            if data["transaction_status"] != "":
                adtransactionobj.transaction_status = data["transaction_status"]
        if "fraud_status" in data and data["fraud_status"] is not None:
            if data["fraud_status"] != "":
                adtransactionobj.fraud_status = data["fraud_status"]
        if "va_numbers" in data and data["va_numbers"] is not None: 
            if data["va_numbers"] != "":
                adtransactionobj.va_number = data["va_numbers"][0]["va_number"]
        if "va_numbers" in data and data["va_numbers"] is not None:
            if data["va_numbers"] != "":
                adtransactionobj.bank = data["va_numbers"][0]["bank"]
        if "settlement_time" in data and data["settlement_time"] is not None:
            if data["settlement_time"] != "":
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
