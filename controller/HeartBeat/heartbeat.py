from db.app import db
from flask import request, jsonify

def get_all():
    if request.method == 'GET':
        mycol = db['Heartbeat']
        try:
            result = mycol.find({})
            
            data = []
            for document in result:
                document['_id'] = str(document['_id'])  
                data.append(document)
            return jsonify(data)
        except Exception as e:
            return jsonify({'error': str(e)})


def add_heartbeat():
    if request.method == 'POST':
        mycol = db['Heartbeat']
        data = request.get_json()

        IR = data.get('IR')
        BPM = data.get('BPM')
        AvgBPM = data.get('AvgBPM')
        ECG = data.get('ECG')

        try:
            post = {
                "IR": IR,
                "BPM": BPM,
                "AvgBPM": AvgBPM,
                "ECG": ECG,
            }
            result = mycol.insert_one(post)  # Use insert_one for single document insertion

            print("Data inserted with record id", result.inserted_id)
            return jsonify({'message': 'Data inserted successfully!'})

        except Exception as e:
            return jsonify({'error': str(e)})
