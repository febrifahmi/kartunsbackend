from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.PesertaWebinars import PesertaWebinar, PesertaWebinarSchema
from webapp.api.utils.database import db
from werkzeug.utils import secure_filename
import os, random, string
from base64 import b64decode, decodebytes

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

pesertawebinar_routes = Blueprint("pesertawebinar_routes", __name__)


# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@pesertawebinar_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_pesertawebinar():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        data = request.get_json()
        pesertawebinar_schema = (
            PesertaWebinarSchema()
        )  # schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        pesertawebinar = pesertawebinar_schema.load(data)
        # need validation in ad creation process
        pesertawebinarobj = PesertaWebinar(
            namapeserta=pesertawebinar["namapeserta"],
            training_id=pesertawebinar["training_id"],
            user_id=pesertawebinar["user_id"],
        )
        # cek eksisting user id and training id, if exist block request otherwise continue save to db
        fetch = PesertaWebinar.query.filter_by(user_id=pesertawebinar["user_id"]).all()
        eksistingpesertawebinar = pesertawebinar_schema.dump(fetch, many=True)
        print("Eksisting data: ", eksistingpesertawebinar)
        for item in eksistingpesertawebinar:
            if (
                item["training_id"] == pesertawebinar["training_id"]
                and item["user_id"] == pesertawebinar["user_id"]
            ):
                return response_with(
                    resp.INVALID_INPUT_422,
                    value={
                        "logged_in_as": current_user,
                        "message": "Peserta webinar has already been registered!",
                    },
                )
        # save to db
        pesertawebinarobj.create()
        result = pesertawebinar_schema.dump(pesertawebinarobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "pesertawebinar": result,
                "logged_in_as": current_user,
                "message": "Peserta webinar has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@pesertawebinar_routes.route("/all", methods=["GET", "OPTIONS"])
@jwt_required()
def get_pesertawebinars():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = PesertaWebinar.query.all()
    pesertawebinar_schema = PesertaWebinarSchema(
        many=True,
        only=[
            "idpeserta",
            "namapeserta",
            "hasilpelatihan",
            "training_id",
            "user_id",
            "created_at",
            "updated_at",
        ],
    )
    pesertawebinar = pesertawebinar_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"pesertawebinars": pesertawebinar})


@pesertawebinar_routes.route("/<int:user_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_specific_pesertawebinar(user_id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = PesertaWebinar.query.filter_by(user_id=user_id).all()
    pesertawebinar_schema = PesertaWebinarSchema(
        many=True,
        only=[
            "idpeserta",
            "namapeserta",
            "hasilpelatihan",
            "training_id",
            "user_id",
            "created_at",
            "updated_at",
        ],
    )
    pesertawebinar = pesertawebinar_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"pesertawebinar": pesertawebinar})


# UPDATE (U)

# DELETE (D)
