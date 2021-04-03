from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def root():
    return 'Bruh bruh bruh'

@app.route('/lookup')
def lookup():
    return render_template('lookup.html')

if __name__ == '__main__':
    app.run()
