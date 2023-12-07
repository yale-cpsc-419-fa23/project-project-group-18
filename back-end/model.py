from enum import Enum
import random
from game import TicTacToe, Gomoku


class GameState(Enum):
    WAITING = 1
    ONGOING = 2
    END = 3

game_type_mapping = {
    "Tic-Tac-Toe": TicTacToe,
    "Gomoku": Gomoku,
}


class GameRoom:
    def __init__(self, id, room_name, game_type, has_password, password):
        self.id = id
        self.__player_count = 0
        self.__player_list = []
        self.__max_player_count = 2
        self.__game_state = GameState.WAITING
        self.__password = ""
        self.room_name = room_name
        self.game_type = game_type
        self.has_password = has_password
        self.game = game_type_mapping[game_type]()
        if self.has_password:
            self.__password = password
        print(f"Game room {id} created.")
    
    def join_player(self, player):
        message = ""
        if self.is_join_available():
            self.__player_count += 1
            self.__player_list.append(player)
            print(f"{player} joins the room {self.id}.")
            message = f"{player} joins the room {self.id}."
            return True, message
        else:
            print("Fail to join the room.")
            message = "Fail to join the room"
            return False, message
    
    def join_player_with_password(self, player, password):
        message = ""
        if self.is_join_available():
            if password == self.__password:
                self.__player_count += 1
                self.__player_list.append(player)
                print(f"{player} joins the room {self.id}.")
                message = f"{player} joins the room {self.id}."
                return True, message
            else:
                print("Password wrong.")
                message = "Password wrong."
        else:
            print("Fail to join the room.")
            message = "Fail to join the room."
        return False, message

    def leave_player(self, player):
        if player in self.__player_list:
            self.__player_list.remove(player)
            self.__player_count -=1
            print(f"{player} leaves the room.")
            if self.__game_state == GameState.ONGOING:
                self.__game_state = GameState.END
                print(f"Game is eneed because of {player}'s leaving.")

        else:
            print(f"Player {player} is not in room.")

    def is_join_available(self):
        if self.__game_state != GameState.WAITING:
            print("Game is ongoing or ended in this room.")
            return False
        elif self.__player_count==self.__max_player_count :
            print("The room is full.")
            return False
        else:
            return True
    
    def check_full(self):
        return self.__player_count == self.__max_player_count
    
    def check_empty(self):
        return self.__player_count == 0

    def start_game(self):
        print("Game start.")
        self.__game_state = GameState.ONGOING
        self.game.set_players(self.__player_list[0], self.__player_list[1])
        return self.game.get_player_piece_map()
    
    def game_over(self):
        print("Game over.")
        self.__game_state = GameState.END
        self.game.game_over()
    
    def if_has_password(self):
        return self.has_password
    
    def to_json(self):
        return {
            "room_id": self.id,
            "room_name": self.room_name,
            "player_count": self.__player_count,
            "max_player_count": self.__max_player_count,
            "game_type": self.game_type,
            "has_password": self.has_password
        }
    

class GameRoomManager:
    def __init__(self):
        self.rooms = {}  
        self.room_count = 0  

    def get_room_list(self):
        room_list = list(self.rooms.values())
        return room_list
    
    def get_room(self, room_id):
        if room_id in self.rooms:
            return self.rooms[room_id]
        print(f"No room {room_id}")

    def create_new_room(self, room_name, game_type, has_password, password):
        new_room_id = self.generate_room_id()
        while new_room_id in self.rooms:
            new_room_id = self.generate_room_id()
        
        
        self.rooms[new_room_id] = GameRoom(new_room_id, room_name, game_type, has_password, password)
            
        self.room_count += 1
        return new_room_id
    
    def player_join_room(self, player_id, room_id, password = ""):
        message = ""
        if(room_id not in self.rooms):
            print(f"Room: {room_id} is not existed.")
            message = f"Room: {room_id} is not existed."
            return False, message
        else:
            room = self.rooms[room_id]
            if room.if_has_password():
                success, message= room.join_player_with_password(player_id, password)
            else:   
                success, message= room.join_player(player_id)
            return success, message

    
    def player_leave_room(self, player_id, room_id):
        if room_id not in self.rooms:
            print(f"Room: {room_id} is not existed.")
            return False
        else:
            room = self.rooms[room_id]
            room.leave_player(player_id)
            if room.check_empty():
                self.remove_room(room_id)
                print(f"Room {room_id} has been removed.")

    def remove_room(self, room_id):
        if room_id in self.rooms:
            del self.rooms[room_id]
            self.room_count -= 1 
        else:
            print(f"Fail to remove. No room {room_id}")

    def generate_room_id(self):
        room_number = random.randint(100000, 999999)
        return str(room_number)



    
