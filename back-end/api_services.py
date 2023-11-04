import time
from model import GameRoomManager
from flask import Flask, jsonify, request
from flask_cors import CORS
import flask_socketio
import uuid

app = Flask(__name__)
CORS(app, origins=["*"], supports_credentials=True)
socketio = flask_socketio.SocketIO(app, cors_allowed_origins="*")

room_manager = GameRoomManager()
#mapping from player_id to room_id
player_manager = {}  
#mapping from sid to player_id
sid_manager = {}

@app.route('/newplayer', methods=['GET'])
def new_player_id():

    player_id = str(uuid.uuid4())
    response = jsonify(success=True, message="New Player ID generated.", player_id=player_id)
    #response.set_cookie('player_id', player_id, samesite='None', secure= True)

    return response

@app.route('/roomlist', methods=['GET'])
def get_room_list():
    room_list = room_manager.get_room_list()
    json_list = []
    for room in room_list:
        json_list.append(room.to_json())
    
    return jsonify(json_list)
        
@app.route('/createroom', methods=['POST'])
def create_new_room():
    player_id = request.form['player_id']
    game_type = request.form['game_type']
    if not player_id:
        response = jsonify(success=False, message="Illegal player ID")
        return response
    
    if player_id in player_manager:
        response = jsonify(success=False, message="Already in a room")
        return response
    
    room_id = room_manager.create_new_room(game_type)
    is_success = room_manager.player_join_room(player_id, room_id)
    if is_success:
        player_manager[player_id] = room_id
        response = jsonify(success=True, message="Create successfully.", room_id=room_id)
    else:
        response = jsonify(success=False, message="Fail to create room")    
    return response


@app.route('/joinroom', methods=['POST'])
def join_room():
    player_id = request.form['player_id']
    room_id = request.form['room_id']
    if not player_id or not room_id:
        response = jsonify(success=False, message="Illegal player_id or room_id")
    else:
        is_success = room_manager.player_join_room(player_id, room_id)
        if is_success:
            player_manager[player_id] = room_id
            response = jsonify(success=True, message="Join successfully.", room_id=room_id)
        else:
            response = jsonify(success=False, message="Fail to join room")

    
    return response
   

@socketio.on('connect')
def handle_connect():
    print('Client connected', request.sid)

@socketio.on('joinroom')
def player_join_room(data):
    player_id = data['player_id']
    room_id = data['room_id']
    sid_manager[request.sid] = player_id
    print(f"{player_id} enter the room {room_id}")
    flask_socketio.join_room(room_id)  
    socketio.emit('joinroom_message', {'is_success': True, 'message': f"{player_id} enter the room {room_id}"}, room=room_id)

    check_game_start(room_id)

@socketio.on('makemove')
def player_make_move(data):
    player_id = data['player_id']
    room_id = data['room_id']
    move = data['index']
    print(f"{player_id}'s move is index:{move}")
    turn_end(room_id, player_id, move)
    
    if check_game_over():
        return
    
    turn_start(room_id)

def check_game_start(room_id):
    room = room_manager.get_room(room_id)
    print(room.to_json())
    if room and room.check_full():
        time.sleep(1)    
        piece_map = room.start_game()
        socketio.emit('gamestart_message', {'piece_map': piece_map, 'message': f"Tic Tac Toe Game Starts"}, room=room_id)
        turn_start(room_id)

def turn_start(room_id):
    room = room_manager.get_room(room_id)
    if room:
        turn = room.game.get_current_turn()
        socketio.emit('turnstart_message', {"turn" : turn, "message" : f"{turn}'s turn starts" }, room=room_id)
    else:
        print(f"No such a room:{room_id}.")

def turn_end(room_id, player_id, move):
    room = room_manager.get_room(room_id)
    if room:
        turn = room.game.get_current_turn()
        room.game.make_move(player_id, move)
        socketio.emit('turnend_message', {"turn" : turn, "index" :move, "message" : f"{turn}'s turn ends" }, room=room_id)
    else:
        print(f"No such a room:{room_id}.")

def check_game_over():
    return

def game_over():
    return
