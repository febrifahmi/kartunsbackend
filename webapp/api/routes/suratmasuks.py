from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.SuratMasuks import SuratMasuk, SuratMasukSchema
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
    os.path.join(os.path.dirname(__file__), "..", "..", "static", "surat", "masuk")
)

suratmasuk_routes = Blueprint("suratmasuk_routes", __name__)


# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@suratmasuk_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_suratmasuk():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
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
            pengirim=suratmasuk["pengirim"],
            filesuraturi=suratmasuk["filesuraturi"],
            file=suratmasuk["file"],
        )
        # filename = secure_filename(suratmasukobj.filesuraturi)
        suratmasukobj.filesuraturi = (
            "suratmasuk_"
            + datetime.today().strftime("%Y%m%d")
            + "_"
            + getrandomstring(16)
            + ".pdf"
        )
        suratmasukobj.author_id = suratmasuk["author_id"]
        pdffile = b64decode(suratmasukobj.file.split(",")[1] + "==")
        print(pdffile)
        print(SURATDIR)
        with open(SURATDIR + "/" + suratmasukobj.filesuraturi, "wb") as f:
            f.write(pdffile)
        # save to db
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
@suratmasuk_routes.route("/all", methods=["GET", "OPTIONS"])
@jwt_required()
def get_suratmasuk():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = SuratMasuk.query.all()
    suratmasuk_schema = SuratMasukSchema(
        many=True,
        only=[
            "idsuratmasuk",
            "suratmasuktitle",
            "suratmasuknr",
            "filesuraturi",
            "suratmasukdesc",
            "pengirim",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    suratmasuks = suratmasuk_schema.dump(fetch)
    # for x in suratmasuks:
    #     with open(SURATDIR + "\\" + x["filesuraturi"], "rb") as f:
    #         pdfencoded = b64encode(f.read())
    #         x["filesuraturi"] = str(pdfencoded.decode("utf-8"))
    print("Surat Masuk: ", suratmasuks)
    return response_with(resp.SUCCESS_200, value={"suratmasuks": suratmasuks})


@suratmasuk_routes.route("/<int:id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_specific_suratmasuk(id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = SuratMasuk.query.get_or_404(id)
    suratmasuk_schema = SuratMasukSchema(
        many=False,
        only=[
            "idsuratmasuk",
            "suratmasuktitle",
            "suratmasuknr",
            "filesuraturi",
            "suratmasukdesc",
            "pengirim",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    suratmasuk = suratmasuk_schema.dump(fetch)
    # with open(SURATDIR + "\\" + suratmasuk["filesuraturi"], "rb") as f:
    #     pdfencoded = b64encode(f.read())
    #     suratmasuk["filesuraturi"] = str(pdfencoded.decode("utf-8"))
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
        if (
            "suratmasuktitle" in suratmasuk
            and suratmasuk["suratmasuktitle"] is not None
        ):
            if suratmasuk["suratmasuktitle"] != "":
                suratmasukobj.suratmasuktitle = suratmasuk["suratmasuktitle"]
        if "suratmasuknr" in suratmasuk and suratmasuk["suratmasuknr"] is not None:
            if suratmasuk["suratmasuknr"] != "":
                suratmasukobj.suratmasuknr = suratmasuk["suratmasuknr"]
        if "filesurat" in suratmasuk and suratmasuk["filesurat"] is not None:
            if suratmasuk["filesurat"] != "":
                suratmasukobj.filesurat = suratmasuk["filesurat"]
        if "suratmasukdesc" in suratmasuk and suratmasuk["suratmasukdesc"] is not None:
            if suratmasuk["suratmasukdesc"] != "":
                suratmasukobj.suratmasukdesc = suratmasuk["suratmasukdesc"]
        if "author_id" in suratmasuk and suratmasuk["author_id"] is not None:
            if suratmasuk["author_id"] != "":
                suratmasukobj.author_id = suratmasuk["author_id"]
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
        value={
            "logged_in_as": current_user,
            "message": "Surat masuk successfully deleted!",
        },
    )
