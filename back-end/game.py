from abc import ABC, abstractmethod

class Game(ABC):
    def __init__(self):
        
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    @abstractmethod
    def make_move(self, *args):
        # get move information, update state
        pass
    
    
    @abstractmethod
    def check_winner(self):
        pass
        


class TicTacToe(Game):
    def __init__(self):
        super().__init__()
        self.current_state = [['', '', ''], ['', '', ''], ['', '', '']]
        self.current_turn = 'O'

    def set_players(self, player1, player2):
        self.player_map = {
            player1 : 'O',
            player2 : 'X'
        }
        
        self.piece_map = {
            'O' : player1,
            'X' : player2
        }
    
    def make_move(self, player, index):
        if self.check_move_validate:
            self.current_state[index // 3][index % 3] = self.player_map[player]
            self.next_turn()
        else:
            raise ValueError('The move is not valid')
    
    def get_current_turn(self):
        return self.current_turn

    def next_turn(self):
        self.current_turn = 'X' if self.current_turn == 'O' else 'O'

    def check_move_validate(self, player, move):
        return True

    def check_tie(self):
        print(self.current_state)
        for row in self.current_state:
            for cell in row:
                if cell == '':
                    return False
        
                
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
    
    def get_player_piece_map(self):
        return self.player_map
    
    def game_over(self):
        self.current_state = [['', '', ''], ['', '', ''], ['', '', '']]
        self.current_turn = 'O'



class Gomoku(Game):
    def __init__(self, board_size=15):
        super().__init__()
        self.board_size = board_size
        self.current_state = [['' for _ in range(board_size)] for _ in range(board_size)]
        self.current_turn = 'Black'

    def set_players(self, player1, player2):
        self.player_map = {player1: 'Black', player2: 'White'}
        self.piece_map = {'Black': player1, 'White': player2}

    def make_move(self, player, index):
        if self.check_move_validate:
            self.current_state[index // self.board_size][index % self.board_size] = self.player_map[player]
            self.next_turn()
        else:
            raise ValueError('The move is not valid')
        
    def get_current_turn(self):
        return self.current_turn

    def next_turn(self):
        self.current_turn = 'Black' if self.current_turn == 'White' else 'White'

    def check_move_validate(self, player, move):
        return True

    def check_winner(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.current_state[row][col] != '' and self.check_directions_for_winner(row, col):
                    return self.piece_map[self.current_state[row][col]]
        return None

    def check_directions_for_winner(self, row, col):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # horizontal, vertical, diagonal_down, diagonal_up
        for dr, dc in directions:
            if self.count_consecutive_pieces(row, col, dr, dc) >= 5:
                return True
        return False

    def count_consecutive_pieces(self, row, col, dr, dc):
        piece_type = self.current_state[row][col]
        count = 1
        for _ in range(1, 5):
            row += dr
            col += dc
            if 0 <= row < self.board_size and 0 <= col < self.board_size and self.current_state[row][col] == piece_type:
                count += 1
            else:
                break
        return count

    def check_tie(self):
        return all(cell != '' for row in self.current_state for cell in row)

    def get_state(self):
        return {'board': self.current_state, 'players': self.players}
    
    def get_player_piece_map(self):
        return self.player_map

    def game_over(self):
        self.current_state = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_turn = 'Black'