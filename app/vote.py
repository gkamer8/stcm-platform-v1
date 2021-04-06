import functools
import json
from api_client import APIClient
from app.db import get_db
from app.auth import decode_auth_token

import jwt
import datetime
import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

from werkzeug.security import check_password_hash, generate_password_hash

from api_client import APIClient

# Implementation built using: https://realpython.com/token-based-authentication-with-flask/#user-status-route

bp = Blueprint('vote', __name__, url_prefix='/vote')

# TODO: Make the server update the "passed" variable after each vote is cast

# /vote/cast
@bp.route("/cast", methods=('GET', 'POST'))
def cast():
    if request.method == 'POST':

        auth_token = request.headers['Authentication']
        resp = decode_auth_token(auth_token)
        if not isinstance(resp, str):
            db = get_db()
            user = db.execute(
                'SELECT * FROM user WHERE id = ?', (resp,)
            ).fetchone()
        else:
            return json.dumps({'error':resp})

        decisionid = request.json['decisionid']
        forvote = request.json['for']

        db = get_db()
        error = None

        if not isinstance(decisionid, int):
            error = 'Decicion id is required.'
        elif not isinstance(forvote, int):
            error = 'For vote is required.'
        elif db.execute(
            'SELECT id FROM votes WHERE userid = ? AND decisionid = ?', (user['id'],decisionid)
        ).fetchone() is not None:
            db.execute(
                'UPDATE votes SET (for) VALUES (?,) WHERE decisionid = ? AND userid = ?',
                (forvote, decisionid, user['id'])
            )
            db.commit()
            return json.dumps({'message': 'success'})

        if error is None:
            db.execute(
                'INSERT INTO votes (decisionid, for, userid, date) VALUES (?, ?, ?, ?)',
                (decisionid, forvote, user['id'], int(time.time()))
            )
            db.commit()
            return json.dumps({'message': 'success'})

        return json.dumps({'error': error})

    return json.dumps({'error': 'request must be post'})


# /vote/create
@bp.route("/create", methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        auth_token = request.headers['Authentication']
        resp = decode_auth_token(auth_token)
        if not isinstance(resp, str):
            db = get_db()
            user = db.execute(
                'SELECT * FROM user WHERE id = ?', (resp,)
            ).fetchone()
        else:
            return json.dumps({'error': resp})
        
        description = request.json['description']
        title = request.json['title']

        if not description:
            error = 'Description is required.'
        elif not title:
            error = 'Title is required.'

        if error is None:
            db.execute(
                'INSERT INTO decisions (description, date, title, passed, userid) VALUES (?, ?, ?, ?, ?)',
                (description, int(time.time()), title, 0, user['id'])
            )
            db.commit()
            return json.dumps({'message': 'success'})

        return json.dumps({'error': error})
    
    return json.dumps({'error': 'must use POST'})


# Returns list of all decisions since a particular date
# /vote/decisions
@bp.route("/decisions", methods=('GET', 'POST'))
def decisions():
    if request.method == 'POST':
        auth_token = request.headers['Authentication']
        resp = decode_auth_token(auth_token)
        if not isinstance(resp, str):
            db = get_db()
            user = db.execute(
                'SELECT * FROM user WHERE id = ?', (resp,)
            ).fetchone()
        else:
            return json.dumps({'error': resp})
        
        try:
            date = request.json['date']
        except:
            date = 0

        decisions = db.execute(
                        'SELECT id, description, title, userid, passed, date FROM decisions WHERE date >= ?', (date,)
                    )
        
        to_return = []
        for row in decisions:
            to_add = {
                'id': row[0],
                'description': row[1],
                'title': row[2],
                'userid': row[3],
                'passed': row[4],
                'date': row[5]
            }
            to_return.append(to_add)

        return json.dumps({'data': to_return})

    return json.dumps({'error': 'must use POST'})
