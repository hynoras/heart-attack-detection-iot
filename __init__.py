from flask import Flask 
from routes.HeartBeat.heartbeat import heartbeat_route
from routes.Diagnosis.diagnosis import diagnosis_route
from routes.Board.board import board_route
from routes.Dashboard.dashboard import dashboard_route

def create_app():
    app = Flask(__name__)

    url_prefix = '/api'

    app.register_blueprint(heartbeat_route, url_prefix = url_prefix)
    app.register_blueprint(diagnosis_route, url_prefix = url_prefix)
    app.register_blueprint(board_route, url_prefix = url_prefix)
    app.register_blueprint(dashboard_route, url_prefix = url_prefix)



    return app
