from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Letters import Letter, LetterSchema
from webapp.api.utils.database import db
from webapp import qrcode

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

letter_routes = Blueprint("letter_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@letter_routes.route("/create", methods=["POST"])
@jwt_required()
def create_letter():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        letter_schema = (
            LetterSchema()
        )  # letter schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        letter = letter_schema.load(data)
        # need validation in ad creation process
        letterobj = Letter(
            lettertitle=letter["lettertitle"],
            letternr=letter["letternr"],
            letterdesc=letter["letterdesc"],
            lettertext=letter["lettertext"],
            lampiran=letter["lampiran"],
            kota=letter["kota"],
            kepada=letter["kepada"],
        )
        letterobj.setQRcodeString(current_user + "_" + "_" + letterobj.letternr)
        letterobj.create()
        result = letter_schema.dump(letterobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "letter": result,
                "logged_in_as": current_user,
                "message": "A letter has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@letter_routes.route("/all", methods=["GET"])
@jwt_required()
def get_letters():
    fetch = Letter.query.all()
    letter_schema = LetterSchema(
        many=True,
        only=[
            "idletter",
            "lettertitle",
            "letternr",
            "qrcodestring",
            "letterdesc",
            "lettertext",
            "lampiran",
            "kota",
            "kepada",
            "created_at",
            "updated_at",
            "penandatangan_id",
        ],
    )
    letters = letter_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"letters": letters})


@letter_routes.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_specific_letter(id):
    fetch = Letter.query.get_or_404(id)
    letter_schema = LetterSchema(
        many=False,
        only=[
            "idletter",
            "lettertitle",
            "letternr",
            "qrcodestring",
            "letterdesc",
            "lettertext",
            "lampiran",
            "kota",
            "kepada",
            "created_at",
            "updated_at",
            "penandatangan_id",
        ],
    )
    letter = letter_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"letter": letter})


# UPDATE (U)
@letter_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_letter(id):
    try:
        current_user = get_jwt_identity()
        letterobj = Letter.query.get_or_404(id)
        data = request.get_json()
        letter_schema = LetterSchema()
        letter = letter_schema.load(data, partial=True)
        if "lettertitle" in letter and letter["lettertitle"] is not None:
            if letter["lettertitle"] != "":
                letterobj.lettertitle = letter["lettertitle"]
        if "letternr" in letter and letter["letternr"] is not None:
            if letter["letternr"] != "":
                letterobj.letternr = letter["letternr"]
        if "qrcodestring" in letter and letter["qrcodestring"] is not None:
            if letter["qrcodestring"] != "":
                letterobj.qrcodestring = letter["qrcodestring"]
        if "letterdesc" in letter and letter["letterdesc"] is not None:
            if letter["letterdesc"] != "":
                letterobj.letterdesc = letter["letterdesc"]
        if "lettertext" in letter and letter["lettertext"] is not None:
            if letter["lettertext"] != "":
                letterobj.lettertext = letter["lettertext"]
        if "lampiran" in letter and letter["lampiran"] is not None:
            if letter["lampiran"] != "":
                letterobj.lampiran = letter["lampiran"]
        if "kota" in letter and letter["kota"] is not None:
            if letter["kota"] != "":
                letterobj.kota = letter["kota"]
        if "kepada" in letter and letter["kepada"] is not None:
            if letter["kepada"] != "":
                letterobj.kepada = letter["kepada"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "letter": letter,
                "logged_in_as": current_user,
                "message": "Letter details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@letter_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_letter(id):
    current_user = get_jwt_identity()
    letterobj = Letter.query.get_or_404(id)
    db.session.delete(letterobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "Letter successfully deleted!"},
    )
