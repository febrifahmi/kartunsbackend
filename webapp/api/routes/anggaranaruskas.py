from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.AnggaranArusKas import AnggaranArusKas, AnggaranArusKasSchema
from webapp.api.utils.database import db
import os, random, string
from PIL import Image
from base64 import b64decode, decodebytes

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

ANGGARANDIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "static", "anggaran", "kas")
)

anggarankas_routes = Blueprint("anggarankas_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@anggarankas_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_anggarankas():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        data = request.get_json()
        anggarankas_schema = (
            AnggaranArusKasSchema()
        )  # anggaran rab schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        anggarankas = anggarankas_schema.load(data)
        # need validation in article creation process
        anggarankasobj = AnggaranArusKas(
            aruskastitle=anggarankas["aruskastitle"],
            aruskasdesc=anggarankas["aruskasdesc"],
            aruskasmonth=anggarankas["aruskasmonth"],
            aruskasyear=anggarankas["aruskasyear"],
            filekasuri=anggarankas["filekasuri"],
            file=anggarankas["file"],
        )
        anggarankasobj.author_id = anggarankas["author_id"]
        xlsfile = b64decode(anggarankasobj.file.split(",")[1] + "==")
        print(xlsfile)
        print(ANGGARANDIR)
        with open(ANGGARANDIR + "\\" + anggarankasobj.filekasuri, "wb") as f:
            f.write(xlsfile)
        # save to db
        anggarankasobj.create()
        result = anggarankas_schema.dump(anggarankasobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "anggarankas": result,
                "logged_in_as": current_user,
                "message": "A Kas has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@anggarankas_routes.route("/all", methods=["GET", "OPTIONS"])
@jwt_required()
def get_anggarankas():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = AnggaranArusKas.query.all()
    anggarankas_schema = AnggaranArusKasSchema(
        many=True,
        only=[
            "idaruskas",
            "aruskastitle",
            "aruskasdesc",
            "aruskasmonth",
            "aruskasyear",
            "filekasuri",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    anggarankas = anggarankas_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"anggarankas": anggarankas})


@anggarankas_routes.route("/<int:id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_specific_anggarankas(id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = AnggaranArusKas.query.get_or_404(id)
    anggarankas_schema = AnggaranArusKasSchema(
        many=False,
        only=[
            "idaruskas",
            "aruskastitle",
            "aruskasdesc",
            "aruskasmonth",
            "aruskasyear",
            "filekasuri",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    anggarankas = anggarankas_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"anggarankas": anggarankas})


# UPDATE (U)

# DELETE (D)
