from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def root():
    return 'Bruh bruh bruh'

@app.route('/lookup', methods=('GET', 'POST'))
def lookup():

    # On search: 
    # If it's a ticker, show the stock
    # If it's not a ticker, search for the company with the API and present a list of options

    return render_template('lookup.html')

if __name__ == '__main__':
    app.run()
