from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Donations import Donations, DonationsSchema
from webapp.api.utils.database import db
import os, random, string
from base64 import b64decode, decodebytes

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

UPLOADDIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","..","static","uploads"))

donations_routes = Blueprint("donation_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@donations_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_donation():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        data = request.get_json()
        donation_schema = (
            DonationsSchema()
        )  # ad schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        donation = donation_schema.load(data)
        # need validation in creation process
        donationobj = Donations(
            namadonatur=donation["namadonatur"],
            bankpengirim=donation["bankpengirim"],
            jumlahdonasi=donation["jumlahdonasi"],
            rektujuan=donation["rektujuan"],
            donasiimgurl=donation["donasiimgurl"],
            donatur_id=donation["donatur_id"],
            file=donation["file"],
        )
        imgfile = b64decode(donationobj.file.split(",")[1] + '==')
        print(imgfile)
        print(UPLOADDIR)
        with open(UPLOADDIR + "\\" + donationobj.donasiimgurl, "wb") as f:
            f.write(imgfile)
        # save to db
        donationobj.create()
        result = donation_schema.dump(donationobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "donation": result,
                "logged_in_as": current_user,
                "message": "A donation has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

# READ (R)
@donations_routes.route("/all", methods=["GET", "OPTIONS"])
@jwt_required()
def get_donations():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = Donations.query.all()
    donation_schema = DonationsSchema(
        many=True,
        only=[
            "iddonation",
            "namadonatur",
            "bankpengirim",
            "jumlahdonasi",
            "rektujuan",
            "donasiimgurl",
            "created_at",
            "updated_at",
            "donatur_id",
        ],
    )
    donations = donation_schema.dump(fetch)
    descendingdonations = sorted(donations, key=lambda x: x["iddonation"], reverse=True)
    return response_with(resp.SUCCESS_200, value={"donations": descendingdonations})


@donations_routes.route("/<int:id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_specific_donation(id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = Donations.query.get_or_404(id)
    donation_schema = DonationsSchema(
        many=False,
        only=[
            "iddonation",
            "namadonatur",
            "bankpengirim",
            "jumlahdonasi",
            "rektujuan",
            "donasiimgurl",
            "created_at",
            "updated_at",
            "donatur_id",
        ],
    )
    donation = donation_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"donation": donation})



# UPDATE (U)


# DELETE (D)