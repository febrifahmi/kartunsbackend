from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Comments import Comment, CommentSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

comment_routes = Blueprint("comment_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@comment_routes.route("/create", methods=["POST"])
@jwt_required()
def create_comment():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        comment_schema = (
            CommentSchema()
        )  # ad schema pertama didefinisikan full utk menerima seluruh data yang diperlukan termasuk password
        comment = comment_schema.load(data)
        # need validation in ad creation process
        commentobj = Comment(
            comment=comment["comment"],
        )
        result = comment_schema.dump(commentobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "comment": result,
                "logged_in_as": current_user,
                "message": "A comment has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@comment_routes.route("/all", methods=["GET"])
def get_comments():
    fetch = Comment.query.all()
    comment_schema = CommentSchema(
        many=True,
        only=[
            "idcomment",
            "comment",
            "created_at",
            "updated_at",
            "komentator_id",
        ],
    )
    comments = comment_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"comments": comments})


@comment_routes.route("/<int:id>", methods=["GET"])
def get_specific_comment(id):
    fetch = Comment.query.get_or_404(id)
    comment_schema = CommentSchema(
        many=False,
        only=[
            "idcomment",
            "comment",
            "created_at",
            "updated_at",
            "komentator_id",
        ],
    )
    comment = comment_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"comment": comment})


# UPDATE (U)
@comment_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_comment(id):
    try:
        current_user = get_jwt_identity()
        commentobj = Comment.query.get_or_404(id)
        data = request.get_json()
        comment_schema = CommentSchema()
        comment = comment_schema.load(data, partial=True)
        if "comment" in comment and comment["comment"] is not None:
            if comment["comment"] != "":
                commentobj.comment = comment["comment"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "comment": comment,
                "logged_in_as": current_user,
                "message": "Comment details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@comment_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_comment(id):
    current_user = get_jwt_identity()
    commentobj = Comment.query.get_or_404(id)
    db.session.delete(commentobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "Comment successfully deleted!"},
    )

