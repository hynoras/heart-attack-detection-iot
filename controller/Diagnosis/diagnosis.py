from flask import request, jsonify
import requests

class DataSender:
    @staticmethod
    def send_to_predict_api():
        if request.method == 'POST':
            # manual_receiver_api = 'http://127.0.0.1:5000/api/patient/manual/receive-sensor-data'
            scheduled_receiver_api = 'http://127.0.0.1:5000/api/patient/scheduled/receive-sensor-data'

            data = request.get_json()

            BPM = data.get('thalachh')
            ECG = data.get('restecg')

        try:
            sensor_data = {
                "thalachh": BPM,
                "restecg": ECG,
            }

            # response_manual = requests.post(manual_receiver_api, json=sensor_data)
            response_scheduled = requests.post(scheduled_receiver_api, json=sensor_data)

            return jsonify({
                "status:": "success"
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)})
