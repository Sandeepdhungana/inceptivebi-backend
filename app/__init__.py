from flask import Flask
from flask_cors import CORS
from .uploadxml.routes import upload_bp
from .chatbot.rotues import chatbot_bp
from .auth.routes import auth_bp
from .superset.routes import preset_bp
from .socket import socketio

from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from .config import Config
import os


load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    jwt = JWTManager(app)

    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(chatbot_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(preset_bp, url_prefix='/api')



    # Bind the app with SocketIO
    socketio.init_app(app)

    return app
