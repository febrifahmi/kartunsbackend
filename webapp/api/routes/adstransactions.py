from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.AdsTransactions import AdTransaction, AdTransactionSchema
from webapp.api.utils.database import db

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
            expire_time=data["expire_time"],
            transaction_time=data["transaction_time"],
            transaction_status=data["transaction_status"],
            fraud_status=data["fraud_status"],
            va_number=data["va_numbers"][0]["va_number"],
            bank=data["va_numbers"][0]["bank"],
        )
        print("Object: ", adtransactionobj)
        existingtransaction = AdTransaction.query.all()
        existingtransaction_schema = AdTransactionSchema(
            many=True,
            only=[
                "order_id",
            ],
        )
        existingtransactions = existingtransaction_schema.dump(existingtransaction)
        transactionexist = False
        for item in existingtransactions:
            if item["order_id"] == adtransactionobj.order_id:
                update_adtransaction(item["idadtransaction"])
                transactionexist = True
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
            "expire_time",
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
            "expire_time",
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
        adtransaction_schema = AdTransactionSchema()
        adtransaction = adtransaction_schema.load(data, partial=True)
        if adtransaction["status_code"] is not None:
            adtransactionobj.status_code = adtransaction["status_code"]
        if adtransaction["status_message"] is not None:
            adtransactionobj.status_message = adtransaction["status_message"]
        if adtransaction["transaction_id"] is not None:
            adtransactionobj.transaction_id = adtransaction["transaction_id"]
        if adtransaction["gross_amount"] is not None:
            adtransactionobj.gross_amount = adtransaction["gross_amount"]
        if adtransaction["currency"] is not None:
            adtransactionobj.currency = adtransaction["currency"]
        if adtransaction["payment_type"] is not None:
            adtransactionobj.payment_type = adtransaction["payment_type"]
        if adtransaction["signature_key"] is not None:
            adtransactionobj.signature_key = adtransaction["signature_key"]
        if adtransaction["expire_time"] is not None:
            adtransactionobj.expire_time = adtransaction["expire_time"]
        if adtransaction["transaction_time"] is not None:
            adtransactionobj.transaction_time = adtransaction["transaction_time"]
        if adtransaction["transaction_status"] is not None:
            adtransactionobj.transaction_status = adtransaction["transaction_status"]
        if adtransaction["fraud_status"] is not None:
            adtransactionobj.fraud_status = adtransaction["fraud_status"]
        if adtransaction["va_number"] is not None:
            adtransactionobj.va_number = adtransaction["va_number"]
        if adtransaction["bank"] is not None:
            adtransactionobj.bank = adtransaction["bank"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "adtransaction": adtransaction,
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
        value={"logged_in_as": current_user, "message": "Ads transaction successfully deleted!"},
    )

