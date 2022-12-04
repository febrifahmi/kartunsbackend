from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Commitee import Pengurus, PengurusSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

pengurus_routes = Blueprint("pengurus_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@pengurus_routes.route("/create", methods=["POST"])
@jwt_required()
def create_pengurus():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        pengurus_schema = (
            PengurusSchema()
        )  # ad schema pertama didefinisikan full utk menerima seluruh data yang diperlukan termasuk password
        pengurus = pengurus_schema.load(data)
        # need validation in ad creation process
        pengurusobj = Pengurus(
            namapengurus=pengurus["namapengurus"],
            jabatan=pengurus["jabatan"],
            tahunkepengurusan=pengurus["tahunkepengurusan"],
            tanggalmulai=pengurus["tanggalmulai"],
            tanggalselesai=pengurus["tanggalselesai"],
            pengurus_id=pengurus["pengurus_id"]
        )
        result = pengurus_schema.dump(pengurusobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "pengurus": result,
                "logged_in_as": current_user,
                "message": "Pengurus has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@pengurus_routes.route("/all", methods=["GET"])
def get_pengurus():
    fetch = Pengurus.query.all()
    pengurus_schema = PengurusSchema(
        many=True,
        only=[
            "idpengurus",
            "namapengurus",
            "jabatan",
            "tahunkepengurusan",
            "tanggalmulai",
            "tanggalselesai",
            "created_at",
            "updated_at",
            "pengurus_id",
        ],
    )
    pengurus = pengurus_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"pengurus": pengurus})


@pengurus_routes.route("/<int:id>", methods=["GET"])
def get_specific_pengurus(id):
    fetch = Pengurus.query.get_or_404(id)
    pengurus_schema = PengurusSchema(
        many=False,
        only=[
            "idpengurus",
            "namapengurus",
            "jabatan",
            "tahunkepengurusan",
            "tanggalmulai",
            "tanggalselesai",
            "created_at",
            "updated_at",
            "pengurus_id",
        ],
    )
    pengurus = pengurus_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"pengurus": pengurus})


# UPDATE (U)
@pengurus_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_pengurus(id):
    try:
        current_user = get_jwt_identity()
        pengurusobj = Pengurus.query.get_or_404(id)
        data = request.get_json()
        pengurus_schema = PengurusSchema()
        pengurus = pengurus_schema.load(data, partial=True)
        if pengurus["namapengurus"] is not None:
            pengurusobj.namapengurus = pengurus["namapengurus"]
        if pengurus["jabatan"] is not None:
            pengurusobj.jabatan = pengurus["jabatan"]
        if pengurus["tahunkepengurusan"] is not None:
            pengurusobj.tahunkepengurusan = pengurus["tahunkepengurusan"]
        if pengurus["tanggalmulai"] is not None:
            pengurusobj.tanggalmulai = pengurus["tanggalmulai"]
        if pengurus["tanggalselesai"] is not None:
            pengurusobj.tanggalselesai = pengurus["tanggalselesai"]
        if pengurus["pengurus_id"] is not None:
            pengurusobj.pengurus_id = pengurus["pengurus_id"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "pengurus": pengurus,
                "logged_in_as": current_user,
                "message": "Pengurus details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
