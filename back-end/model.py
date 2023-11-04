from enum import Enum
import random
from game import TicTacToe


class GameState(Enum):
    WAITING = 1
    ONGOING = 2
    

class GameRoom:
    def __init__(self, id):
        self.id = id
        self.__player_count = 0
        self.__player_set = set()
        self.__max_player_count = 0
        self.__game_state = GameState.WAITING
        self.__game = TicTacToe(room_id=self.id)
        print(f"Game room {id} created.")
    
    def join_player(self, player):
        if(self.is_join_avilable()):
            self.__player_count += 1
            self.__player_set.add(player)
            print(f"{player} joins the room.")
        else:
            print("Fail to join the room.")

    def leave_player(self, player):
        if(player in self.__player_set):
            self.__player_set.remove(player)
            print(f"{player} leaves the room.")
        else:
            print("Leaving room: error occurs.")


    def is_join_avilable(self):
        if(self.__game_state == GameState.ONGOING):
            print("A game is ongoing in the room.")
            return False
        elif(self.__player_count==self.__max_player_count):
            print("The room is full.")
            return False
        else:
            return True
    
    def to_json(self):
        return {
            "id": self.id,
            "player_count": self.__player_count
        }
    
    def start(self):
        self.__game.set_players(self.__player_set[0], self.__player_set[1])
    
    

class GameRoomManager:
    def __init__(self):
        self.rooms = {}  
        self.room_count = 0  

    def get_room_list(self):
        room_list = list(self.rooms.values())
        return room_list

    def create_new_room(self):
        new_room_id = self.generate_room_id()
        while new_room_id in self.rooms:
            new_room_id = self.generate_room_id()
        
        
        self.rooms[new_room_id] = GameRoom(new_room_id)
            
        self.room_count += 1
        return new_room_id

    
    def remove_room(self, room_id):
        
        if room_id in self.rooms:
            del self.rooms[room_id]
            self.room_count -= 1
    
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
    
    def generate_room_id(self):
        room_number = random.randint(100000, 999999)
        return str(room_number)



    
