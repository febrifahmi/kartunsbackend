from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.AdsSubscriptions import AdSubscription, AdsubSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

adsub_routes = Blueprint("adsub_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@adsub_routes.route("/create", methods=["POST"])
@jwt_required()
def create_adsub():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        adsub_schema = (
            AdsubSchema()
        )  # Adsub schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        adsub = adsub_schema.load(data)
        # need validation in tsub creation process
        adsubobj = AdSubscription(
            adsubnumber=adsub["adsubnumber"],
        )
        result = adsub_schema.dump(adsubobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "adsubscription": result,
                "logged_in_as": current_user,
                "message": "An ad subscription has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@adsub_routes.route("/all", methods=["GET"])
def get_adsub():
    fetch = AdSubscription.query.all()
    adsub_schema = AdsubSchema(
        many=True,
        only=[
            "idadsub",
            "adsubnumber",
            "created_at",
            "updated_at",
            "subscriber_id",
            "ad_id",
        ],
    )
    adsubs = adsub_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"adsubscriptions": adsubs})


@adsub_routes.route("/<int:id>", methods=["GET"])
def get_specific_adsub(id):
    fetch = AdSubscription.query.get_or_404(id)
    adsub_schema = AdsubSchema(
        many=False,
        only=[
            "idadsub",
            "adsubnumber",
            "created_at",
            "updated_at",
            "subscriber_id",
            "ad_id",
        ],
    )
    adsub = adsub_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"adsubscription": adsub})


# UPDATE (U)
@adsub_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_adsub(id):
    try:
        current_user = get_jwt_identity()
        adsubobj = AdSubscription.query.get_or_404(id)
        data = request.get_json()
        adsub_schema = AdsubSchema()
        adsub = adsub_schema.load(data, partial=True)
        if adsub["tsubnumber"] is not None:
            adsubobj.tsubnumber = adsubobj["tsubnumber"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "trainingsubscription": adsub,
                "logged_in_as": current_user,
                "message": "Ad subscription details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@adsub_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_adsub(id):
    current_user = get_jwt_identity()
    adsubobj = AdSubscription.query.get_or_404(id)
    db.session.delete(adsubobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "Ads subscription successfully deleted!"},
    )

