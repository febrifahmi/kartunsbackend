import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class Feed(db.Model):
    __tablename__ = "feeds"
    idfeed = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feedtext = db.Column(db.String(140))
    reply_to_feed_id = db.Column(db.String())
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    feed_author_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    # relationship

    def __init__(
        self, feedtext
    ):
        self.feedtext = feedtext

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class FeedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feed
        sqla_session = db.session

    idfeed = fields.Integer(dump_only=True)
    feedtext = fields.String(required=True)
    reply_to_feed_id = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    feed_author_id = fields.Integer()