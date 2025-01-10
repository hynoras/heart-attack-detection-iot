from flask import request, jsonify
import random
from datetime import datetime
from bson import ObjectId
from db.app import db


def get_heartbeat():
    try:
        heartbeats = list(db['Heartbeat'].find().sort("timestamp", -1).limit(5))
        heartbeats.reverse()  # Đảo ngược thứ tự từ mới nhất -> cũ nhất

        result = [
            {
                '_id': str(hb['_id']),  
                'IR': hb.get('IR'),
                'BPM': hb.get('BPM'),
                'AvgBPM': hb.get('AvgBPM'),
                'ECG': hb.get('ECG'),
                'timestamp': hb.get('timestamp').isoformat() if hb.get('timestamp') else None, 
            }
            for hb in heartbeats
        ]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_avg_BPM():
    try:
        heartbeats = list(db['Heartbeat'].find().sort("timestamp", -1).limit(1))

        result = [
            {
                'AvgBPM': hb.get('AvgBPM'),
                'timestamp': hb.get('timestamp').isoformat() if hb.get('timestamp') else None, 
            }
            for hb in heartbeats
        ]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def post_heartbeat():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        required_fields = ['IR', 'BPM', 'AvgBPM', 'ECG']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        heartbeat = {
            'IR': data['IR'],
            'BPM': data['BPM'],
            'AvgBPM': data['AvgBPM'],
            'ECG': data['ECG'],
            'timestamp': datetime.now() 
        }

        result = db['Heartbeat'].insert_one(heartbeat)

        return jsonify({'message': 'Data saved successfully', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def generate_random_data():
    return {
        "IR": random.randint(50000, 100000),
        "BPM": round(random.uniform(60.0, 100.0), 2),
        "AvgBPM": round(random.uniform(65.0, 95.0), 2),
        "ECG": round(random.uniform(120, 200), 2),
        "timestamp": datetime.now().isoformat()
    }
