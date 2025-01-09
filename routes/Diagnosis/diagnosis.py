from flask import Blueprint
from controller.Diagnosis.diagnosis import DataSender

diagnosis_route = Blueprint('diagnosis_route', __name__)

@diagnosis_route.route('/send-to-predict-api', methods=['POST'])
def add_heartbeat_values():
    return DataSender.send_to_predict_api()

@diagnosis_route.route('/send-to-diagnose', methods=['POST'])
def send_to_diagnose_endpoint():
    return DataSender.send_to_diagnose()

@diagnosis_route.route('/add-sensor-data', methods=['POST'])
def store_sensor_data():
    return DataSender.add_sensor_data()