from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Members import Member, MemberSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

member_routes = Blueprint("member_routes", __name__)


# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@member_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_member():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        data = request.get_json()
        member_schema = (
            MemberSchema()
        )  # member schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        member = member_schema.load(data)
        # need validation in member creation process
        memberobj = Member(
            nomoranggota=member["nomoranggota"],
            validfrom=member["validfrom"],
            validthru=member["validthru"],
        )
        memberobj.alamat = member["alamat"]
        memberobj.notelp = member["notelp"]
        memberobj.pekerjaan = member["pekerjaan"]
        memberobj.perusahaan = member["perusahaan"]
        memberobj.kantor = member["kantor"]
        memberobj.alamatkantor = member["alamatkantor"]
        memberobj.mulaibekerja = member["mulaibekerja"]
        memberobj.user_id = member["user_id"]
        memberobj.create()
        result = member_schema.dump(memberobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "member": result,
                "logged_in_as": current_user,
                "message": "A member has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@member_routes.route("/all", methods=["GET", "OPTIONS"])
@jwt_required()
def get_members():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = Member.query.all()
    member_schema = MemberSchema(
        many=True,
        only=[
            "idmember",
            "nomoranggota",
            "validfrom",
            "validthru",
            "alamat",
            "notelp",
            "pekerjaan",
            "perusahaan",
            "kantor",
            "alamatkantor",
            "mulaibekerja",
            "user_id",
        ],
    )
    members = member_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"members": members})


@member_routes.route("/<int:user_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_specific_member(user_id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = Member.query.filter_by(user_id=user_id).first_or_404()
    member_schema = MemberSchema(
        many=False,
        only=[
            "idmember",
            "nomoranggota",
            "validfrom",
            "validthru",
            "alamat",
            "notelp",
            "pekerjaan",
            "perusahaan",
            "kantor",
            "alamatkantor",
            "mulaibekerja",
            "user_id",
        ],
    )
    member = member_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"member": member})


# UPDATE (U)
@member_routes.route("/update/<int:id>", methods=["PUT", "OPTIONS"])
@jwt_required()
def update_member(id):
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        memberobj = Member.query.get_or_404(id)
        data = request.get_json()
        member_schema = MemberSchema()
        member = member_schema.load(data, partial=True)
        if "validfrom" in member and member["validfrom"] is not None:
            if member["validfrom"] != "":
                memberobj.validfrom = member["validfrom"]
        if "validthru" in member and member["validthru"] is not None:
            if member["validthru"] != "":
                memberobj.validthru = member["validthru"]
        if "alamat" in member and member["alamat"] is not None:
            if member["alamat"] != "":
                memberobj.alamat = member["alamat"]
        if "notelp" in member and member["notelp"] is not None:
            if member["notelp"] != "":
                memberobj.notelp = member["notelp"]
        if "pekerjaan" in member and member["pekerjaan"] is not None:
            if member["pekerjaan"] != "":
                memberobj.pekerjaan = member["pekerjaan"]
        if "perusahaan" in member and member["perusahaan"] is not None:
            if member["perusahaan"] != "":
                memberobj.perusahaan = member["perusahaan"]
        if "kantor" in member and member["kantor"] is not None:
            if member["kantor"] != "":
                memberobj.kantor = member["kantor"]
        if "alamatkantor" in member and member["alamatkantor"] is not None:
            if member["alamatkantor"] != "":
                memberobj.alamatkantor = member["alamatkantor"]
        if "mulaibekerja" in member and member["mulaibekerja"] is not None:
            if member["mulaibekerja"] != "":
                memberobj.mulaibekerja = member["mulaibekerja"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "member": member,
                "logged_in_as": current_user,
                "message": "Member details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@member_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_member(id):
    current_user = get_jwt_identity()
    memberobj = Member.query.get_or_404(id)
    db.session.delete(memberobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "Member successfully deleted!"},
    )
