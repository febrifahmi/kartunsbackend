from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.TrainingSubscriptions import TrainingSubscription, TsubsSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

tsub_routes = Blueprint("tsub_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@tsub_routes.route("/create", methods=["POST"])
@jwt_required()
def create_tsub():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        tsub_schema = (
            TsubsSchema()
        )  # tsub schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        tsub = tsub_schema.load(data)
        # need validation in tsub creation process
        tsubobj = TrainingSubscription(
            tsubsnumber=tsub["tsubsnumber"],
        )
        result = tsub_schema.dump(tsubobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "trainingsubscription": result,
                "logged_in_as": current_user,
                "message": "A training subscription has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@tsub_routes.route("/all", methods=["GET"])
def get_tsub():
    fetch = TrainingSubscription.query.all()
    tsub_schema = TsubsSchema(
        many=True,
        only=[
            "idtsub",
            "tsubnumber",
            "created_at",
            "updated_at",
            "subscriber_id",
            "training_id",
        ],
    )
    tsubs = tsub_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"trainingsubscriptions": tsubs})


@tsub_routes.route("/<int:id>", methods=["GET"])
def get_specific_tsub(id):
    fetch = TrainingSubscription.query.get_or_404(id)
    tsub_schema = TsubsSchema(
        many=False,
        only=[
            "idtsub",
            "tsubnumber",
            "created_at",
            "updated_at",
            "subscriber_id",
            "training_id",
        ],
    )
    tsub = tsub_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"trainingsubscription": tsub})


# UPDATE (U)
@tsub_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_tsub(id):
    try:
        current_user = get_jwt_identity()
        tsubobj = TrainingSubscription.query.get_or_404(id)
        data = request.get_json()
        tsub_schema = TsubsSchema()
        tsub = tsub_schema.load(data, partial=True)
        if tsub["tsubnumber"] is not None:
            tsubobj.tsubnumber = tsub["tsubnumber"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "trainingsubscription": tsub,
                "logged_in_as": current_user,
                "message": "Training subscription details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@tsub_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_tsub(id):
    current_user = get_jwt_identity()
    tsubobj = TrainingSubscription.query.get_or_404(id)
    db.session.delete(tsubobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "Training subscription successfully deleted!"},
    )

