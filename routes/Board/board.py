from flask import Blueprint
from controller.Board.board import register_device

board_route = Blueprint('board_route', __name__)

@board_route.route('/register-device', methods=['POST'])
def add_heartbeat_values():
    return register_device()