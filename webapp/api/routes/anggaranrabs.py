from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.AnggaranRAB import AnggaranRAB, AnggaranRABSchema
from webapp.api.utils.database import db
from werkzeug.utils import secure_filename
import os, random, string
from PIL import Image
from base64 import b64decode, decodebytes, b64encode

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

ANGGARANDIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "static", "anggaran", "rab")
)

anggaranrab_routes = Blueprint("anggaranrab_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@anggaranrab_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_anggaranrab():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        data = request.get_json()
        anggaranrab_schema = (
            AnggaranRABSchema()
        )  # anggaran rab schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        anggaranrab = anggaranrab_schema.load(data)
        # need validation in article creation process
        anggaranrabobj = AnggaranRAB(
            rabtitle=anggaranrab["rabtitle"],
            rabdesc=anggaranrab["rabdesc"],
            rabyear=anggaranrab["rabyear"],
            fileraburi=anggaranrab["fileraburi"],
            file=anggaranrab["file"],
        )
        filename = secure_filename(anggaranrabobj.fileraburi)
        anggaranrabobj.fileraburi = filename
        anggaranrabobj.author_id = anggaranrab["author_id"]
        xlsfile = b64decode(anggaranrabobj.file.split(",")[1] + "==")
        print(xlsfile)
        print(ANGGARANDIR)
        with open(ANGGARANDIR + "\\" + anggaranrabobj.fileraburi, "wb") as f:
            f.write(xlsfile)
        # save to db
        anggaranrabobj.create()
        result = anggaranrab_schema.dump(anggaranrabobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "anggaranrab": result,
                "logged_in_as": current_user,
                "message": "An RAB has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@anggaranrab_routes.route("/all", methods=["GET", "OPTIONS"])
@jwt_required()
def get_anggaranrab():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = AnggaranRAB.query.all()
    anggaranrab_schema = AnggaranRABSchema(
        many=True,
        only=[
            "idrab",
            "rabtitle",
            "rabdesc",
            "rabyear",
            "fileraburi",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    anggaranrabs = anggaranrab_schema.dump(fetch)
    descendingrabs = sorted(anggaranrabs, key=lambda x: x["idrab"], reverse=True)
    for x in descendingrabs:
        with open(ANGGARANDIR + "\\" + x['fileraburi'], "rb") as f:
            xlsencoded = b64encode(f.read())
            x['fileraburi'] = str(xlsencoded.decode("utf-8"))
    return response_with(resp.SUCCESS_200, value={"anggaranrab": descendingrabs})


@anggaranrab_routes.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_specific_anggaranrab(id):
    fetch = AnggaranRAB.query.get_or_404(id)
    anggaranrab_schema = AnggaranRABSchema(
        many=False,
        only=[
            "idrab",
            "rabtitle",
            "rabdesc",
            "rabyear",
            "fileraburi",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    anggaranrab = anggaranrab_schema.dump(fetch)
    with open(ANGGARANDIR + "\\" + anggaranrab['fileraburi'], "rb") as f:
        xlsencoded = b64encode(f.read())
        anggaranrab['fileraburi'] = str(xlsencoded.decode("utf-8"))
    return response_with(resp.SUCCESS_200, value={"anggaranrab": anggaranrab})


# UPDATE (U)

# DELETE (D)
