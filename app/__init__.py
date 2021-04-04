import os

from flask import Flask
from flask_cors import CORS

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# This code was taken from: https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/

"""

To run:

Navigate into the stcm-platform-v1 folder and type the following into the terminal:

On Mac and Linux:

$ export FLASK_APP=app
$ export FLASK_ENV=development
$ flask run

On Windows (cmd):

> set FLASK_APP=app
> set FLASK_ENV=development
> flask run

On Windows (PowerShell):

> $env:FLASK_APP = "app"
> $env:FLASK_ENV = "development"
> flask run

Then navigate into the webapp folder and type the following into the terminal:

> npm run serve

"""

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',  # should be overwritten with something random in deployment
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists (Pretty sure this is for a database we don't have yet)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def root():
        return 'Bruh bruh bruh'

    @app.route("/lookup")
    def stockLookup():
        from api_client import APIClient
        data = request.args.get('stock')
        client = APIClient()
        data1 = str(client.seach_for_ticker(data, max_tick=1000)[0])
        return {"data": data1}

    @app.route("/stock-list-autocomplete")
    def stockList():
        from api_client import APIClient
        data = request.args.get('stock')
        client = APIClient()
        list = client.get_relevant_stock_tickers(data)
        return {"data": list}

    # /lookup
    # from . import lookup
    # app.register_blueprint(lookup.bp)

    return app
