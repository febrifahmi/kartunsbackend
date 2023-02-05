from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Feeds import Feed, FeedSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

feed_routes = Blueprint("feed_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@feed_routes.route("/create", methods=["POST"])
@jwt_required()
def create_feed():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        feed_schema = (
            FeedSchema()
        )  # feed schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        feed = feed_schema.load(data)
        # need validation in feed creation process
        feedobj = Feed(
            feedtext=feed["feedtext"],
            feed_author_id=feed["feed_author_id"],
        )
        feedobj.create()
        result = feed_schema.dump(feedobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "feed": result,
                "logged_in_as": current_user,
                "message": "A feed has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (C)
@feed_routes.route("/all", methods=["GET"])
@jwt_required()
def get_feeds():
    fetch = Feed.query.all()
    feed_schema = FeedSchema(
        many=True,
        only=[
            "idfeed",
            "feedtext",
            "reply_to_feed_id",
            "created_at",
            "updated_at",
            "feed_author_id",
        ],
    )
    feeds = feed_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"feeds": feeds})


@feed_routes.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_specific_feed(id):
    fetch = Feed.query.get_or_404(id)
    feed_schema = FeedSchema(
        many=False,
        only=[
            "idfeed",
            "feedtext",
            "reply_to_feed_id",
            "created_at",
            "updated_at",
            "feed_author_id",
        ],
    )
    feed = feed_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"feed": feed})


# UPDATE (U)
@feed_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_feed(id):
    try:
        current_user = get_jwt_identity()
        feedobj = Feed.query.get_or_404(id)
        data = request.get_json()
        feed_schema = FeedSchema()
        feed = feed_schema.load(data, partial=True)
        if "feedtext" in feed and feed["feedtext"] is not None:
            feedobj.feedtext = feed["feedtext"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "feed": feed,
                "logged_in_as": current_user,
                "message": "Feed details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@feed_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_feed(id):
    current_user = get_jwt_identity()
    feedobj = Feed.query.get_or_404(id)
    db.session.delete(feedobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "Feed successfully deleted!"},
    )