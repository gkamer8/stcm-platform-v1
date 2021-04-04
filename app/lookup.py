import functools
import json
from api_client import APIClient

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from api_client import APIClient

bp = Blueprint('auth', __name__, url_prefix='/lookup')

# /lookup/stock
# Returns JSON with basic stock information like name, logo, website, etc.
@bp.route("/stock")
def stockLookup():
    stock = request.args.get('stock')
    client = APIClient()
    details = client.get_ticker_details(stock)
    data = {'data': details}
    return json.dumps(data)

# /lookup/autocomoplete
# Returns json data with list of tickers that match substring stock
@bp.route("/autocomplete")
def stockList():
    stock = request.args.get('stock')
    client = APIClient()
    tickers = client.get_relevant_stock_tickers(stock)
    data = {'data': tickers}
    return json.dumps(data)