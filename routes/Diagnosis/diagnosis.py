from flask import Blueprint
from controller.Diagnosis.diagnosis import DataSender

diagnosis_route = Blueprint('diagnosis_route', __name__)

@diagnosis_route.route('/send-to-predict-api', methods=['POST'])
def add_heartbeat_values():
    return DataSender.send_to_predict_api()