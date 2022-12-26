from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Agendas import Agenda, AgendaSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

agenda_routes = Blueprint("agenda_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@agenda_routes.route("/create", methods=["POST"])
@jwt_required()
def create_agenda():
    try:
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
        )
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
@agenda_routes.route("/all", methods=["GET"])
def get_agenda():
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
        ],
    )
    agenda = agenda_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"agenda": agenda})

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
        if agenda["judul"] is not None:
            agendaobj.judul = agenda["judul"]
        if agenda["agendaimgurl"] is not None:
            agendaobj.agendaimgurl = agenda["agendaimgurl"]
        if agenda["agendadesc"] is not None:
            agendaobj.agendadesc = agenda["agendadesc"]
        if agenda["agendatext"] is not None:
            agendaobj.agendatext = agenda["agendatext"]
        if agenda["tanggalmulai"] is not None:
            agendaobj.tanggalmulai = agenda["tanggalmulai"]
        if agenda["tanggalselesai"] is not None:
            agendaobj.tanggalselesai = agenda["tanggalselesai"]
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