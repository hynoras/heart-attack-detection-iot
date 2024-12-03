from flask import request, jsonify
import requests

class DataSender:
    @staticmethod
    def send_to_predict_api():
        if request.method == 'POST':
            predict_api = 'http://127.0.0.1:5000/api/patient/diagnosis'

            data = request.get_json()

            BPM = data.get('BPM')
            ECG = data.get('ECG')

        try:
            sensor_data = {
                "BPM": BPM,
                "ECG": ECG,
            }

            response = requests.post(predict_api, json=sensor_data)
            response_data = response.json
            
            return jsonify({
                "status:": "success",
                "prediction": response_data
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)})
