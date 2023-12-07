import time
from model import GameRoomManager
from flask import Flask, jsonify, request
from flask_cors import CORS
import flask_socketio
import uuid
from db_services import top_n_players, add_player, update_score, user_login, user_register

app = Flask(__name__)
CORS(app, origins=["*"], supports_credentials=True)
socketio = flask_socketio.SocketIO(app, cors_allowed_origins="*")

room_manager = GameRoomManager()
#mapping from player_id to room_id
player_manager = {}  
#mapping from sid to player_id
sid_manager = {}

#test————————————————————————————————
'''
room_id1 = room_manager.create_new_room('Tic-Tac-Toe')
is_success = room_manager.player_join_room('1', room_id1)
is_success = room_manager.player_join_room('2', room_id1)

room_id2 = room_manager.create_new_room('Tic-Tac-Toe')
is_success = room_manager.player_join_room('3', room_id2)


room_id3 = room_manager.create_new_room('Tic-Tac-Toe')
is_success = room_manager.player_join_room('4', room_id3)


room_id4 = room_manager.create_new_room('Tic-Tac-Toe')
is_success = room_manager.player_join_room('5', room_id4)
is_success = room_manager.player_join_room('6', room_id4)

room_id5 = room_manager.create_new_room('Tic-Tac-Toe')
is_success = room_manager.player_join_room('7', room_id5)

@app.route('/testcookies', methods=['POST'])
def testCookies():
    #data = request.json
    #user_id = data['user_id']
    data = request.json
    player_id = data['player_id']
    print(player_id)
    #player_id = request.args.get('player_id')
    response = jsonify(message="Set cookie.")
    response.set_cookie('ijojojioj', player_id)
    return response
#test————————————————————————————————
'''

@app.route('/newplayer', methods=['GET'])
def new_player_id():

    player_id = str(uuid.uuid4())
    print(player_id)
    response = jsonify(success=True, message="New Player ID generated.", player_id=player_id)
    add_player(player_id)
    #response.set_cookie('player_id', player_id, samesite='None', secure= True)

    return response

@app.route('/login', methods=['POST'])
def userlogin():
    data = request.json
    user_id = data['username']
    password = data['password']
    if not user_id or not password:
        response = jsonify(success=False, message="Empty username or password.")
        return response
    print(user_id, password)
    is_success = user_login(user_id, password)
    if is_success:
        response = jsonify(success=True, message="Login successfully.", user_id=user_id)
    else:
        response = jsonify(success=False, message="Wrong username or password.")
    return response

@app.route('/register', methods=['POST'])
def userregister():
    data = request.json
    user_id = data['username']
    password = data['password']
    email = data['email']
    if not user_id or not password or not email:
        response = jsonify(success=False, message="Empty username/password/email address.")
        return response
    print(user_id, password, email)
    is_success = user_register(user_id, password, email)
    if is_success:
        response = jsonify(success=True, message="Register successfully.", user_id=user_id)
    else:
        response = jsonify(success=False, message="Existed username or email.")
    return response


@app.route('/roomlist', methods=['GET'])
def get_room_list():
    room_list = room_manager.get_room_list()
    json_list = []
    for room in room_list:
        json_list.append(room.to_json())
    
    return jsonify(json_list)

@app.route('/leaderboard', methods=['GET'])
def get_leader_board():
    result = top_n_players(10)
    json_list = []
    for row in result:
        json_list.append({'player_id':row[0], 'score':row[1]})

    return jsonify(json_list)
        
@app.route('/createroom', methods=['POST'])
def create_new_room():
    data = request.json
    player_id = data['player_id']
    game_type = data['game_type']
    has_password = data['has_password']
    room_name = data['room_name']
    if not player_id:
        response = jsonify(success=False, message="Illegal player ID")
        return response

    if player_id in player_manager:
        print('xxxx')
        response = jsonify(success=False, message="Already in a room")
        return response

    password = data['password'] if has_password else ""
    room_id = room_manager.create_new_room(room_name, game_type, has_password, password)
    is_success = room_manager.player_join_room(player_id, room_id, password)
    if is_success:
        player_manager[player_id] = room_id
        response = jsonify(success=True, message="Create successfully.", room_id=room_id)
    else:
        response = jsonify(success=False, message="Fail to create room")   
  
    return response


@app.route('/joinroom', methods=['POST'])
def join_room():
    data = request.json
    player_id = data['player_id']
    room_id = data['room_id']
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

@app.route('/joinroompassword', methods=['POST'])
def join_room_with_password():
    data = request.json
    player_id = data['player_id']
    room_id = data['room_id']
    password = data['password']
    if not player_id or not room_id:
        response = jsonify(success=False, message="Illegal player_id or room_id")
    else:
        is_success, message = room_manager.player_join_room(player_id, room_id, password)
        if is_success:
            player_manager[player_id] = room_id
            response = jsonify(success=True, message=message, room_id=room_id)
        else:
            response = jsonify(success=False, message=message)
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
    
    is_over, player_id = check_game_over(room_id)
    if is_over and player_id:
        socketio.emit('gameover_message', {'winner': player_id, 'message': f"{player_id} wins the game."}, room=room_id)
        game_over(room_id)
    elif is_over and player_id=="":
        socketio.emit('gameover_message', {'winner': "", 'message': "Game ties."}, room=room_id)
        game_over(room_id)
    else:   
        turn_start(room_id)

@socketio.on('restart')
def rejoin_game(data):
    player_id = data['player_id']
    room_id = data['room_id']
    print(f"{player_id} is ready for next game.")
    success = player_rejoin(room_id)
    if success:
        socketio.emit('rejoin_message', {'is_success': success, 'message': f"{player_id} is ready for next game."}, room=room_id)
        check_game_start(room_id)
    else:
        socketio.emit('rejoin_message', {'is_success': success, 'message': f"{player_id} fails to rejoin the room."}, room=room_id)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected', request.sid)
    player_id = sid_manager[request.sid]
    room_id = player_manager[player_id]
    room_manager.player_leave_room(player_id, room_id)
    if player_id in player_manager:
        del player_manager[player_id]
    if request.sid in sid_manager:
        del sid_manager[request.sid]




def check_game_start(room_id):
    room = room_manager.get_room(room_id)
    if room and room.check_all_ready():
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

def check_game_over(room_id):
    room = room_manager.get_room(room_id)
    if room:
        winner = room.game.check_winner()
        if winner:
            print(f"{winner} wins the game.")
            update_score(winner)
            return True, winner 
        
        if room.game.check_tie():
            print(f"Game tie.")
            return True, ""
    else:
        print(f"No such a room:{room_id}.")
    return False, ""
    
def player_rejoin(room_id):
    room = room_manager.get_room(room_id)
    if room:
        room.player_rejoin()
        return True
    else:
        print(f"No such a room:{room_id}.")
    return False

def game_over(room_id):
    room = room_manager.get_room(room_id)
    if room:
        room.game_over()
    else:
        print(f"No such a room:{room_id}.")
    return None
