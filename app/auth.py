import functools
import json
from api_client import APIClient
from app.db import get_db

import jwt
import datetime


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

from werkzeug.security import check_password_hash, generate_password_hash

from api_client import APIClient

# Implementation built using: https://realpython.com/token-based-authentication-with-flask/#user-status-route

bp = Blueprint('auth', __name__, url_prefix='/auth')

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

# /auth/register
@bp.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        name = request.json['name']
        admin = request.json['admin']
        stake = request.json['stake']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        elif not name:
            error = 'Name is required.'
        elif admin != 0 and admin != 1:
            error = 'Admin parameter invalid.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        elif not stake or not isinstance(stake, float) or stake < 0 or stake > 1:
            error = "Stake required and must be a number between 0 and 1"

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, email, name, admin, stake) VALUES (?, ?, ?, ?, ?, ?)',
                (username, generate_password_hash(password), email, name, admin, stake)
            )
            db.commit()
            return json.dumps({'message': 'success'})

        return json.dumps({'error': error})

    return json.dumps({'error': 'request must be post'})


# /auth/login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # session.clear()
            # session['user_id'] = user['id']
            auth_token = encode_auth_token(user['id'])
            return json.dumps({'message': 'success', 'auth_token': auth_token.decode()})

        return json.dumps({'error': error})

    return json.dumps({'error': 'request must be post'})


# Get user information
@bp.route('/userinfo', methods=('GET', 'POST'))
def userinfo():
    if request.method == 'POST':
        auth_token = request.headers['Authentication']
        resp = decode_auth_token(auth_token)
        if not isinstance(resp, str):
            db = get_db()
            user = db.execute(
                'SELECT * FROM user WHERE id = ?', (resp,)
            ).fetchone()
        
            return json.dumps({'username':user['username'], 'admin':user['admin'], 'email':user['email'], 'name':user['name']})
        else:
            return json.dumps({'error': resp})
    
    return json.dumps({'error': 'must use POST'})

# Get all user information
@bp.route('/allusers', methods=('GET', 'POST'))
def allusers():
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
        
        users = db.execute('SELECT * FROM user')
        
        data = []
        for user in users:
            to_append = {}
            to_append['id'] = user['id']
            to_append['username'] = user['username']
            to_append['name'] = user['name']
            to_append['stake'] = user['stake']
            to_append['email'] = user['email']
            data.append(to_append)

        return json.dumps({'data': data})
    
    return json.dumps({'error': 'must use POST'})

@bp.route('/changeinfo', methods=('GET', 'POST'))
def changeinfo():
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
        
        username = request.json['username']
        password = generate_password_hash(request.json['password'])
        name = request.json['name']
        email = request.json['email']

        db.execute('UPDATE user SET username = ?, name = ?, password = ?, email = ? WHERE id = ?', (username, name, password, email, user['id']))
        db.commit()

        return json.dumps({'message':'success'})

    return json.dumps({'error': 'must use POST'})
