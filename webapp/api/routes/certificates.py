from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Certificates import Certificate, CertificateSchema
from webapp.api.utils.database import db

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

certificate_routes = Blueprint("certificate_routes", __name__)

# CONSULT https://marshmallow.readthedocs.io/en/stable/quickstart.html IF YOU FIND ANY TROUBLE WHEN USING SCHEMA HERE!
# CREATE (C)
@certificate_routes.route("/create", methods=["POST"])
@jwt_required()
def create_certificate():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        certificate_schema = (
            CertificateSchema()
        )  # certificate schema pertama didefinisikan full utk menerima seluruh data yang diperlukan
        certificate = certificate_schema.load(data)
        # need validation in ad creation process
        certobj = Certificate(
            certtitle=certificate["certtitle"],
            certbgimgurl=certificate["certbgimgurl"],
            certnumber=certificate["certnumber"],
            certtext=certificate["certtext"],
            certdate=certificate["certdate"],
            penerima_id=certificate["penerima_id"],
        )
        result = certificate_schema.dump(certobj)
        return response_with(
            resp.SUCCESS_201,
            value={
                "certificate": result,
                "logged_in_as": current_user,
                "message": "Certificate has been created successfully!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# READ (R)
@certificate_routes.route("/all", methods=["GET"])
def get_certificates():
    fetch = Certificate.query.all()
    certificate_schema = CertificateSchema(
        many=True,
        only=[
            "idcert",
            "certtitle",
            "certbgimgurl",
            "certnumber",
            "certtext",
            "certdate",
            "created_at",
            "updated_at",
            "penerima_id",
        ],
    )
    certificates = certificate_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"certificates": certificates})


@certificate_routes.route("/<int:id>", methods=["GET"])
def get_specific_certificate(id):
    fetch = Certificate.query.get_or_404(id)
    certificate_schema = CertificateSchema(
        many=False,
        only=[
            "idcert",
            "certtitle",
            "certbgimgurl",
            "certnumber",
            "certtext",
            "certdate",
            "created_at",
            "updated_at",
            "penerima_id",
        ],
    )
    certificate = certificate_schema.dump(fetch)
    return response_with(resp.SUCCESS_200, value={"certificate": certificate})


# UPDATE (U)
@certificate_routes.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_certificate(id):
    try:
        current_user = get_jwt_identity()
        certobj = Certificate.query.get_or_404(id)
        data = request.get_json()
        certificate_schema = CertificateSchema()
        certificate = certificate_schema.load(data, partial=True)
        if certificate["certtitle"] is not None:
            certobj.certtitle = certificate["certtitle"]
        if certificate["certbgimgurl"] is not None:
            certobj.certbgimgurl = certificate["certbgimgurl"]
        if certificate["certnumber"] is not None:
            certobj.certnumber = certificate["certnumber"]
        if certificate["certtex"] is not None:
            certobj.certtext = certificate["certtext"]
        if certificate["certdate"] is not None:
            certobj.certdate = certificate["certdate"]
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                "certificate": certificate,
                "logged_in_as": current_user,
                "message": "Certificate details successfully updated!",
            },
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


# DELETE (D)
@certificate_routes.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_certificate(id):
    current_user = get_jwt_identity()
    certobj = Certificate.query.get_or_404(id)
    db.session.delete(certobj)
    db.session.commit()
    return response_with(
        resp.SUCCESS_200,
        value={"logged_in_as": current_user, "message": "Certificate successfully deleted!"},
    )


