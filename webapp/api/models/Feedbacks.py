import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class Feedback(db.Model):
    __tablename__ = "feedbacks"
    idfeedback = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feedbacktitle = db.Column(db.String(50))
    feedbackimgurl = db.Column(db.String(128))
    feedbackdesc = db.Column(db.String(140))
    feedbacktext = db.Column(db.String(800))
    is_followedup = db.Column(db.Boolean(), default=0)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    customer_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    def __init__(
        self, feedbacktitle, feedbackimgurl, feedbackdesc, feedbacktext,
    ):
        self.feedbacktitle = feedbacktitle
        self.feedbackimgurl = feedbackimgurl
        self.feedbackdesc = feedbackdesc
        self.feedbacktext = feedbacktext

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class FeedbackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feedback
        sqla_session = db.session

    idfeedback = fields.Integer(dump_only=True)
    feedbacktitle = fields.String(required=True)
    feedbackimgurl = fields.String()
    feedbackdesc = fields.String(required=True)
    feedbacktext = fields.String(required=True)
    is_followedup = fields.Boolean()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    customer_id = fields.Integer()