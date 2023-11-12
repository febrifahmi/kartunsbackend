from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.AdRates import AdRates, AdRatesSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

adrates_routes = Blueprint("adrates_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@adrates_routes.route("/create", methods=["POST"])
@jwt_required()
def create_adrate():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        adrate_schema = (
            AdRatesSchema()
        )  # ad schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        adrate = adrate_schema.load(data)
        # need validation in ad creation process
        adrateobj = AdRates(
            adratetitle=adrate["adratetitle"],
            adrateperhariharian=adrate["adrateperhariharian"],
            adrateperharibulanan=adrate["adrateperharibulanan"],
            adrateperharitahunan=adrate["adrateperharitahunan"],
        )
        adrateobj.manager_id=adrate["manager_id"]
        adrateobj.create()
        result = adrate_schema.dump(adrateobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "adrate": result,
                "logged_in_as": current_user,
                "message": "An adrate has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (C)

# UPDATE (U)

# DELETE (D)
