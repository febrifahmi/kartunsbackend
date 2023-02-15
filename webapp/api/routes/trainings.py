from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Trainings import Training, TrainingSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

training_routes = Blueprint("training_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@training_routes.route("/create", methods=["POST"])
@jwt_required()
def create_training():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        training_schema = (
            TrainingSchema()
        )  # ad schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        training = training_schema.load(data)
        # need validation in ad creation process
        trainingobj = Training(
            trainingtitle=training["trainingtitle"],
            trainingimgurl=training["trainingimgurl"],
            trainingdesc=training["trainingdesc"],
            trainingtext=training["trainingtext"],
            durationday=training["durationday"],
            startdate=training["startdate"],
            level=training["level"],
            price=training["price"],
        )
        result = training_schema.dump(trainingobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "training": result,
                "logged_in_as": current_user,
                "message": "A training has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

# READ (R)
@training_routes.route("/all", methods=["GET"])
def get_trainings():
    fetch = Training.query.all()
    training_schema = TrainingSchema(
        many=True,
        only=[
            "idtraining",
            "trainingtitle",
            "trainingimgurl",
            "trainingdesc",
            "trainingtext",
            "durationday",
            "startdate",
            "level",
            "price",
            "created_at",
            "updated_at",
            "trainer_id",
        ],
    )
    trainings = training_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"trainings": trainings})


@training_routes.route("/<int:id>", methods=["GET"])
def get_specific_training(id):
    fetch = Training.query.get_or_404(id)
    training_schema = TrainingSchema(
        many=False,
        only=[
            "idtraining",
            "trainingtitle",
            "trainingimgurl",
            "trainingdesc",
            "trainingtext",
            "durationday",
            "startdate",
            "level",
            "price",
            "created_at",
            "updated_at",
            "trainer_id",
        ],
    )
    training = training_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"training": training})


# UPDATE (U)
@training_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_training(id):
    try:
        current_user = get_jwt_identity()
        trainingobj = Training.query.get_or_404(id)
        data = request.get_json()
        training_schema = TrainingSchema()
        training = training_schema.load(data, partial=True)
        if "trainingtitle" in training and training["trainingtitle"] is not None:
            if training["trainingtitle"] != "":
                trainingobj.trainingtitle = training["trainingtitle"]
        if "trainingimgurl" in training and training["trainingimgurl"] is not None:
            if training["trainingimgurl"] != "":
                trainingobj.trainingimgurl = training["trainingimgurl"]
        if "trainingdesc" in training and training["trainingdesc"] is not None:
            if training["trainingdesc"] != "":
                trainingobj.trainingdesc = training["trainingdesc"]
        if "trainingtext" in training and training["trainingtext"] is not None:
            if training["trainingtext"] != "":
                trainingobj.trainingtext = training["trainingtext"]
        if "durationday" in training and training["durationday"] is not None:
            if training["durationday"] != "":
                trainingobj.durationday = training["durationday"]
        if "startdate" in training and  training["startdate"] is not None:
            if training["startdate"] != "":
                trainingobj.startdate = training["startdate"]
        if "level" in training and training["level"] is not None:
            if training["level"] != "":
                trainingobj.level = training["level"]
        if "price" in training and training["price"] is not None:
            if training["price"] != "":
                trainingobj.price = training["price"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "training": training,
                "logged_in_as": current_user,
                "message": "Training details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@training_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_training(id):
    current_user = get_jwt_identity()
    trainingobj = Training.query.get_or_404(id)
    db.session.delete(trainingobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "Training successfully deleted!"},
    )


