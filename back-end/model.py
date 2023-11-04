from enum import Enum
import random
from game import TicTacToe


class GameState(Enum):
    WAITING = 1
    ONGOING = 2

game_type_mapping = {
    "tic-tac-toe": TicTacToe,
}
    

class GameRoom:
    def __init__(self, id, type):
        self.id = id
        self.__player_count = 0
        self.__player_list = []
        self.__max_player_count = 2
        self.__game_state = GameState.WAITING
        self.game = game_type_mapping[type]()
        print(f"Game room {id} created.")
    
    def join_player(self, player):
        if self.is_join_available():
            self.__player_count += 1
            self.__player_list.append(player)
            print(f"{player} joins the room {self.id}.")
        else:
            print("Fail to join the room.")

    def leave_player(self, player):
        if player in self.__player_list:
            self.__player_list.remove(player)
            self.__player_count -=1
            print(f"{player} leaves the room.")
        else:
            print(f"Player {player} is not in room.")

    def is_join_available(self):
        if self.__game_state == GameState.ONGOING:
            print("A game is ongoing in the room.")
            return False
        elif self.__player_count==self.__max_player_count :
            print("The room is full.")
            return False
        else:
            return True
    
    def to_json(self):
        return {
            "room_id": self.id,
            "player_count": self.__player_count
        }
    
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
        self.__game_state = GameState.ONGOING
        self.game.game_over()
    
    
    

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

    def create_new_room(self, game_type):
        new_room_id = self.generate_room_id()
        while new_room_id in self.rooms:
            new_room_id = self.generate_room_id()
        
        
        self.rooms[new_room_id] = GameRoom(new_room_id, game_type)
            
        self.room_count += 1
        return new_room_id
    
    def player_join_room(self, player_id, room_id):
        if(room_id not in self.rooms):
            print(f"Room: {room_id} is not existed.")
            return False
        else:
            room = self.rooms[room_id]
            if(room.is_join_available()):
                room.join_player(player_id)
                return True
            else:
                return False
    
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



    
