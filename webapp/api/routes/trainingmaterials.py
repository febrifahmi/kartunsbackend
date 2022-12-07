from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.TrainingMaterials import TrainingMaterial, TrainMatSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

trainmat_routes = Blueprint("trainmat_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@trainmat_routes.route("/create", methods=["POST"])
@jwt_required()
def create_trainmat():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        trainmat_schema = (
            TrainMatSchema()
        )  # ad schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        trainmat = trainmat_schema.load(data)
        # need validation in ad creation process
        trainmatobj = TrainingMaterial(
            tmtitle=trainmat["tmtitle"],
            tmimgurl=trainmat["adimgurl"],
            tmdesc=trainmat["tmdesc"],
            tmtext=trainmat["tmtext"],
            urifile=trainmat["urifile"],
            is_verified=trainmat["is_verified"],
        )
        result = trainmat_schema.dump(trainmatobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "material": result,
                "logged_in_as": current_user,
                "message": "Training material has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@trainmat_routes.route("/all", methods=["GET"])
def get_trainmats():
    fetch = TrainingMaterial.query.all()
    trainmat_schema = TrainMatSchema(
        many=True,
        only=[
            "idtm",
            "tmtitle",
            "tmimgurl",
            "tmdesc",
            "tmtext",
            "urifile",
            "is_verified",
            "created_at",
            "updated_at",
            "training_id",
        ],
    )
    trainmats = trainmat_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"trainingmaterials": trainmats})


@trainmat_routes.route("/<int:id>", methods=["GET"])
def get_specific_trainmat(id):
    fetch = TrainingMaterial.query.get_or_404(id)
    trainmat_schema = TrainMatSchema(
        many=False,
        only=[
            "idtm",
            "tmtitle",
            "tmimgurl",
            "tmdesc",
            "tmtext",
            "urifile",
            "is_verified",
            "created_at",
            "updated_at",
            "training_id",
        ],
    )
    trainmat = trainmat_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"trainingmaterial": trainmat})


# UPDATE (U)
@trainmat_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_trainmat(id):
    try:
        current_user = get_jwt_identity()
        trainmatobj = TrainingMaterial.query.get_or_404(id)
        data = request.get_json()
        trainmat_schema = TrainMatSchema()
        trainmat = trainmat_schema.load(data, partial=True)
        if trainmat["tmtitle"] is not None:
            trainmatobj.tmtitle = trainmat["tmtitle"]
        if trainmat["tmimgurl"] is not None:
            trainmatobj.tmimgurl = trainmat["tmimgurl"]
        if trainmat["tmdesc"] is not None:
            trainmatobj.tmdesc = trainmat["tmdesc"]
        if trainmat["tmtext"] is not None:
            trainmatobj.tmtext = trainmat["tmtext"]
        if trainmat["urifile"] is not None:
            trainmatobj.urifile = trainmat["urifile"]
        if trainmat["is_verified"] is not None:
            trainmatobj.is_verified = trainmat["is_verified"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "trainingmaterial": trainmat,
                "logged_in_as": current_user,
                "message": "Training details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@trainmat_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_trainmat(id):
    current_user = get_jwt_identity()
    trainmatobj = TrainingMaterial.query.get_or_404(id)
    db.session.delete(trainmatobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "Training material successfully deleted!"},
    )




