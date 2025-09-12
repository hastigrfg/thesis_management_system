from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys

# اضافه کردن مسیر src به sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.services.auth_service import AuthService
from src.services.student_service import StudentService
from src.services.professor_service import ProfessorService
from src.services.messaging_service import MessagingService

app = Flask(__name__)
CORS(app)

# سرویس‌ها
auth_service = AuthService()
student_service = StudentService()
professor_service = ProfessorService()
messaging_service = MessagingService()

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = auth_service.login(data['user_id'], data['password'])
        if user:
            return jsonify({
                'success': True,
                'user': {
                    'user_id': user.user_id,
                    'name': user.name,
                    'role': user.get_role()
                }
            })
        return jsonify({'success': False, 'message': 'اطلاعات ورود نامعتبر'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/thesis-requests', methods=['GET'])
def get_thesis_requests():
    try:
        professor_id = request.args.get('professor_id')
        requests = professor_service.get_thesis_requests(professor_id)
        return jsonify({'success': True, 'data': requests})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/messages', methods=['GET'])
def get_messages():
    try:
        user_id = request.args.get('user_id')
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        messages = messaging_service.get_user_messages(user_id, unread_only=unread_only)
        return jsonify({'success': True, 'data': [m.to_dict() for m in messages]})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/messages', methods=['POST'])
def send_message():
    try:
        data = request.json
        success, message = messaging_service.send_message(
            data['sender_id'], data['receiver_id'], 
            data['message_type'], data['subject'], data['content'],
            data.get('related_thesis_id')
        )
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
