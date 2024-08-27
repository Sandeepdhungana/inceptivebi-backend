from app import create_app
from app.socket import socketio 

app = create_app()

if __name__ == '__main__':
    socketio.run(port=5000, app=app, debug=True,host='0.0.0.0')
