from flask import Flask, render_template, request
from api_client import APIClient

app = Flask(__name__)

@app.route('/')
def root():
    return 'Bruh bruh bruh'

@app.route('/lookup', methods=('GET', 'POST'))
def lookup():

    # On search: 
    # If it's a ticker, show the stock
    # If it's not a ticker, search for the company with the API and present a list of options
    if request.method == 'POST':
        search = request.form['stock-search']
        client = APIClient()
        is_stock = client.is_a_stock_ticker(search)
        if is_stock:
            return "'tis a stock"
        else:
            return str(client.seach_for_ticker(search, max_tick=1000))

    return render_template('lookup.html')

if __name__ == '__main__':
    app.run()
