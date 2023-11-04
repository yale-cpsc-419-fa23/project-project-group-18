from abc import ABC, abstractmethod

class Game(ABC):
    def __init__(self, room_id):
        self.room_id = room_id
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    @abstractmethod
    def make_move(self, *args):
        # get move information, update state
        pass
    
    @abstractmethod
    def update_state(self):
        pass
    
    @abstractmethod
    def check_winner(self):
        pass
        


class TicTacToe(Game):
    def __init__(self, room_id):
        super().__init__(room_id)
        self.current_state = [['', '', ''], ['', '', ''], ['', '', '']]

    def set_players(self, player1, player2):
        self.player_map = {
            player1 : 'X',
            player2 : 'O'
        }
        
        self.piece_map = {
            'X' : player1,
            'O' : player2
        }
    
    def make_move(self, player, index):
        self.current_state[index / 3][index % 3] = self.player_map[player]
    
    def check_move_validate(self, player, move):
        return True

    def check_winner(self):
        board = self.current_state
        # Check rows and columns
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != '':
                return self.piece_map[board[i][0]]
            if board[0][i] == board[1][i] == board[2][i] != '':
                return self.piece_map[board[0][i]]
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != '' or board[0][2] == board[1][1] == board[2][0] != '':
            return self.piece_map[board[1][1]]
        return None  # No winner yet

    def get_state(self):
        return {
            'board': self.current_state,
            'players': self.players
        }