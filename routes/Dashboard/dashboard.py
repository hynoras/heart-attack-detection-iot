from flask import Blueprint
from controller.Dashboard.dashboard import post_heartbeat, get_heartbeat, generate_random_data, get_avg_BPM
import time
import threading
import requests 

dashboard_route = Blueprint('dashboard_route', __name__)

@dashboard_route.route('/heartbeat', methods=['GET'])
def get_heartbeat_data():
    return get_heartbeat()

@dashboard_route.route('/avg-BPM', methods=['GET'])
def get_avg_BPM_data():
    return get_avg_BPM()

@dashboard_route.route('/heartbeat/add', methods=['POST'])
def post_heartbeat_data():
    return post_heartbeat()

# def auto_post_data():
#     while True:
#         data = generate_random_data()  
#         try:
#             response = requests.post("http://127.0.0.1:5000/api/heartbeat/add", json=data)
#             print(f"POST Response: {response.status_code}, {response.json()}")
#         except Exception as e:
#             print(f"Error sending POST request: {e}")
#         time.sleep(60) 

# thread = threading.Thread(target=auto_post_data)
# thread.daemon = True  
# thread.start()
