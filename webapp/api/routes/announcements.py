from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Announcements import Pengumuman, PengumumanSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

pengumuman_routes = Blueprint("pengumuman_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@pengumuman_routes.route("/create", methods=["POST"])
@jwt_required()
def create_pengumuman():
    try:
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
        )
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
@pengumuman_routes.route("/all", methods=["GET"])
def get_pengumuman():
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
        ],
    )
    pengumuman = pengumuman_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"pengumuman": pengumuman})


@pengumuman_routes.route("/<int:id>", methods=["GET"])
def get_specific_agenda(id):
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
        if "pengumumanimgurl" in pengumuman and pengumuman["pengumumanimgurl"] is not None:
            if pengumuman["pengumumanimgurl"] != "":
                pengumumanobj.pengumumanimgurl = pengumuman["pengumumanimgurl"]
        if "pengumumandesc" in pengumuman and pengumuman["pengumumandesc"] is not None:
            if pengumuman["pengumumandesc"] != "":
                pengumumanobj.pengumumandesc = pengumuman["pengumumandesc"]
        if "pengumumantext" in pengumuman and pengumuman["pengumumantext"] is not None:
            if pengumuman["pengumumantext"] != "":
                pengumumanobj.pengumumantext = pengumuman["pengumumantext"]
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
        value={"logged_in_as": current_user, "message": "Pengumuman successfully deleted!"},
    )


