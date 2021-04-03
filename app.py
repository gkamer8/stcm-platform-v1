from flask import Flask

app = Flask(__name__)

@app.route('/')
def root():
    return 'Bruh bruh bruh'

if __name__ == '__main__':
    app.run()
