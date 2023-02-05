from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Reactions import Reaction, ReactionSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

reaction_routes = Blueprint("reaction_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@reaction_routes.route("/create", methods=["POST"])
@jwt_required()
def create_reaction():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        reaction_schema = (
            ReactionSchema()
        )  # reaction schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        reaction = reaction_schema.load(data)
        # need validation in ad creation process
        reactionobj = Reaction(
            reactioncontent=reaction["reactioncontent"],
            audience_id=reaction["audience_id"],
            article_id=reaction["article_id"],
            agenda_id=reaction["agenda_id"],
        )
        result = reaction_schema.dump(reactionobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "reaction": result,
                "logged_in_as": current_user,
                "message": "A reaction has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@reaction_routes.route("/all", methods=["GET"])
def get_reaction():
    fetch = Reaction.query.all()
    reaction_schema = ReactionSchema(
        many=True,
        only=[
            "idreaction",
            "reactioncontent",
            "created_at",
            "updated_at",
            "audience_id",
            "article_id",
            "agenda_id",
        ],
    )
    reactions = reaction_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"reactions": reactions})


@reaction_routes.route("/<int:id>", methods=["GET"])
def get_specific_reaction(id):
    fetch = Reaction.query.get_or_404(id)
    reaction_schema = ReactionSchema(
        many=False,
        only=[
            "idreaction",
            "reactioncontent",
            "created_at",
            "updated_at",
            "audience_id",
            "article_id",
            "agenda_id",
        ],
    )
    reaction = reaction_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"reaction": reaction})


# UPDATE (U)
@reaction_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_reaction(id):
    try:
        current_user = get_jwt_identity()
        reactionobj = Reaction.query.get_or_404(id)
        data = request.get_json()
        reaction_schema = ReactionSchema()
        reaction = reaction_schema.load(data, partial=True)
        if "reactioncontent" in reaction and reaction["reactioncontent"] is not None:
            reactionobj.reactioncontent = reaction["reactioncontent"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "reaction": reaction,
                "logged_in_as": current_user,
                "message": "Reaction details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@reaction_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_reaction(id):
    current_user = get_jwt_identity()
    reactionobj = Reaction.query.get_or_404(id)
    db.session.delete(reactionobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "Reaction successfully deleted!"},
    )

