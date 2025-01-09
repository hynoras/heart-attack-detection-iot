from flask import request, jsonify
import requests
import time
from db.mysqlconfig import db
from utils.logger import Logger


logger = Logger('diagnosis.py')

class DataSender:
    @staticmethod
    def send_to_predict_api():
        if request.method == 'POST':
            scheduled_receiver_api = 'http://127.0.0.1:5000/api/add-sensor-data'

            data = request.get_json()
            
            id = data.get('unique_id')
            BPM = data.get('thalachh')
            ECG = data.get('restecg')

        try:
            sensor_data = {
                "id": id,
                "thalachh": BPM,
                "restecg": ECG,
            }

            requests.post(scheduled_receiver_api, json=sensor_data)

            return jsonify({
                "status:": "success"
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)})
        
    @staticmethod
    def send_to_diagnose():
        time.sleep(2)
        if request.method == 'POST':
            manual_receiver_api = 'http://127.0.0.1:5000/api/patient/manual/receive-sensor-data'

            data = request.get_json()
            
            BPM = data.get('thalachh')
            ECG = data.get('restecg')

        try:
            sensor_data = {
                "thalachh": BPM,
                "restecg": ECG,
            }

            requests.post(manual_receiver_api, json=sensor_data)
            return jsonify({"status": "success"}), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def add_sensor_data():
        data = request.get_json()
        required_fields = ['unique_id', 'thalachh', 'restecg']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        cur = db.cursor()
        try:
            cur.execute(
                'INSERT INTO sensor_data (device_id, thalachh, restecg) VALUES (%s, %s, %s)',
                (data['unique_id'], data['thalachh'], data['restecg'])
            )
            db.commit()
            return jsonify({"message": "Data stored successfully"}), 200
        except Exception as e:
            db.rollback()
            logger.error(f'An error occurred: {e}')
            return jsonify({"error": str(e)}), 500
        finally:
            cur.close()
