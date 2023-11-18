from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.TrainingWebinars import TrainingWebinar, TrainingWebinarSchema
from webapp.api.utils.database import db
import os, random, string
from base64 import b64decode, decodebytes

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

UPLOADDIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "static", "uploads")
)

trainingwebinar_routes = Blueprint("trainingwebinar_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@trainingwebinar_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_trainingwebinar():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        data = request.get_json()
        trainingwebinar_schema = (
            TrainingWebinarSchema()
        )  # schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        trainingwebinar = trainingwebinar_schema.load(data)
        # need validation in ad creation process
        trainingwebinarobj = TrainingWebinar(
            webinartitle=trainingwebinar["webinartitle"],
            webinarimgurl=trainingwebinar["webinarimgurl"],
            webinardesc=trainingwebinar["webinardesc"],
            webinartext=trainingwebinar["webinartext"],
            startdate=trainingwebinar["startdate"],
            enddate=trainingwebinar["enddate"],
            level=trainingwebinar["level"],
            price=trainingwebinar["price"],
            file=trainingwebinar["file"],
        )
        trainingwebinarobj.author_id = trainingwebinar["author_id"]
        imgfile = b64decode(trainingwebinarobj.file.split(",")[1] + "==")
        print(imgfile)
        print(UPLOADDIR)
        with open(UPLOADDIR + "/" + trainingwebinarobj.webinarimgurl, "wb") as f:
            f.write(imgfile)
        # save to db
        trainingwebinarobj.create()
        result = trainingwebinar_schema.dump(trainingwebinarobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "trainingwebinar": result,
                "logged_in_as": current_user,
                "message": "A training webinar has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@trainingwebinar_routes.route("/all", methods=["GET", "OPTIONS"])
def get_trainingwebinars():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = TrainingWebinar.query.all()
    trainingwebinar_schema = TrainingWebinarSchema(
        many=True,
        only=[
            "idwebinar",
            "webinartitle",
            "webinarimgurl",
            "webinardesc",
            "webinartext",
            "startdate",
            "enddate",
            "level",
            "price",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    trainingwebinars = trainingwebinar_schema.dump(fetch)
    descendingwebinars = sorted(trainingwebinars, key=lambda x: x["idwebinar"], reverse=True)
    return response_with(resp.SUCCESS_200, value={"trainingwebinars": descendingwebinars})


@trainingwebinar_routes.route("/<int:id>", methods=["GET", "OPTIONS"])
def get_specific_trainingwebinar(id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = TrainingWebinar.query.get_or_404(id)
    trainingwebinar_schema = TrainingWebinarSchema(
        many=False,
        only=[
            "idwebinar",
            "webinartitle",
            "webinarimgurl",
            "webinardesc",
            "webinartext",
            "startdate",
            "enddate",
            "level",
            "price",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    trainingwebinar = training_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"trainingwebinar": trainingwebinar})


# UPDATE (U)

# DELETE (D)
