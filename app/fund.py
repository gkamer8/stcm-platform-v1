import functools
import json
from api_client import APIClient
from app.db import get_db
from app.auth import decode_auth_token

import jwt
import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

from werkzeug.security import check_password_hash, generate_password_hash

from api_client import APIClient

from td_api_client import TDAPIClient

# Implementation built using: https://realpython.com/token-based-authentication-with-flask/#user-status-route

bp = Blueprint('fund', __name__, url_prefix='/fund')

# /fund/positions
@bp.route('/positions', methods=('GET', 'POST'))
def positions():
    auth_token = request.headers['Authentication']
    resp = decode_auth_token(auth_token)
    if isinstance(resp, str):
        return json.dumps({'error':resp})

    tdclient = TDAPIClient()
    positions = tdclient.get_positions()['positions']

    to_return = []
    for pos in positions:
        to_return.append(pos)

    return json.dumps({'data': to_return})