from flask import Flask
from __init__ import create_app
from flask_cors import CORS

app = Flask(__name__)

app = create_app()

CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
