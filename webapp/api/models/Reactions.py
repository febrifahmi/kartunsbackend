import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class Reaction(db.Model):
    __tablename__ = "reactions"
    idreaction = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reactioncontent = db.Column(db.String(8))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    audience_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))
    article_id = db.Column(db.Integer, db.ForeignKey("articles.idarticle"))
    agenda_id = db.Column(db.Integer, db.ForeignKey("agendas.idagenda"))

    def __init__(
        self, reactioncontent
    ):
        self.reactioncontent = reactioncontent

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class ReactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reaction
        sqla_session = db.session

    idreaction = fields.Integer(dump_only=True)
    reactioncontent = fields.String(required=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    audience_id = fields.Integer()
    article_id = fields.Integer()
    agenda_id = fields.Integer()