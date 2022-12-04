from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Ads import Ad, AdSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

ad_routes = Blueprint("ad_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@ad_routes.route("/create", methods=["POST"])
@jwt_required()
def create_ads():
    try:
        pass
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (C)
@ad_routes.route("/all", methods=["GET"])
def get_ads():
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
            "is_blocked",
            "created_at",
            "updated_at",
            "advertiser_id",
        ],
    )
    ads = ad_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"ads": ads})

@ad_routes.route("/<int:id>", methods=["GET"])
def get_specific_ad(id):
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
            "is_blocked",
            "created_at",
            "updated_at",
            "advertiser_id",
        ],
    )
    ad = ad_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"ad": ad})


# UPDATE (U)
@ad_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_ad(id):
    try:
        current_user = get_jwt_identity()
        adobj = Ad.query.get_or_404(id)
        data = request.get_json()
        ad_schema = AdSchema()
        ad = ad_schema.load(data, partial=True)
        if ad["adcampaigntitle"] is not None:
            adobj.adcampaigntitle = ad["adcampaigntitle"]
        if ad["adimgurl"] is not None:
            adobj.adimgurl = ad["adimgurl"]
        if ad["adcampaigndesc"] is not None:
            adobj.adcampaigndesc = ad["adcampaigndesc"]
        if ad["nrdaysserved"] is not None:
            adobj.nrdaysserved = ad["nrdaysserved"]
        if ad["is_blocked"] is not None:
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