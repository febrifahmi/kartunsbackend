from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Announcements import Pengumuman, PengumumanSchema
from webapp.api.utils.database import db
from werkzeug.utils import secure_filename
import os, random, string
from PIL import Image
from base64 import b64decode, decodebytes

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

UPLOADDIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "static", "uploads")
)

pengumuman_routes = Blueprint("pengumuman_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@pengumuman_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_pengumuman():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        data = request.get_json()
        pengumuman_schema = (
            PengumumanSchema()
        )  # ad schema pertama didefinisikan full utk menerima seluruh data yang diperlukan termasuk password
        pengumuman = pengumuman_schema.load(data)
        # need validation in ad creation process
        pengumumanobj = Pengumuman(
            judul=pengumuman["judul"],
            pengumumanimgurl=pengumuman["pengumumanimgurl"],
            pengumumandesc=pengumuman["pengumumandesc"],
            pengumumantext=pengumuman["pengumumantext"],
            file=pengumuman["file"],
        )
        filename = secure_filename(pengumumanobj.pengumumanimgurl)
        pengumumanobj.pengumumanimgurl = filename
        pengumumanobj.author_id = pengumuman["author_id"]
        imgfile = b64decode(pengumumanobj.file.split(",")[1] + "==")
        print(imgfile)
        print(UPLOADDIR)
        with open(UPLOADDIR + "/" + pengumumanobj.pengumumanimgurl, "wb") as f:
            f.write(imgfile)
        # save to db
        pengumumanobj.create()
        result = pengumuman_schema.dump(pengumumanobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "pengumuman": result,
                "logged_in_as": current_user,
                "message": "An announcement has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@pengumuman_routes.route("/all", methods=["GET", "OPTIONS"])
def get_pengumuman():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = Pengumuman.query.all()
    pengumuman_schema = PengumumanSchema(
        many=True,
        only=[
            "idpengumuman",
            "judul",
            "pengumumanimgurl",
            "pengumumandesc",
            "pengumumantext",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    pengumuman = pengumuman_schema.dump(fetch)
    descendingpengumuman = sorted(pengumuman, key=lambda x: x["idpengumuman"], reverse=True)
    return response_with(resp.SUCCESS_200, value={"pengumumans": descendingpengumuman})


@pengumuman_routes.route("/<int:id>", methods=["GET", "OPTIONS"])
def get_specific_agenda(id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = Pengumuman.query.get_or_404(id)
    pengumuman_schema = PengumumanSchema(
        many=False,
        only=[
            "idpengumuman",
            "judul",
            "pengumumanimgurl",
            "pengumumandesc",
            "pengumumantext",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    pengumuman = pengumuman_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"pengumuman": pengumuman})


# UPDATE (U)
@pengumuman_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_pengumuman(id):
    try:
        current_user = get_jwt_identity()
        pengumumanobj = Pengumuman.query.get_or_404(id)
        data = request.get_json()
        pengumuman_schema = PengumumanSchema()
        pengumuman = pengumuman_schema.load(data, partial=True)
        if "judul" in pengumuman and pengumuman["judul"] is not None:
            if pengumuman["judul"] != "":
                pengumumanobj.judul = pengumuman["judul"]
        if (
            "pengumumanimgurl" in pengumuman
            and pengumuman["pengumumanimgurl"] is not None
        ):
            if pengumuman["pengumumanimgurl"] != "":
                pengumumanobj.pengumumanimgurl = pengumuman["pengumumanimgurl"]
        if "pengumumandesc" in pengumuman and pengumuman["pengumumandesc"] is not None:
            if pengumuman["pengumumandesc"] != "":
                pengumumanobj.pengumumandesc = pengumuman["pengumumandesc"]
        if "pengumumantext" in pengumuman and pengumuman["pengumumantext"] is not None:
            if pengumuman["pengumumantext"] != "":
                pengumumanobj.pengumumantext = pengumuman["pengumumantext"]
        if "author_id" in pengumuman and pengumuman["author_id"] is not None:
            if pengumuman["author_id"] != "":
                pengumumanobj.author_id = pengumuman["author_id"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "pengumuman": pengumuman,
                "logged_in_as": current_user,
                "message": "Pengumuman details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@pengumuman_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_pengumuman(id):
    current_user = get_jwt_identity()
    pengumumanobj = Pengumuman.query.get_or_404(id)
    db.session.delete(pengumumanobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={
            "logged_in_as": current_user,
            "message": "Pengumuman successfully deleted!",
        },
    )
