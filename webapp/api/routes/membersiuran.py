from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.MembersIuran import IuranMember, IuranMemberSchema
from webapp.api.utils.database import db
from werkzeug.utils import secure_filename
import os, random, string
from PIL import Image
from base64 import b64decode, decodebytes

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

iuranmember_routes = Blueprint("iuranmember_routes", __name__)

IURANDIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "static", "iuranmember")
)


# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@iuranmember_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_iuranmember():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        data = request.get_json()
        iuranmember_schema = (
            IuranMemberSchema()
        )  # iuran member schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        iuranmember = iuranmember_schema.load(data)
        # need validation in iuran member creation process
        filename = secure_filename(iuranmember["iuranimgurl"])
        iuranmemberobj = IuranMember(
            nomoranggota=iuranmember["nomoranggota"],
            namaanggota=iuranmember["namaanggota"],
            tahun=iuranmember["tahun"],
            jumlahiuran=iuranmember["jumlahiuran"],
            bankpengirim=iuranmember["bankpengirim"],
            iuranimgurl=filename,
            member_id=iuranmember["member_id"],
            user_id=iuranmember["user_id"],
            file=iuranmember["file"],
        )
        imgfile = b64decode(iuranmemberobj.file.split(",")[1] + "==")
        print(imgfile)
        print(IURANDIR)
        with open(IURANDIR + "/" + iuranmemberobj.iuranimgurl, "wb") as f:
            f.write(imgfile)
        # save to db
        iuranmemberobj.create()
        result = iuranmember_schema.dump(iuranmemberobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "iuranmember": result,
                "logged_in_as": current_user,
                "message": "An iuran member has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@iuranmember_routes.route("/all", methods=["GET", "OPTIONS"])
@jwt_required()
def get_iuranmembers():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = IuranMember.query.all()
    iuranmember_schema = IuranMemberSchema(
        many=True,
        only=[
            "idiuran",
            "nomoranggota",
            "namaanggota",
            "tahun",
            "jumlahiuran",
            "bankpengirim",
            "iuranimgurl",
            "member_id",
            "user_id",
            "created_at",
        ],
    )
    iuranmembers = iuranmember_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"iuranmembers": iuranmembers})


@iuranmember_routes.route("/<int:user_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_specific_iuranmember(user_id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = IuranMember.query.filter_by(user_id=user_id).all()
    iuranmember_schema = IuranMemberSchema(
        many=True,
        only=[
            "idiuran",
            "nomoranggota",
            "namaanggota",
            "tahun",
            "jumlahiuran",
            "bankpengirim",
            "iuranimgurl",
            "member_id",
            "user_id",
            "created_at",
        ],
    )
    iuranmember = iuranmember_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"iuranmember": iuranmember})


# UPDATE


# DELETE
