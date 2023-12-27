from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.JobOffers import JobOffer, JobOfferSchema
from webapp.api.utils.database import db
from webapp.api.utils.utility import getrandomstring
from werkzeug.utils import secure_filename
import os, random, string
from flask import current_app
from PIL import Image
from base64 import b64decode, decodebytes

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta, datetime

UPLOADDIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "static", "uploads")
)

joboffer_routes = Blueprint("joboffer_routes", __name__)


# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@joboffer_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_offer():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
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
            offertype=offer["offertype"],
            startdate=offer["startdate"],
            enddate=offer["enddate"],
            salaryrange=offer["salaryrange"],
            offertext=offer["offertext"],
            companylogo=offer["companylogo"],
            file=offer["file"],
        )
        # filename = secure_filename(offerobj.companylogo)
        offerobj.companylogo = (
            "lowongan_"
            + offerobj.offertype
            + "_"
            + datetime.today().strftime("%Y%m%d")
            + "_"
            + getrandomstring(16)
            + ".png"
        )
        offerobj.author_id = offer["author_id"]
        offerobj.is_approved = 0
        offerobj.is_blocked = 0
        imgfile = b64decode(offerobj.file.split(",")[1] + "==")
        print(imgfile)
        print(UPLOADDIR)
        with open(UPLOADDIR + "/" + offerobj.companylogo, "wb") as f:
            f.write(imgfile)
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
@joboffer_routes.route("/all", methods=["GET", "OPTIONS"])
def get_offers():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = JobOffer.query.all()
    offer_schema = JobOfferSchema(
        many=True,
        only=[
            "idoffer",
            "offertitle",
            "companylogo",
            "offerdesc",
            "offertype",
            "startdate",
            "enddate",
            "salaryrange",
            "offertext",
            "is_approved",
            "is_blocked",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    offers = offer_schema.dump(fetch)
    descendingoffers = sorted(offers, key=lambda x: x["idoffer"], reverse=True)
    return response_with(resp.SUCCESS_200, value={"offers": descendingoffers})


@joboffer_routes.route("/<int:id>", methods=["GET", "OPTIONS"])
def get_specific_offer(id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = JobOffer.query.get_or_404(id)
    offer_schema = JobOfferSchema(
        many=False,
        only=[
            "idoffer",
            "offertitle",
            "companylogo",
            "offerdesc",
            "offertype",
            "startdate",
            "enddate",
            "salaryrange",
            "offertext",
            "is_approved",
            "is_blocked",
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
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
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
        if "offertype" in offer and offer["offertype"] is not None:
            if offer["offertype"] != "":
                offerobj.offertype = offer["offertype"]
        if "salaryrange" in offer and offer["salaryrange"] is not None:
            if offer["salaryrange"] != "":
                offerobj.salaryrange = offer["salaryrange"]
        if "offertext" in offer and offer["offertext"] is not None:
            if offer["offertext"] != "":
                offerobj.offertext = offer["offertext"]
        if "is_approved" in offer and offer["is_approved"] is not None:
            if offer["is_approved"] != "":
                offerobj.is_approved = offer["is_approved"]
        if "is_blocked" in offer and offer["is_blocked"] is not None:
            if offer["is_blocked"] != "":
                offerobj.is_blocked = offer["is_blocked"]
        if "author_id" in offer and offer["author_id"] is not None:
            if offer["author_id"] != "":
                offerobj.author_id = offer["author_id"]
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
