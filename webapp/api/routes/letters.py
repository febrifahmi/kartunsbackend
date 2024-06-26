from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Letters import Letter, LetterSchema
from webapp.api.utils.database import db
from webapp.api.utils.utility import getrandomstring
from werkzeug.utils import secure_filename
from webapp import qrcode
import os, random, string
from base64 import b64decode, decodebytes, b64encode

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta, datetime

SURATDIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "static", "surat", "keluar")
)

letter_routes = Blueprint("letter_routes", __name__)


# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@letter_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_letter():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        data = request.get_json()
        letter_schema = (
            LetterSchema()
        )  # letter schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        letter = letter_schema.load(data)
        # need validation in ad creation process
        letterobj = Letter(
            suratkeluartitle=letter["suratkeluartitle"],
            suratkeluarnr=letter["suratkeluarnr"],
            suratkeluardesc=letter["suratkeluardesc"],
            kepada=letter["kepada"],
            filesuratkeluaruri=letter["filesuratkeluaruri"],
            file=letter["file"],
        )
        # filename = secure_filename(letterobj.filesuratkeluaruri)
        letterobj.filesuratkeluaruri = (
            "suratkeluar_"
            + datetime.today().strftime("%Y%m%d")
            + "_"
            + getrandomstring(16)
            + ".pdf"
        )
        letterobj.author_id = letter["author_id"]
        pdffile = b64decode(letterobj.file.split(",")[1] + "==")
        print(pdffile)
        print(SURATDIR)
        with open(SURATDIR + "\\" + letterobj.filesuratkeluaruri, "wb") as f:
            f.write(pdffile)
        # save to db
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
@letter_routes.route("/all", methods=["GET", "OPTIONS"])
@jwt_required()
def get_letters():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = Letter.query.all()
    letter_schema = LetterSchema(
        many=True,
        only=[
            "idsuratkeluar",
            "suratkeluartitle",
            "suratkeluarnr",
            "suratkeluardesc",
            "kepada",
            "filesuratkeluaruri",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    letters = letter_schema.dump(fetch)
    # for x in letters:
    #     with open(SURATDIR + "/" + x["filesuratkeluaruri"], "rb") as f:
    #         pdfencoded = b64encode(f.read())
    #         x["filesuratkeluaruri"] = str(pdfencoded.decode("utf-8"))
    # print("Letters: ",letters)
    return response_with(resp.SUCCESS_200, value={"letters": letters})


@letter_routes.route("/<int:id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_specific_letter(id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = Letter.query.get_or_404(id)
    letter_schema = LetterSchema(
        many=False,
        only=[
            "idsuratkeluar",
            "suratkeluartitle",
            "suratkeluarnr",
            "suratkeluardesc",
            "kepada",
            "filesuratkeluaruri",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    letter = letter_schema.dump(fetch)
    # with open(SURATDIR + "\\" + letter["filesuratkeluaruri"], "rb") as f:
    #     pdfencoded = b64encode(f.read())
    #     letter["filesuratkeluaruri"] = str(pdfencoded.decode("utf-8"))
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
        if "author_id" in letter and letter["author_id"] is not None:
            if letter["author_id"] != "":
                letterobj.author_id = letter["author_id"]
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
