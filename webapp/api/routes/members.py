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
@member_routes.route("/create", methods=["POST"])
@jwt_required()
def create_member():
    try:
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
        memberobj.alamat=member["alamat"]
        memberobj.notelp=member["notelp"]
        memberobj.pekerjaan=member["pekerjaan"]
        memberobj.perusahaan=member["perusahaan"]
        memberobj.kantor=member["kantor"]
        memberobj.alamatkantor=member["alamatkantor"]
        memberobj.mulaibekerja=member["mulaibekerja"]
        memberobj.user_id=member["user_id"]
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
@member_routes.route("/all", methods=["GET"])
def get_members():
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


@member_routes.route("/<int:id>", methods=["GET"])
def get_specific_member(id):
    fetch = Member.query.get_or_404(id)
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
@member_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_member(id):
    try:
        current_user = get_jwt_identity()
        memberobj = Member.query.get_or_404(id)
        data = request.get_json()
        member_schema = MemberSchema()
        member = member_schema.load(data, partial=True)
        if member["validfrom"] is not None:
            memberobj.validfrom = member["validfrom"]
        if member["validthru"] is not None:
            memberobj.validthru = member["validthru"]
        if member["alamat"] is not None:
            memberobj.alamat = member["alamat"]
        if member["notelp"] is not None:
            memberobj.notelp = member["notelp"]
        if member["pekerjaan"] is not None:
            memberobj.pekerjaan = member["pekerjaan"]
        if member["perusahaan"] is not None:
            memberobj.perusahaan = member["perusahaan"]
        if member["kantor"] is not None:
            memberobj.kantor = member["kantor"]
        if member["alamatkantor"] is not None:
            memberobj.alamatkantor = member["alamatkantor"]
        if member["mulaibekerja"] is not None:
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