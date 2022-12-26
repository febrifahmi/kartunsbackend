from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.SuratMasuks import SuratMasuk, SuratMasukSchema
from webapp.api.utils.database import db
from webapp import qrcode

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

suratmasuk_routes = Blueprint("suratmasuk_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@suratmasuk_routes.route("/create", methods=["POST"])
@jwt_required()
def create_suratmasuk():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        suratmasuk_schema = (
            SuratMasukSchema()
        )  # suratmasuk schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        suratmasuk = suratmasuk_schema.load(data)
        # need validation in ad creation process
        suratmasukobj = SuratMasuk(
            suratmasuktitle=suratmasuk["suratmasuktitle"],
            suratmasuknr=suratmasuk["suratmasuknr"],
            suratmasukdesc=suratmasuk["suratmasukdesc"],
            filesurat=suratmasuk["filesurat"],
        )
        suratmasukobj.create()
        result = suratmasuk_schema.dump(suratmasukobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "suratmasuk": result,
                "logged_in_as": current_user,
                "message": "Surat masuk has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@suratmasuk_routes.route("/all", methods=["GET"])
@jwt_required()
def get_suratmasuk():
    fetch = SuratMasuk.query.all()
    suratmasuk_schema = SuratMasukSchema(
        many=True,
        only=[
            "idsuratmasuk",
            "suratmasuktitle",
            "suratmasuknr",
            "filesurat",
            "suratmasukdesc",
            "created_at",
            "updated_at",
        ],
    )
    suratmasuks = suratmasuk_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"suratmasuks": suratmasuks})


@suratmasuk_routes.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_specific_suratmasuk(id):
    fetch = SuratMasuk.query.get_or_404(id)
    suratmasuk_schema = SuratMasukSchema(
        many=False,
        only=[
            "idsuratmasuk",
            "suratmasuktitle",
            "suratmasuknr",
            "filesurat",
            "suratmasukdesc",
            "created_at",
            "updated_at",
        ],
    )
    suratmasuk = suratmasuk_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"suratmasuk": suratmasuk})


# UPDATE (U)
@suratmasuk_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_suratmasuk(id):
    try:
        current_user = get_jwt_identity()
        suratmasukobj = SuratMasuk.query.get_or_404(id)
        data = request.get_json()
        suratmasuk_schema = SuratMasukSchema()
        suratmasuk = suratmasuk_schema.load(data, partial=True)
        if suratmasuk["suratmasuktitle"] is not None:
            suratmasukobj.suratmasuktitle = suratmasuk["suratmasuktitle"]
        if suratmasuk["suratmasuknr"] is not None:
            suratmasukobj.suratmasuknr = suratmasuk["suratmasuknr"]
        if suratmasuk["filesurat"] is not None:
            suratmasukobj.filesurat = suratmasuk["filesurat"]
        if suratmasuk["suratmasukdesc"] is not None:
            suratmasukobj.suratmasukdesc = suratmasuk["suratmasukdesc"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "suratmasuk": suratmasuk,
                "logged_in_as": current_user,
                "message": "Surat masuk details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@suratmasuk_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_suratmasuk(id):
    current_user = get_jwt_identity()
    suratmasukobj = SuratMasuk.query.get_or_404(id)
    db.session.delete(suratmasukobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "Surat masuk successfully deleted!"},
    )
