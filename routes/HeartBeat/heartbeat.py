# from flask import Blueprint, request
# from controller.HeartBeat.heartbeat import add_heartbeat, get_all

# heartbeat_route = Blueprint('heartbeat_route', __name__)

# @heartbeat_route.route('/heartbeats' , methods = ['GET'])
# def get_all_heartbeat():
#     return get_all()

# @heartbeat_route.route('/add-heartbeat', methods=['POST'])
# def add_heartbeat_values():
#     print("Request received:", request.json)
#     return add_heartbeat()