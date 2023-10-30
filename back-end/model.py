from enum import Enum

class GameState(Enum):
    WAITING = 1
    ONGOING = 2
    

class GameRoom:
    def __init__(self, room_id):
        self.room_id = room_id
        self.__player_count = 0
        self.__player_set = set()
        self.__max_player_count = 0
        self.__game_state = GameState.WAITING
        print("Game room {room_id} created.")
    
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

class GameRoomManager:
    def __init__(self):
        self.rooms = {}  
        self.room_count = 0  

    def create_room(self, room_id):
        # 确保room_id不在字典中，避免覆盖
        if room_id not in self.rooms:
            # 创建Room实例并添加到字典中
            self.rooms[room_id] = GameRoom(room_id)
            # 房间数量加1
            self.room_count += 1
            return True
        else:
            print(f"Room: {room_id} already existed.")
            return False
    
    def remove_room(self, room_id):
        # 如果成功删除，房间数量减1
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
            


    
