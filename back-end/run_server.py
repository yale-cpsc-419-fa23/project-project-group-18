from flask import Flask, jsonify, request
from flask_cors import CORS
from api_services import socketio, app


# app = Flask(__name__)
# CORS(app)
# socketio = flask_socketio.SocketIO(app, cors_allowed_origins="*")
# @socketio.on('join')
# def on_join(data):
#     room = data
#     print(1)
#     print(data)
#     print(2)
#     flask_socketio.join_room(room)  
#     flask_socketio.send("You have joined the room: " + room, room=room)  


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
