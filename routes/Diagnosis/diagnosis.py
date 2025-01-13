import threading
from flask import Blueprint, request, jsonify
from controller.Diagnosis.diagnosis import DataSender


diagnosis_route = Blueprint('diagnosis_route', __name__)

@diagnosis_route.route('/send-to-predict-api', methods=['POST'])
def send_to_predict():
    return DataSender.send_to_predict()

@diagnosis_route.route('/add-sensor-data', methods=['POST'])
def store_sensor_data():
    return DataSender.add_sensor_data()
