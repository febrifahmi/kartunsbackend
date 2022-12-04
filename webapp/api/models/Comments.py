import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class Comment(db.Model):
    __tablename__ = "comments"
    idcomment = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(140))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    komentator_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))
    article_id = db.Column(db.Integer, db.ForeignKey("articles.idarticle"))

    # relationship

    def __init__(
        self, comment
    ):
        self.comment = comment

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        sqla_session = db.session

    idcomment = fields.Integer(dump_only=True)
    comment = fields.String(required=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    komentator_id = fields.Integer()
    article_id = fields.Integer()