from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.PelamarKerjas import PelamarKerja, PelamarKerjaSchema
from webapp.api.utils.database import db
from werkzeug.utils import secure_filename
import os, random, string
from base64 import b64decode, decodebytes

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

pelamarkerja_routes = Blueprint("pelamarkerja_routes", __name__)


# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@pelamarkerja_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_pelamarkerja():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        data = request.get_json()
        pelamarkerja_schema = (
            PelamarKerjaSchema()
        )  # schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        pelamarkerja = pelamarkerja_schema.load(data)
        # need validation in ad creation process
        pelamarkerjaobj = PelamarKerja(
            namapelamar=pelamarkerja["namapelamar"],
            doksuratlamaran=pelamarkerja["doksuratlamaran"],
            dokcv=pelamarkerja["dokcv"],
            dokportofolio=pelamarkerja["dokportofolio"],
            joboffer_id=pelamarkerja["joboffer_id"],
            pelamar_id=pelamarkerja["pelamar_id"],
        )
        # cek eksisting user id and training id, if exist block request otherwise continue save to db
        fetch = PelamarKerja.query.filter_by(user_id=pelamarkerja["pelamar_id"]).all()
        eksistingpelamar = pelamarkerja_schema.dump(fetch, many=True)
        print("Eksisting data: ", eksistingpelamar)
        for item in eksistingpelamar:
            if (
                item["joboffer_id"] == pelamarkerja["joboffer_id"]
                and item["pelamar_id"] == pelamarkerja["pelamar_id"]
            ):
                return response_with(
                    resp.INVALID_INPUT_422,
                    value={
                        "logged_in_as": current_user,
                        "message": "Pelamar has already been recorder as pelamar for this job offer!",
                    },
                )
        # save to db
        pelamarkerjaobj.create()
        result = pelamarkerja_schema.dump(pelamarkerjaobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "pelamarkerja": result,
                "logged_in_as": current_user,
                "message": "Lamaran kerja has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@pelamarkerja_routes.route("/all", methods=["GET", "OPTIONS"])
@jwt_required()
def get_pelamarkerjas():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = PelamarKerja.query.all()
    pelamarkerja_schema = PelamarKerjaSchema(
        many=True,
        only=[
            "idpelamar",
            "namapelamar",
            "doksuratlamaran",
            "dokcv",
            "dokportofolio",
            "hasilseleksiakhir",
            "joboffer_id",
            "pelamar_id",
            "created_at",
            "updated_at",
        ],
    )
    pelamarkerjas = pelamarkerja_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"pelamarkerjas": pelamarkerjas})


@pelamarkerja_routes.route("/<int:pelamar_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_specific_pelamarkerja(pelamar_id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = PelamarKerja.query.filter_by(pelamar_id=pelamar_id).all()
    pelamarkerja_schema = PelamarKerjaSchema(
        many=True,
        only=[
            "idpelamar",
            "namapelamar",
            "doksuratlamaran",
            "dokcv",
            "dokportofolio",
            "hasilseleksiakhir",
            "joboffer_id",
            "pelamar_id",
            "created_at",
            "updated_at",
        ],
    )
    pelamarkerja = pelamarkerja_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"pelamarkerja": pelamarkerja})


# UPDATE (U)

# DELETE (D)
