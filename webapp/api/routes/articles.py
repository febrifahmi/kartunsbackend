from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Articles import Article, ArticleSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

article_routes = Blueprint("article_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@article_routes.route("/create", methods=["POST"])
@jwt_required()
def create_article():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        article_schema = (
            ArticleSchema()
        )  # article schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        article = article_schema.load(data)
        # need validation in article creation process
        articleobj = Article(
            articletitle=article["articletitle"],
            articleimgurl=article["articleimgurl"],
            articledesc=article["articledesc"],
            articletext=article["articletext"],
            author_id=article["author_id"],
        )
        articleobj.create()
        result = article_schema.dump(articleobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "article": result,
                "logged_in_as": current_user,
                "message": "An article has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@article_routes.route("/all", methods=["GET"])
def get_article():
    fetch = Article.query.all()
    article_schema = ArticleSchema(
        many=True,
        only=[
            "idarticle",
            "articletitle",
            "articleimgurl",
            "articledesc",
            "articletext",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    articles = article_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"articles": articles})


@article_routes.route("/<int:id>", methods=["GET"])
def get_specific_article(id):
    fetch = Article.query.get_or_404(id)
    article_schema = ArticleSchema(
        many=False,
        only=[
            "idarticle",
            "articletitle",
            "articleimgurl",
            "articledesc",
            "articletext",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    article = article_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"article": article})



# UPDATE (U)
@article_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_article(id):
    try:
        current_user = get_jwt_identity()
        articleobj = Article.query.get_or_404(id)
        data = request.get_json()
        article_schema = ArticleSchema()
        article = article_schema.load(data, partial=True)
        if article["articletitle"] is not None:
            articleobj.articletitle = article["articletitle"]
        if article["articleimgurl"] is not None:
            articleobj.articleimgurl = article["articleimgurl"]
        if article["articledesc"] is not None:
            articleobj.articledesc = article["articledesc"]
        if article["articletext"] is not None:
            articleobj.articletext = article["articletext"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "article": article,
                "logged_in_as": current_user,
                "message": "Article details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@article_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_article(id):
    current_user = get_jwt_identity()
    articleobj = Article.query.get_or_404(id)
    db.session.delete(articleobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "Article successfully deleted!"},
    )
