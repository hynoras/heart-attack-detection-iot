import threading
from flask import Blueprint, request, jsonify
from controller.Diagnosis.diagnosis import DataSender


diagnosis_route = Blueprint('diagnosis_route', __name__)

@diagnosis_route.route('/send-to-predict-api', methods=['POST'])
def send_to_predict():
    return DataSender.send_to_predict()

@diagnosis_route.route('/send-to-diagnose', methods=['POST'])
def send_to_diagnose():
    return DataSender.send_to_diagnose()
# def send_to_diagnose_endpoint():
#     try:
#         data = request.get_json()

#         send_to_diagnose = threading.Thread(target=DataSender.send_to_diagnose, args=(data,))
#         send_to_diagnose.daemon = True
#         send_to_diagnose.start()
#         print("Threads started successfully")
#         return jsonify({"message": "Threads started successfully"}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@diagnosis_route.route('/add-sensor-data', methods=['POST'])
def store_sensor_data():
    return DataSender.add_sensor_data()
