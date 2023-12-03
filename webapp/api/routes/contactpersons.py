from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.ContactPersons import ContactPerson, ContactPersonSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

contactperson_routes = Blueprint("contactperson_routes", __name__)


# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@contactperson_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_cover():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        data = request.get_json()
        contactperson_schema = (
            ContactPersonSchema()
        )  # CP schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        contactperson = contactperson_schema.load(data)
        # need validation in CP creation process
        contactpersonobj = ContactPerson(
            nama=contactperson["nama"],
            nomorwa=contactperson["nomorwa"],
            is_active=contactperson["is_active"],
        )
        contactpersonobj.user_id = contactperson["userid"]
        # save to db
        contactpersonobj.create()
        # cek apakah file yang diupload sesuai daftar jenis file yg diijinkan
        result = contactperson_schema.dump(contactpersonobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "contactperson": result,
                "logged_in_as": current_user,
                "message": "A contact person has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)
