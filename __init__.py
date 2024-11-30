from flask import Flask 
from routes.HeartBeat.heartbeat import heartbeat_route

def create_app():
    app = Flask(__name__)

    url_prefix = '/api'

    app.register_blueprint(heartbeat_route, url_prefix = url_prefix)

    return app
