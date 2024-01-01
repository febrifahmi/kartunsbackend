from flask import Blueprint, Request
from flask.globals import request
from webapp.api.utils.responses import response_with
from webapp.api.utils import responses as resp
from webapp.api.models.Members import Member, MemberSchema
from webapp.api.utils.database import db
import os
from flask import current_app

# Flask-JWT-Extended preparation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

logtail_routes = Blueprint("logtail_routes", __name__)


# https://stackoverflow.com/a/13790289
def tail(f, lines=1, _buffer=4098):
    """Tail a file and get X lines from the end"""
    # place holder for the lines found
    lines_found = []

    # block counter will be multiplied by buffer
    # to get the block size from the end
    block_counter = -1

    # loop until we find X lines
    while len(lines_found) < lines:
        try:
            f.seek(block_counter * _buffer, os.SEEK_END)
        except IOError:  # either file is too small, or too many lines requested
            f.seek(0)
            lines_found = f.readlines()
            break

        lines_found = f.readlines()

        # we found enough lines, get out
        # Removed this line because it was redundant the while will catch
        # it, I left it for history
        # if len(lines_found) > lines:
        #    break

        # decrement the block counter to get the
        # next X bytes
        block_counter -= 1

    return lines_found[-lines:]


# READ
@logtail_routes.route("/readlog", methods=["GET", "OPTIONS"])
@jwt_required()
def get_logs():
    # handle preflight request first
    if request.method == "OPTIONS":
        return response_with(resp.SUCCESS_200)
    logfile = current_app.config['KARTUNSLOGFILE']
    if os.path.isfile(logfile):
        with open(logfile) as f:
            logs = tail(f, 100, 4098)
    else:
        logs = "app logs not available on dev mode."
    return response_with(resp.SUCCESS_200, value={"logs": logs})