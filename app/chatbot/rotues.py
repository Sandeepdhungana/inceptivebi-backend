from flask import Blueprint, request, jsonify
from app.chatbot.models import ChatBot

chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', None)

    if user_message:
        chatbot = ChatBot()
        reply, response = chatbot.chat(user_message)
        intent_name = response['interpretations'][0]['intent']['name']
        if intent_name == 'FallbackIntent':
            return jsonify({
                'message': [{"content": "Our sales team will getback to you at the earliest"}]
            }), 200
        return jsonify({
            'message': reply,
        }), 200

    return jsonify({
        'error': "No user message found."
    }), 400
