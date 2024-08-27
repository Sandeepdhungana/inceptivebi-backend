from flask import Flask, request, jsonify, Blueprint
from flask_socketio import SocketIO
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

def simulate_file_processing():
    """Simulate file processing."""
    count = 0
    while count < 10:
        socketio.sleep(2)
        count += 1
        socketio.emit('file_upload_response', {'message': f'Processing... {count * 10}% complete'})
    socketio.emit('file_upload_response', {'message': 'File processing completed'})

@socketio.on('start_processing')
def handle_start_processing(data):
    print('Received start_processing:', data)
    threading.Thread(target=simulate_file_processing).start()

@upload_bp.route('/upload', methods=['POST'])
def upload_and_forward():

    socketio.emit('file_upload_response', {'message': 'File received, starting processing...'})
    socketio.start_background_task(simulate_file_processing)

    return jsonify({'message': 'File upload initiated'}), 202


