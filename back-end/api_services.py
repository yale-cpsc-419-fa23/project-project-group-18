from flask import Flask, jsonify, request
from flask_cors import CORS
import flask_socketio

app = Flask(__name__)
CORS(app)
socketio = flask_socketio.SocketIO(app, cors_allowed_origins="*")



@socketio.on('join')
def on_join(data):
    room = data['room']
    username = data['username']
    flask_socketio.join_room(room)  
    socketio.send(f"{username} have joined the room: {room}", room=room)  

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    
    flask_socketio.leave_room(room)
    socketio.send(f'{username} has left the room.', room=room)

@socketio.on('in_game_action')
def handle_player_action(data):
    username = data['username']
    room = data['room']
    action = data['action']
    
    socketio.send(f'{username} takes action:{action}', room=room)
