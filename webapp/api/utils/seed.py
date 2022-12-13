from flask.cli import with_appcontext
from webapp.api.models.Users import User, UserSchema
from webapp.api.utils import responses as resp
from webapp.api.utils.responses import response_with


@with_appcontext
def seed():
    """Seed the database."""
    try:
        adminexist = 0
        fetch = User.query.all()
        existinguserschema = UserSchema(
            many=True,
            only=[
                "iduser",
                "username",
                "email",
            ],
        )
        existinguser = existinguserschema.dump(fetch)
        for item in existinguser:
            if item["username"] == "admin":
                adminexist = 1
        if adminexist == 0:
            seeddata = {
                "username": "admin",
                "first_name": "Admin",
                "last_name": "KartUNS",
                "email": "admin@kartuns.org",
                "is_alumni": 1,
                "password": "4Dm1n",
                "is_admin": 1,
            }
            user_schema = (
                UserSchema()
            )  # user schema pertama didefinisikan full utk menerima seluruh data yang diperlukan termasuk password
            user = user_schema.load(seeddata)
            # need validation in user creation process (cek existing username, email, etc)
            userobj = User(
                username=user["username"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                email=user["email"],
                is_alumni=user["is_alumni"],
            )
            userobj.set_password(user["password"])
            userobj.is_admin = user["is_admin"]
            userobj.avatar(48)
            userobj.create()
            user_schema = UserSchema(
                only=["username", "first_name", "last_name", "email", "is_admin"]
            )  # definisikan ulang user_schema tanpa memasukkan plain password sehingga di exclude dari result/API response
            result = user_schema.dump(user)
            return response_with(
                resp.SUCCESS_201,
                value={
                    "status": "success",
                    "user": result,
                    "message": "An account has been created for {} successfully!".format(
                        user["email"]
                    ),
                },
            )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)
