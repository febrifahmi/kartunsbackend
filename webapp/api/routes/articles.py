from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Articles import Article, ArticleSchema
from webapp.api.utils.database import db
from werkzeug.utils import secure_filename
import os, random, string
from PIL import Image
from base64 import b64decode, decodebytes

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

UPLOADDIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "static", "uploads")
)

article_routes = Blueprint("article_routes", __name__)


# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@article_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_article():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
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
            file=article["file"],
        )
        filename = secure_filename(articleobj.articleimgurl)
        articleobj.articleimgurl = filename
        imgfile = b64decode(articleobj.file.split(",")[1] + "==")
        print(imgfile)
        print(UPLOADDIR)
        with open(UPLOADDIR + "/" + articleobj.articleimgurl, "wb") as f:
            f.write(imgfile)
        # save to db
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
@article_routes.route("/all", methods=["GET", "OPTIONS"])
def get_article():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
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
    descendingarticle = sorted(articles, key=lambda x: x["idarticle"], reverse=True)
    return response_with(resp.SUCCESS_200, value={"articles": descendingarticle})


@article_routes.route("/<int:id>", methods=["GET", "OPTIONS"])
def get_specific_article(id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
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
@article_routes.route("/update/<int:id>", methods=["PUT", "OPTIONS"])
@jwt_required()
def update_article(id):
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        articleobj = Article.query.get_or_404(id)
        data = request.get_json()
        article_schema = ArticleSchema()
        article = article_schema.load(data, partial=True)
        if "articletitle" in article and article["articletitle"] is not None:
            if article["articletitle"] != "":
                articleobj.articletitle = article["articletitle"]
        if "articleimgurl" in article and article["articleimgurl"] is not None:
            if article["articleimgurl"] != "":
                filename = secure_filename(article["articleimgurl"])
                articleobj.articleimgurl = "artc_" + filename
        if "articledesc" in article and article["articledesc"] is not None:
            if article["articledesc"] != "":
                articleobj.articledesc = article["articledesc"]
        if "articletext" in article and article["articletext"] is not None:
            if article["articletext"] != "":
                articleobj.articletext = article["articletext"]
        if "author_id" in article and article["author_id"] is not None:
            if article["author_id"] != "":
                articleobj.author_id = article["author_id"]
        if "file" in article and article["file"] is not None:
            if article["file"] != "":
                imgfile = b64decode(article["file"].split(",")[1] + "==")
                print(imgfile)
                print(UPLOADDIR)
                with open(UPLOADDIR + "/" + articleobj.articleimgurl, "wb") as f:
                    f.write(imgfile)
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
@article_routes.route("/delete/<int:id>", methods=["DELETE", "OPTIONS"])
@jwt_required()
def delete_article(id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    current_user = get_jwt_identity()
    articleobj = Article.query.get_or_404(id)
    db.session.delete(articleobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={
            "logged_in_as": current_user,
            "message": "Article successfully deleted!",
        },
    )
