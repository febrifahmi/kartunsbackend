from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Covers import Cover, CoverSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

cover_routes = Blueprint("cover_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@cover_routes.route("/create", methods=["POST"])
@jwt_required()
def create_cover():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        cover_schema = (
            CoverSchema()
        )  # ad schema pertama didefinisikan full utk menerima seluruh data yang diperlukan termasuk password
        cover = cover_schema.load(data)
        # need validation in ad creation process
        coverobj = Cover(
            covertitle=cover["covertitle"],
            coverimgurl=cover["coverimgurl"],
            coverdesc=cover["coverdesc"],
            covertext=cover["covertext"],
            nrdaysserved=cover["nrdaysserved"],
        )
        result = cover_schema.dump(coverobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "cover": result,
                "logged_in_as": current_user,
                "message": "A cover has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@cover_routes.route("/all", methods=["GET"])
def get_covers():
    fetch = Cover.query.all()
    cover_schema = CoverSchema(
        many=True,
        only=[
            "idcover",
            "covertitle",
            "coverimgurl",
            "coverdesc",
            "covertext",
            "nrdaysserved",
            "created_at",
            "updated_at",
        ],
    )
    covers = cover_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"covers": covers})


@cover_routes.route("/<int:id>", methods=["GET"])
def get_specific_cover(id):
    fetch = Cover.query.get_or_404(id)
    cover_schema = CoverSchema(
        many=False,
        only=[
            "idcover",
            "covertitle",
            "coverimgurl",
            "coverdesc",
            "covertext",
            "nrdaysserved",
            "created_at",
            "updated_at",
        ],
    )
    cover = cover_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"cover": cover})


# UPDATE (U)
@cover_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_cover(id):
    try:
        current_user = get_jwt_identity()
        coverobj = Cover.query.get_or_404(id)
        data = request.get_json()
        cover_schema = CoverSchema()
        cover = cover_schema.load(data, partial=True)
        if cover["covertitle"] is not None:
            coverobj.covertitle = cover["covertitle"]
        if cover["coverimgurl"] is not None:
            coverobj.coverimgurl = cover["coverimgurl"]
        if cover["coverdesc"] is not None:
            coverobj.coverdesc = cover["coverdesc"]
        if cover["nrdaysserved"] is not None:
            coverobj.nrdaysserved = cover["nrdaysserved"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "cover": cover,
                "logged_in_as": current_user,
                "message": "Cover details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@cover_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_cover(id):
    current_user = get_jwt_identity()
    coverobj = Cover.query.get_or_404(id)
    db.session.delete(coverobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "A cover successfully deleted!"},
    )
