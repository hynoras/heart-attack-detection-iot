from flask import request, jsonify
import requests, time, threading
from db.mysqlconfig import db
from utils.logger import Logger


logger = Logger('diagnosis.py')

class DataSender:
    @staticmethod
    def send_to_predict():
        manual_url = 'http://127.0.0.1:5000/api/patient/manual/receive-sensor-data'
        data = request.get_json()
        
        BPM = data.get('thalachh')
        ECG = data.get('restecg')

        try:
            response = DataSender.add_sensor_data(data)
            if response[1] != 200:
                return response
            sensor_data = {
                "thalachh": BPM,
                "restecg": ECG,
            }

            requests.post(manual_url, json=sensor_data)
            logger.info('Send data to main server successfully!')

            return jsonify({"message": "Data stored and sent successfully"}), 200
        except Exception as e:
            db.rollback()
            logger.error(f'An error occurred: {e}')
            return jsonify({"error": str(e)}), 500
        
    def add_sensor_data(data):
        required_fields = ['unique_id', 'thalachh', 'restecg', 'AvgBPM']
        missing_fields = [field for field in required_fields if field not in data]
        data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')  

        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        cur = db.cursor()
        try:
            cur.execute(
                'INSERT INTO sensor_data (device_id, thalachh, restecg, avg_bpm, timestamp) VALUES (%s, %s, %s, %s, %s)',
                (data['unique_id'], data['thalachh'], data['restecg'], data['AvgBPM'], data['timestamp'])
            )
            db.commit()
            return jsonify({"message": "Data stored successfully"}), 200
        except Exception as e:
            db.rollback()
            logger.error(f'An error occurred: {e}')
            return jsonify({"error": str(e)}), 500
        finally:
            cur.close()

