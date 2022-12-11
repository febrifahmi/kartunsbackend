import datetime
# from webapp import bcrypt
from flask_bcrypt import Bcrypt
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields
# from webapp.api.models.Pakets import PaketSchema

# import hmac to substitute hash checking, after werkzeug.security.safe_str_cm was deprecated in bcrypt check_password_hash implementation
# import hmac

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = "users"
    iduser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(40))
    tentang = db.Column(db.String(1500))
    is_alumni = db.Column(db.Boolean(), default=0)
    is_pengurus = db.Column(db.Boolean(), default=0)
    is_trainer = db.Column(db.Boolean(), default=0)
    is_admin = db.Column(db.Boolean(), default=0)
    admin_verified = db.Column(db.Boolean(), default=0)
    profpic = db.Column(db.String(128))
    passhash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, server_default=db.func.now())
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # relationship
    # ads = db.relationship("Ads", backref="Advertiser", cascade="all, delete-orphan")
    # trainings = db.relationship("Trainings", backref="Participant", cascade="all, delete-orphan")
    # certificates = db.relationship("Certificates", backref="Holder", cascade="all, delete-orphan")

    def __init__(self, username, first_name, last_name, email, is_alumni):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_alumni = is_alumni

    def set_password(self, password):
        self.passhash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(
            self.passhash, password
        )  # check_password_hash that use werkzeug.security.safe_str_cm was deprecated and changed to hmac.check_password_hash. See: https://github.com/maxcountryman/flask-bcrypt/pull/70
        # return hmac.compare_digest(self.passhash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        self.profpic = "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest, size)
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest, size
        )

    # @classmethod # to help login by username using json
    # def find_by_username(cls, username):
    #     return cls.query.filter_by(username=username).first()

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        # load_instance = True
        sqla_session = db.session

    iduser = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String()
    email = fields.String(required=True)
    tentang = fields.String()    
    is_alumni = fields.Boolean()
    is_pengurus = fields.Boolean()
    is_trainer = fields.Boolean()
    is_admin = fields.Boolean()
    admin_verified = fields.Boolean()
    profpic = fields.String()
    password = fields.String(required=True)
    passhash = fields.String()
    last_seen = fields.String(dump_only=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    # pakets = fields.Nested(
    #     PaketSchema,
    #     many=True,
    #     only=["judulpaket", "tahunanggaran", "unitkerja", "email", "telepon"],
    # )
