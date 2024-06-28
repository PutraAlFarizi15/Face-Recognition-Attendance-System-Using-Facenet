"""
Flask application for marking attendance in the SQLite attendance system database.
"""

from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    """
    Marks the attendance for a user.
    
    Expects JSON payload with user_id.
    
    Returns:
        JSON response with a success message.
    """
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    timestamp = datetime.now()

    try:
        conn = sqlite3.connect('Database/attendance_system.db')
        c = conn.cursor()

        c.execute("INSERT INTO attendance (user_id, timestamp) VALUES (?, ?)", (user_id, timestamp))
        conn.commit()
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'message': 'Attendance marked successfully'})

if __name__ == '__main__':
    app.run(debug=True)
