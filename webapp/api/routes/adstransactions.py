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
        adtransaction_schema = (
            AdTransactionSchema()
        )  # Adsub schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        adtransaction = adtransaction_schema.load(data)
        # need validation in tsub creation process
        adtransactionobj = AdTransaction(
            statuscode=adtransaction["statuscode"],
            status_message=adtransaction["status_message"],
            transaction_id=adtransaction["transaction_id"],
            order_id=adtransaction["order_id"],
            merchant_id=adtransaction["merchant_id"],
            gross_amount=adtransaction["gross_amount"],
            currency=adtransaction["currency"],
            payment_type=adtransaction["payment_type"],
            transaction_time=adtransaction["transaction_time"],
            transaction_status=adtransaction["transaction_status"],
            va_number=adtransaction["va_number"],
            fraud_status=adtransaction["fraud_status"],
        )
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
            "statuscode",
            "status_message",
            "transaction_id",
            "order_id",
            "merchant_id",
            "gross_amount",
            "currency",
            "payment_type",
            "transaction_time",
            "transaction_status",
            "va_number",
            "fraud_status",
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
            "statuscode",
            "status_message",
            "transaction_id",
            "order_id",
            "merchant_id",
            "gross_amount",
            "currency",
            "payment_type",
            "transaction_time",
            "transaction_status",
            "va_number",
            "fraud_status",
        ],
    )
    adtransaction = adtransaction_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"adtransaction": adtransaction})


# UPDATE (U)
@adtransaction_routes.route("/update/<int:id>", methods=["PUT"])
def update_adsub(id):
    try:
        adtransactionobj = AdTransaction.query.get_or_404(id)
        data = request.get_json()
        adtransaction_schema = AdTransactionSchema()
        adtransaction = adtransaction_schema.load(data, partial=True)
        if adtransaction["statuscode"] is not None:
            adtransactionobj.statuscode = adtransaction["statuscode"]
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
        if adtransaction["transaction_time"] is not None:
            adtransactionobj.transaction_time = adtransaction["transaction_time"]
        if adtransaction["transaction_status"] is not None:
            adtransactionobj.transaction_status = adtransaction["transaction_status"]
        if adtransaction["va_number"] is not None:
            adtransactionobj.va_number = adtransaction["va_number"]
        if adtransaction["fraud_status"] is not None:
            adtransactionobj.fraud_status = adtransaction["fraud_status"]
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

