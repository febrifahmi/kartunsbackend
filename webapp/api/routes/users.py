from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Users import User, UserSchema
from webapp.api.utils.database import db
from werkzeug.utils import secure_filename
import traceback
import os, random, string
from base64 import b64decode, decodebytes, b64encode

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

PROFILEDIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","..","static","profiles"))

user_routes = Blueprint("user_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@user_routes.route("/create", methods=["POST"])
@jwt_required()
def create_user():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        user_schema = (
            UserSchema()
        )  # user schema pertama didefinisikan full utk menerima seluruh data yang diperlukan termasuk password
        user = user_schema.load(data)
        # need validation in user creation process (cek existing username, email, etc)
        userobj = User(
            username=user["username"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            is_alumni=user["is_alumni"],
        )
        userobj.set_password(user["password"])
        userobj.create()
        user_schema = UserSchema(
            only=[
                "username",
                "first_name",
                "last_name",
                "email",
                "is_alumni",
                "is_admin",
            ]
        )  # definisikan ulang user_schema tanpa memasukkan plain password sehingga di exclude dari result/API response
        result = user_schema.dump(user)
        return response_with(
            resp.SUCCESS_201,
            value={
                "user": result,
                "logged_in_as": current_user,
                "message": "An account has been created for {} successfully!".format(
                    user["email"]
                ),
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@user_routes.route("/all", methods=["GET", "OPTIONS"])
@jwt_required()
def get_users():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = User.query.all()
    user_schema = UserSchema(
        many=True,
        only=[
            "iduser",
            "username",
            "first_name",
            "last_name",
            "email",
            "tentang",
            "is_alumni",
            "is_pengurus",
            "is_admin",
            "admin_verified",
            "profpic",
            "created_at",
            "updated_at",
        ],
    )
    users = user_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"users": users})


@user_routes.route("/<int:id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_specific_user(id):
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = User.query.get_or_404(id)
    user_schema = UserSchema(
        many=False,
        only=[
            "iduser",
            "username",
            "first_name",
            "last_name",
            "email",
            "tentang",
            "is_alumni",
            "is_pengurus",
            "is_admin",
            "admin_verified",
            "profpic",
            "created_at",
            "updated_at",
        ],
    )
    user = user_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"user": user})


# UPDATE (U)
@user_routes.route("/update/<int:id>", methods=["PUT", "OPTIONS"])
@jwt_required()
def update_user(id):
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        userobj = User.query.get_or_404(id)
        data = request.get_json()
        user_schema = UserSchema()
        user = user_schema.load(data, partial=True)
        if "username" in user and user["username"] is not None:
            if user["username"] != "":
                userobj.username = user["username"]
        if "first_name" in user and user["first_name"] is not None:
            if user["first_name"] != "":
                userobj.first_name = user["first_name"]
        if "last_name" in user and user["last_name"] is not None:
            if user["last_name"] != "":
                userobj.last_name = user["last_name"]
        if "email" in user and user["email"] is not None:
            if user["email"] != "":
                userobj.email = user["email"]
        if "tentang" in user and user["tentang"] is not None:
            if user["tentang"] != "":
                userobj.tentang = user["tentang"]
        if "is_alumni" in user and user["is_alumni"] is not None:
            if user["is_alumni"] != "":
                userobj.is_alumni = user["is_alumni"]
        if "is_pengurus" in user and user["is_pengurus"] is not None:
            if user["is_pengurus"] != "":
                userobj.is_pengurus = user["is_pengurus"]
        if "password" in user and user["password"] is not None:
            if user["password"] != "":
                userobj.set_password(user["password"])
        if "profpic" in user and user["profpic"] is not None:
            if user["profpic"] != "":
                filename = secure_filename(user["profpic"])
                userobj.profpic = filename
        if "file" in user and user["file"] is not None:
            if user["file"] != "":
                imgfile = b64decode(user["file"].split(",")[1] + '==')
                print(imgfile)
                print(PROFILEDIR)
                with open(PROFILEDIR + "/" + userobj.profpic, "wb") as f:
                    f.write(imgfile)
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "user": user,
                "logged_in_as": current_user,
                "message": "User details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        traceback.print_exc()
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@user_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    current_user = get_jwt_identity()
    userobj = User.query.get_or_404(id)
    db.session.delete(userobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "User successfully deleted!"},
    )


# LOGIN (L)
@user_routes.route("/login", methods=["POST", "OPTIONS"])
def authenticate_user():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        data = request.get_json()
        active_user = User.query.filter_by(username=data["username"]).first()
        # print(active_user.username,active_user.first_name,active_user.passhash)
        if not active_user:
            return response_with(resp.SERVER_ERROR_404)
        if active_user.check_password(data["password"]):
            access_token = create_access_token(
                identity=data["username"], fresh=timedelta(minutes=15)
            )
            return response_with(
                resp.SUCCESS_201,
                value={
                    "message": "Logged in as {}".format(active_user.username),
                    "logged_in_as": active_user.username,
                    "iduser": active_user.iduser,
                    "name": active_user.first_name + " " + active_user.last_name,
                    "useremail": active_user.email,
                    "tentang": active_user.tentang,
                    "access_token": access_token,
                    "avatar": active_user.profpic,
                    "is_alumni": active_user.is_alumni,
                    "is_pengurus": active_user.is_pengurus,
                    "is_trainer": active_user.is_trainer,
                    "is_admin": active_user.is_admin,
                },
            )
        else:
            return response_with(resp.UNAUTHORIZED_403)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# REGISTER (REG)
@user_routes.route("/register", methods=["POST", "OPTIONS"])
def register_user():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        data = request.get_json()
        user_schema = (
            UserSchema()
        )  # user schema pertama didefinisikan full utk menerima seluruh data yang diperlukan termasuk password
        user = user_schema.load(data)
        # need validation in user creation process (cek existing username, email, etc)
        userobj = User(
            username=user["username"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            is_alumni=user["is_alumni"],
        )
        userobj.set_password(user["password"])
        userobj.profpic = userobj.avatar(128)
        userobj.create()
        user_schema = UserSchema(
            only=[
                "username",
                "first_name",
                "last_name",
                "email",
                "is_alumni",
                "profpic",
            ]
        )  # definisikan ulang user_schema tanpa memasukkan plain password sehingga di exclude dari result/API response
        result = user_schema.dump(user)
        return response_with(
            resp.SUCCESS_201,
            value={
                "user": result,
                "message": "An account has been created for {} successfully!".format(
                    user["email"]
                ),
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# LOGOUT (LO)
@user_routes.route("/logout", methods=["GET", "OPTIONS"])
def logout_user():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    return response_with(resp.SUCCESS_200)
