from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.PengajuanBeasiswa import (
    PengajuanBeasiswa,
    PengajuanBeasiswaSchema,
)
from webapp.api.utils.database import db
from webapp.api.utils.utility import getrandomstring
from werkzeug.utils import secure_filename
import os, random, string
from PIL import Image
from base64 import b64decode, decodebytes

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta, datetime

pengajuanbeasiswa_routes = Blueprint("pengajuanbeasiswa_routes", __name__)

BERKASBEASISWADIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "static", "berkasbeasiswa")
)


# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@pengajuanbeasiswa_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_pengajuanbeasiswa():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        data = request.get_json()
        pengajuanbeasiswa_schema = (
            PengajuanBeasiswaSchema()
        )  # pengajuan schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        pengajuanbeasiswa = pengajuanbeasiswa_schema.load(data)
        # need validation in pengajuan beasiswa creation process
        pengajuanbeasiswaobj = PengajuanBeasiswa(
            namamahasiswa=pengajuanbeasiswa["namamahasiswa"],
            batchbeasiswa=pengajuanbeasiswa["batchbeasiswa"],
            dokproposalbsw=pengajuanbeasiswa["dokproposalbsw"],
            dokcv=pengajuanbeasiswa["dokcv"],
            dokportofolio=pengajuanbeasiswa["dokportofolio"],
            fileproposalbsw=pengajuanbeasiswa["fileproposalbsw"],
            filecv=pengajuanbeasiswa["filecv"],
            fileportofolio=pengajuanbeasiswa["fileportofolio"],
            user_id=pengajuanbeasiswa["user_id"],
        )
        # filename1 = secure_filename(pengajuanbeasiswaobj.fileproposalbsw)
        pengajuanbeasiswaobj.dokproposalbsw = (
            "proposalbsw_usr"
            + str(pengajuanbeasiswaobj.user_id)
            + "_"
            + datetime.today().strftime("%Y%m%d")
            + "_"
            + getrandomstring(16)
            + ".pdf"
        )
        pengajuanbeasiswaobj.dokcv = (
            "cv_usr"
            + str(pengajuanbeasiswaobj.user_id)
            + "_"
            + datetime.today().strftime("%Y%m%d")
            + "_"
            + getrandomstring(16)
            + ".pdf"
        )
        pengajuanbeasiswaobj.dokportofolio = (
            "portofolio_usr"
            + str(pengajuanbeasiswaobj.user_id)
            + "_"
            + datetime.today().strftime("%Y%m%d")
            + "_"
            + getrandomstring(16)
            + ".pdf"
        )
        pdffile1 = b64decode(pengajuanbeasiswaobj.fileproposalbsw.split(",")[1] + "==")
        print(pdffile1)
        # print(BERKASBEASISWADIR)
        with open(
            BERKASBEASISWADIR + "/" + pengajuanbeasiswaobj.dokproposalbsw, "wb"
        ) as f:
            f.write(pdffile1)
        pdffile2 = b64decode(pengajuanbeasiswaobj.filecv.split(",")[1] + "==")
        print(pdffile2)
        with open(BERKASBEASISWADIR + "/" + pengajuanbeasiswaobj.dokcv, "wb") as f:
            f.write(pdffile2)
        pdffile3 = b64decode(pengajuanbeasiswaobj.fileportofolio.split(",")[1] + "==")
        print(pdffile3)
        with open(
            BERKASBEASISWADIR + "/" + pengajuanbeasiswaobj.dokportofolio, "wb"
        ) as f:
            f.write(pdffile3)
        # save to db
        pengajuanbeasiswaobj.create()
        result = pengajuanbeasiswa_schema.dump(pengajuanbeasiswaobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "pengajuanbeasiswa": result,
                "logged_in_as": current_user,
                "message": "Pengajuan beasiswa has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@pengajuanbeasiswa_routes.route("/all", methods=["GET", "OPTIONS"])
@jwt_required()
def get_pengajuanbeasiswa():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = PengajuanBeasiswa.query.all()
    pengajuanbeasiswa_schema = PengajuanBeasiswaSchema(
        many=True,
        only=[
            "idpengajuan",
            "namamahasiswa",
            "batchbeasiswa",
            "dokproposalbsw",
            "dokcv",
            "dokportofolio",
            "hasilseleksiakhir",
            "user_id",
            "created_at",
            "updated_at",
        ],
    )
    pengajuanbeasiswa = pengajuanbeasiswa_schema.dump(fetch)
    return response_with(
        resp.SUCCESS_200, value={"pengajuanbeasiswas": pengajuanbeasiswa}
    )


@pengajuanbeasiswa_routes.route("/<int:user_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_specific_pengajuanbeasiswa(user_id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = PengajuanBeasiswa.query.filter_by(user_id=user_id).all()
    pengajuanbeasiswa_schema = PengajuanBeasiswaSchema(
        many=True,
        only=[
            "idpengajuan",
            "namamahasiswa",
            "batchbeasiswa",
            "dokproposalbsw",
            "dokcv",
            "dokportofolio",
            "hasilseleksiakhir",
            "user_id",
            "created_at",
            "updated_at",
        ],
    )
    pengajuanbeasiswa = pengajuanbeasiswa_schema.dump(fetch)
    return response_with(
        resp.SUCCESS_200, value={"pengajuanbeasiswa": pengajuanbeasiswa}
    )
