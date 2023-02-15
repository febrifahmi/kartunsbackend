from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.JobOffers import JobOffer, JobOfferSchema
from webapp.api.utils.database import db
from werkzeug.utils import secure_filename
import os, random, string
from flask import current_app

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

joboffer_routes = Blueprint("joboffer_routes", __name__)


# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@joboffer_routes.route("/create", methods=["POST"])
@jwt_required()
def create_offer():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        offer_schema = (
            JobOfferSchema()
        )  # ad schema pertama didefinisikan full utk menerima seluruh data yang diperlukan termasuk password
        offer = offer_schema.load(data)
        # need validation in ad creation process
        offerobj = JobOffer(
            offertitle=offer["offertitle"],
            offerdesc=offer["offerdesc"],
            offertext=offer["offertext"],
            companylogo=offer["companylogo"]
        )
        offerobj.author_id = offer["author_id"]
        offerobj.is_approved = 0
        # save to db
        offerobj.create()
        # cek apakah file yang diupload sesuai daftar jenis file yg diijinkan
        result = offer_schema.dump(offerobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "offer": result,
                "logged_in_as": current_user,
                "message": "An offer has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@joboffer_routes.route("/all", methods=["GET"])
def get_offers():
    fetch = JobOffer.query.all()
    offer_schema = JobOfferSchema(
        many=True,
        only=[
            "idoffer",
            "offertitle",
            "companylogo",
            "offerdesc",
            "offertext",
            "is_approved",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    offers = offer_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"offer": offers})


@joboffer_routes.route("/<int:id>", methods=["GET"])
def get_specific_offer(id):
    fetch = JobOffer.query.get_or_404(id)
    offer_schema = JobOfferSchema(
        many=False,
        only=[
            "idoffer",
            "offertitle",
            "companylogo",
            "offerdesc",
            "offertext",
            "is_approved",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    offer = offer_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"offer": offer})


# UPDATE (U)
@joboffer_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_offer(id):
    try:
        current_user = get_jwt_identity()
        offerobj = JobOffer.query.get_or_404(id)
        data = request.get_json()
        offer_schema = JobOfferSchema()
        offer = offer_schema.load(data, partial=True)
        if "offertitle" in offer and offer["offertitle"] is not None:
            if offer["offertitle"] != "":
                offerobj.offertitle = offer["offertitle"]
        if "companylogo" in offer and offer["companylogo"] is not None:
            if offer["companylogo"] != "":
                offerobj.companylogo = offer["companylogo"]
        if "offerdesc" in offer and offer["offerdesc"] is not None:
            if offer["offerdesc"] != "":
                offerobj.offerdesc = offer["offerdesc"]
        if "offertext" in offer and offer["offertext"] is not None:
            if offer["offertext"] != "":
                offerobj.offertext = offer["offertext"]
        if "is_approved" in offer and offer["is_approved"] is not None:
            if offer["is_approved"] != "":
                offerobj.is_approved = offer["is_approved"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "offer": offer,
                "logged_in_as": current_user,
                "message": "Offer details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@joboffer_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_offer(id):
    current_user = get_jwt_identity()
    offerobj = JobOffer.query.get_or_404(id)
    db.session.delete(offerobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={
            "logged_in_as": current_user,
            "message": "An offer successfully deleted!",
        },
    )
