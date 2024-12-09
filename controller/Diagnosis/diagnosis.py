from flask import request, jsonify
import requests

class DataSender:
    @staticmethod
    def send_to_predict_api():
        if request.method == 'POST':
            sensor_data_receiver_api = 'http://127.0.0.1:5000/api/patient/receive-sensor-data'

            data = request.get_json()

            BPM = data.get('thalachh')
            ECG = data.get('restecg')

        try:
            sensor_data = {
                "thalachh": BPM,
                "restecg": ECG,
            }

            response = requests.post(sensor_data_receiver_api, json=sensor_data)
            response_data = response.json

            return jsonify({
                "status:": "success",
                "prediction": response_data
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)})
