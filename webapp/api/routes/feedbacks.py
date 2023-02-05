from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Feedbacks import Feedback, FeedbackSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

feedback_routes = Blueprint("feedback_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@feedback_routes.route("/create", methods=["POST"])
@jwt_required()
def create_feedback():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        feedback_schema = (
            FeedbackSchema()
        )  # feedback schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        feedback= feedback_schema.load(data)
        # need validation in feedback creation process
        feedbackobj = Feedback(
            feedbacktitle=feedback["feedbacktitle"],
            feedbackimgurl=feedback["feedbackimgurl"],
            feedbackdesc=feedback["feedbackdesc"],
            feedbacktext=feedback["feedbacktext"],
        )
        result = feedback_schema.dump(feedbackobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "feedback": result,
                "logged_in_as": current_user,
                "message": "A feedback has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@feedback_routes.route("/all", methods=["GET"])
def get_feedbacks():
    fetch = Feedback.query.all()
    feedback_schema = FeedbackSchema(
        many=True,
        only=[
            "idfeedback",
            "feedbacktitle",
            "feedbackimgurl",
            "feedbackdesc",
            "feedbacktext",
            "is_followedup",
            "created_at",
            "updated_at",
            "customer_id",
        ],
    )
    feedbacks = feedback_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"feedbacks": feedbacks})


@feedback_routes.route("/<int:id>", methods=["GET"])
def get_specific_feedback(id):
    fetch = Feedback.query.get_or_404(id)
    feedback_schema = FeedbackSchema(
        many=False,
        only=[
            "idfeedback",
            "feedbacktitle",
            "feedbackimgurl",
            "feedbackdesc",
            "feedbacktext",
            "is_followedup",
            "created_at",
            "updated_at",
            "customer_id"
        ],
    )
    feedback = feedback_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"feedback": feedback})


# UPDATE (U)
@feedback_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_feedback(id):
    try:
        current_user = get_jwt_identity()
        feedbackobj = Feedback.query.get_or_404(id)
        data = request.get_json()
        feedback_schema = FeedbackSchema()
        feedback = feedback_schema.load(data, partial=True)
        if "feedbacktitle" in feedback and feedback["feedbacktitle"] is not None:
            feedbackobj.feedbacktitle = feedback["feedbacktitle"]
        if "feedbackimgurl" in feedback and feedback["feedbackimgurl"] is not None:
            feedbackobj.feedbackimgurl = feedback["feedbackimgurl"]
        if "feedbackdesc" in feedback and feedback["feedbackdesc"] is not None:
            feedbackobj.feedbackdesc = feedback["feedbackdesc"]
        if "feedbacktext" in feedback and feedback["feedbacktext"] is not None:
            feedbackobj.feedbacktext = feedback["feedbacktext"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "feedback": feedback,
                "logged_in_as": current_user,
                "message": "Feedback details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@feedback_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_feedback(id):
    current_user = get_jwt_identity()
    feedbackobj = Feedback.query.get_or_404(id)
    db.session.delete(feedbackobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "Feedback successfully deleted!"},
    )

