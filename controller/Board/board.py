from flask import request, jsonify
from db.mysqlconfig import db
from utils.logger import Logger

logger = Logger('board.py')

def register_device():
    data = request.get_json()
    unique_id = data.get('unique_id')

    cur = db.cursor()
    try:
        cur.execute('SELECT * FROM device WHERE id = %s', (unique_id))
        board = cur.fetchone()

        if board:
            logger.debug("Device already registered")
            return jsonify({"message": "Device already registered"}), 200
        else:
            cur.execute('INSERT INTO device(id) VALUES (%s)', (unique_id))
            db.commit()

            logger.debug(f"Device registered successfully, unique_id: {unique_id}")
            return jsonify({
                "message": "Device registered successfully", 
                "unique_id": unique_id}), 201
        
    except Exception as e:
            db.rollback()
            logger.error(f'Error: {str(e)}')
            return (f'Error: {str(e)}')
    finally:
            cur.close()