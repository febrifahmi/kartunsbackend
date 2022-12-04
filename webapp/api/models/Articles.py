import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class Article(db.Model):
    __tablename__ = "articles"
    idarticle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    articletitle = db.Column(db.String(50))
    articleimgurl = db.Column(db.String(128))
    articledesc = db.Column(db.String(140))
    articletext = db.Column(db.String(800))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    author_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    # relationship

    def __init__(
        self, articletitle, articleimgurl, articledesc, articletext
    ):
        self.articletitle = articletitle
        self.articleimgurl = articleimgurl
        self.articledesc = articledesc
        self.articletext = articletext

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class ArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Article
        sqla_session = db.session

    idarticle = fields.Integer(dump_only=True)
    articletitle = fields.String(required=True)
    articleimgurl = fields.String(required=True)
    articledesc = fields.String()
    articletext = fields.String(required=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    author_id = fields.Integer()