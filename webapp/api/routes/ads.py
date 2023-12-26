from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Ads import Ad, AdSchema
from webapp.api.utils.database import db
import os, random, string
from PIL import Image
from base64 import b64decode, decodebytes

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

UPLOADDIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "static", "uploads")
)

ad_routes = Blueprint("ad_routes", __name__)


# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@ad_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_ads():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        data = request.get_json()
        ad_schema = (
            AdSchema()
        )  # ad schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        ad = ad_schema.load(data)
        # need validation in ad creation process
        adobj = Ad(
            adcampaigntitle=ad["adcampaigntitle"],
            adimgurl=ad["adimgurl"],
            adcampaigndesc=ad["adcampaigndesc"],
            adcampaigntext=ad["adcampaigntext"],
            nrdaysserved=ad["nrdaysserved"],
            kodetagihan=ad["kodetagihan"],
            file=ad["file"],
        )
        adobj.advertiser_id = ad["advertiser_id"]
        imgfile = b64decode(adobj.file.split(",")[1] + "==")
        print(imgfile)
        print(UPLOADDIR)
        with open(UPLOADDIR + "/" + adobj.adimgurl, "wb") as f:
            f.write(imgfile)
        # save to db
        adobj.create()
        result = ad_schema.dump(adobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "ad": result,
                "logged_in_as": current_user,
                "message": "An ad has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (C)
@ad_routes.route("/all", methods=["GET", "OPTIONS"])
def get_ads():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = Ad.query.all()
    ad_schema = AdSchema(
        many=True,
        only=[
            "idad",
            "adcampaigntitle",
            "adimgurl",
            "adcampaigndesc",
            "adcampaigntext",
            "nrdaysserved",
            "kodetagihan",
            "is_paid",
            "is_blocked",
            "created_at",
            "updated_at",
            "advertiser_id",
        ],
    )
    ads = ad_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"ads": ads})


@ad_routes.route("/<int:id>", methods=["GET", "OPTIONS"])
def get_specific_ad(id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = Ad.query.get_or_404(id)
    ad_schema = AdSchema(
        many=False,
        only=[
            "idad",
            "adcampaigntitle",
            "adimgurl",
            "adcampaigndesc",
            "adcampaigntext",
            "nrdaysserved",
            "kodetagihan",
            "is_paid",
            "is_blocked",
            "created_at",
            "updated_at",
            "advertiser_id",
        ],
    )
    ad = ad_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"ad": ad})


# UPDATE (U)
@ad_routes.route("/update/<int:id>", methods=["PUT", "OPTIONS"])
@jwt_required()
def update_ad(id):
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        adobj = Ad.query.get_or_404(id)
        data = request.get_json()
        ad_schema = AdSchema()
        ad = ad_schema.load(data, partial=True)
        if "adcampaigntitle" in ad and ad["adcampaigntitle"] is not None:
            if ad["adcampaigntitle"] != "":
                adobj.adcampaigntitle = ad["adcampaigntitle"]
        if "adimgurl" in ad and ad["adimgurl"] is not None:
            if ad["adimgurl"] != "":
                adobj.adimgurl = ad["adimgurl"]
        if "adcampaigndesc" in ad and ad["adcampaigndesc"] is not None:
            if ad["adcampaigndesc"] != "":
                adobj.adcampaigndesc = ad["adcampaigndesc"]
        if "nrdaysserved" in ad and ad["nrdaysserved"] is not None:
            if ad["nrdaysserved"] != "":
                adobj.nrdaysserved = ad["nrdaysserved"]
        if "is_paid" in ad and ad["is_paid"] is not None:
            if ad["is_paid"] != "":
                adobj.is_paid = ad["is_paid"]
        if "is_blocked" in ad and ad["is_blocked"] is not None:
            if ad["is_blocked"] != "":
                adobj.is_blocked = ad["is_blocked"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "ad": ad,
                "logged_in_as": current_user,
                "message": "Ad details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@ad_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_ad(id):
    current_user = get_jwt_identity()
    adobj = Ad.query.get_or_404(id)
    db.session.delete(adobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "Ad successfully deleted!"},
    )
