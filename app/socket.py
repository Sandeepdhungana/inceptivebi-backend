# app/socket_config.py

from flask_socketio import SocketIO

# Initialize SocketIO without an app
socketio = SocketIO(cors_allowed_origins="*")
