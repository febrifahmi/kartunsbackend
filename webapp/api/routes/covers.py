from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Covers import Cover, CoverSchema
from webapp.api.utils.database import db
from werkzeug.utils import secure_filename
import os, random, string
from flask import current_app
from PIL import Image
from base64 import b64decode, decodebytes
import io

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

UPLOADDIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","..","static","uploads"))

cover_routes = Blueprint("cover_routes", __name__)


# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@cover_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_cover():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        data = request.get_json()
        cover_schema = (
            CoverSchema()
        )  # ad schema pertama didefinisikan full utk menerima seluruh data yang diperlukan termasuk password
        cover = cover_schema.load(data)
        # need validation in ad creation process
        coverobj = Cover(
            covertitle=cover["covertitle"],
            coverdesc=cover["coverdesc"],
            covertext=cover["covertext"],
            coverimgurl=cover["coverimgurl"],
            file=cover["file"]
        )
        filename = secure_filename(coverobj.coverimgurl)
        coverobj.coverimgurl = filename
        coverobj.author_id = cover["author_id"]
        imgfile = b64decode(coverobj.file.split(",")[1] + '==')
        print(imgfile)
        print(UPLOADDIR)
        with open(UPLOADDIR + "/" + coverobj.coverimgurl, "wb") as f:
            f.write(imgfile)
        # save to db
        coverobj.create()
        # cek apakah file yang diupload sesuai daftar jenis file yg diijinkan
        result = cover_schema.dump(coverobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "cover": result,
                "logged_in_as": current_user,
                "message": "A cover has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@cover_routes.route("/all", methods=["GET", "OPTIONS"])
def get_covers():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = Cover.query.all()
    cover_schema = CoverSchema(
        many=True,
        only=[
            "idcover",
            "covertitle",
            "coverimgurl",
            "coverdesc",
            "covertext",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    covers = cover_schema.dump(fetch)
    descendingcovers = sorted(covers, key=lambda x: x["idcover"], reverse=True)
    return response_with(resp.SUCCESS_200, value={"covers": descendingcovers})


@cover_routes.route("/<int:id>", methods=["GET", "OPTIONS"])
def get_specific_cover(id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = Cover.query.get_or_404(id)
    cover_schema = CoverSchema(
        many=False,
        only=[
            "idcover",
            "covertitle",
            "coverimgurl",
            "coverdesc",
            "covertext",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    cover = cover_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"cover": cover})


# UPDATE (U)
@cover_routes.route("/update/<int:id>", methods=["PUT", "OPTIONS"])
@jwt_required()
def update_cover(id):
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        coverobj = Cover.query.get_or_404(id)
        data = request.get_json()
        cover_schema = CoverSchema()
        cover = cover_schema.load(data, partial=True)
        if "covertitle" in cover and cover["covertitle"] is not None:
            if cover["covertitle"] != "":
                coverobj.covertitle = cover["covertitle"]
        if "coverimgurl" in cover and cover["coverimgurl"] is not None:
            if cover["coverimgurl"] != "":
                coverobj.coverimgurl = cover["coverimgurl"]
        if "coverdesc" in cover and cover["coverdesc"] is not None:
            if cover["coverdesc"] != "":
                coverobj.coverdesc = cover["coverdesc"]
        if "covertext" in cover and cover["covertext"] is not None:
            if cover["covertext"] != "":
                coverobj.covertext = cover["covertext"]
        if "author_id" in cover and cover["author_id"] is not None:
            if cover["author_id"] != "":
                coverobj.author_id = cover["author_id"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "cover": cover,
                "logged_in_as": current_user,
                "message": "Cover details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@cover_routes.route("/delete/<int:id>", methods=["DELETE", "OPTIONS"])
@jwt_required()
def delete_cover(id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    current_user = get_jwt_identity()
    coverobj = Cover.query.get_or_404(id)
    db.session.delete(coverobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={
            "logged_in_as": current_user,
            "message": "A cover successfully deleted!",
        },
    )
