from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Agendas import Agenda, AgendaSchema
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

agenda_routes = Blueprint("agenda_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@agenda_routes.route("/create", methods=["POST", "OPTIONS"])
@jwt_required()
def create_agenda():
    try:
        # handle preflight request first
        if request.method == "OPTIONS":
            return response_with(resp.SUCCESS_200)
        current_user = get_jwt_identity()
        data = request.get_json()
        agenda_schema = (
            AgendaSchema()
        )  # ad schema pertama didefinisikan full utk menerima seluruh data yang diperlukan termasuk password
        agenda = agenda_schema.load(data)
        # need validation in ad creation process
        agendaobj = Agenda(
            judul=agenda["judul"],
            agendaimgurl=agenda["agendaimgurl"],
            agendadesc=agenda["agendadesc"],
            agendatext=agenda["agendatext"],
            tanggalmulai=agenda["tanggalmulai"],
            tanggalselesai=agenda["tanggalselesai"],
            file=agenda["file"],
        )
        filename = secure_filename(agendaobj.agendaimgurl)
        agendaobj.agendaimgurl = filename
        agendaobj.author_id = agenda["author_id"]
        imgfile = b64decode(agendaobj.file.split(",")[1] + "==")
        print(imgfile)
        print(UPLOADDIR)
        with open(UPLOADDIR + "/" + agendaobj.agendaimgurl, "wb") as f:
            f.write(imgfile)
        # save to db
        agendaobj.create()
        result = agenda_schema.dump(agendaobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "agenda": result,
                "logged_in_as": current_user,
                "message": "An agenda has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@agenda_routes.route("/all", methods=["GET", "OPTIONS"])
def get_agenda():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    fetch = Agenda.query.all()
    agenda_schema = AgendaSchema(
        many=True,
        only=[
            "idagenda",
            "judul",
            "agendaimgurl",
            "agendadesc",
            "agendatext",
            "tanggalmulai",
            "tanggalselesai",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    agendas = agenda_schema.dump(fetch)
    descendingagendas = sorted(agendas, key=lambda x: x["idagenda"], reverse=True)
    return response_with(resp.SUCCESS_200, value={"agendas": descendingagendas})


@agenda_routes.route("/<int:id>", methods=["GET"])
def get_specific_agenda(id):
    fetch = Agenda.query.get_or_404(id)
    agenda_schema = AgendaSchema(
        many=False,
        only=[
            "idagenda",
            "judul",
            "agendaimgurl",
            "agendadesc",
            "agendatext",
            "tanggalmulai",
            "tanggalselesai",
            "created_at",
            "updated_at",
            "author_id",
        ],
    )
    agenda = agenda_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"agenda": agenda})


# UPDATE (U)
@agenda_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_agenda(id):
    try:
        current_user = get_jwt_identity()
        agendaobj = Agenda.query.get_or_404(id)
        data = request.get_json()
        agenda_schema = AgendaSchema()
        agenda = agenda_schema.load(data, partial=True)
        if "judul" in agenda and agenda["judul"] is not None:
            if agenda["judul"] != "":
                agendaobj.judul = agenda["judul"]
        if "agendaimgurl" in agenda and agenda["agendaimgurl"] is not None:
            if agenda["agendaimgurl"] != "":
                agendaobj.agendaimgurl = agenda["agendaimgurl"]
        if "agendadesc" in agenda and agenda["agendadesc"] is not None:
            if agenda["agendadesc"] != "":
                agendaobj.agendadesc = agenda["agendadesc"]
        if "agendadesc" in agenda and agenda["agendatext"] is not None:
            if agenda["agendatext"] != "":
                agendaobj.agendatext = agenda["agendatext"]
        if "tanggalmulai" in agenda and agenda["tanggalmulai"] is not None:
            if agenda["tanggalmulai"] != "":
                agendaobj.tanggalmulai = agenda["tanggalmulai"]
        if "tanggalselesai" in agenda and agenda["tanggalselesai"] is not None:
            if agenda["tanggalselesai"] != "":
                agendaobj.tanggalselesai = agenda["tanggalselesai"]
        if "author_id" in agenda and agenda["author_id"] is not None:
            if agenda["author_id"] != "":
                agendaobj.author_id = agenda["author_id"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "agenda": agenda,
                "logged_in_as": current_user,
                "message": "Agenda details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@agenda_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_agenda(id):
    current_user = get_jwt_identity()
    agendaobj = Agenda.query.get_or_404(id)
    db.session.delete(agendaobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "Agenda successfully deleted!"},
    )
