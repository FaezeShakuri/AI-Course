import math
import copy
import numpy
import colorama
from enum import Enum

# Size of board
SIZE = 3

# Players
X = "X"
O = "O"

# States
Tie = "Tie"
NoWinner = "None"

# Scores
class Score(Enum):
    win = 1
    lose = -1
    tie = 0


class Game:
    
    def __init__(self):
        self._state = NoWinner
        self._board =  [[None, None, None], [None, None, None], [None, None, None]]


    def print_board(self, board):
        global X, O


        print(f"i/j 0     1     2")
        i = 0
        for row in board:
            print(i, end = " ")
            i += 1

            for c in row: 
                if c == None:
                    print(colorama.Fore.LIGHTBLACK_EX + f"( . )" + colorama.Style.RESET_ALL, end = " ")

                elif c == X:
                    print(colorama.Fore.LIGHTBLACK_EX + "( " + colorama.Style.RESET_ALL, end = "")
                    print(colorama.Fore.BLUE          +   X  + colorama.Style.RESET_ALL, end = "")
                    print(colorama.Fore.LIGHTBLACK_EX + " )" + colorama.Style.RESET_ALL, end = " ")
                
                elif c == O:
                    print(colorama.Fore.LIGHTBLACK_EX + "( " + colorama.Style.RESET_ALL, end = "")
                    print(colorama.Fore.RED           +   O  + colorama.Style.RESET_ALL, end = "")
                    print(colorama.Fore.LIGHTBLACK_EX + " )" + colorama.Style.RESET_ALL, end = " ")
                
                else:
                    print("Error")
            
            print("\n")


    def actions(self, board):
        """
        Finds the all possible moves. possible moves are the None items in board.

        :return: List of all possible actions
        """

        actions = []

        for item in range(SIZE):
            for sub_item in range(len(board[item])):
                action = (item, sub_item)

                # If this cell is empty, it can be an action
                if board[item][sub_item] == None:
                    actions += [action]

        return actions


    def to_move(self, board):
        """
        Indicates that who has the next turn, X or O.

        :return: Player who has the next turn
        """

        X_count = 0
        O_count = 0

        for item in board:
            X_count += item.count(X)
            O_count += item.count(O)

        if X_count > O_count:
            return O

        elif X_count == O_count:
            return X

        return None


    def result(self, board, action):
        """
        Makes a move in board with action.

        :param action:
        :return:
        """

        new_board = copy.deepcopy(board)
        player = self.to_move(board)
        # if player == None:
        #     print("None player")
        new_board[action[0]][action[1]] = player

        return new_board


    def tmp_winner(self, board):
        """
        Indicates the winner in a row of board.
        :return: The winner
        """
        
        global X, O, SIZE

        # Checks in row
        for item in board:
            c_x = 0
            c_o = 0
        
            for sub_item in item:
                if sub_item == X:
                    c_x += 1

                elif sub_item == O:
                    c_o += 1

            if c_x == SIZE:
                return (True, X)

            elif c_o == SIZE:
                return (True, O)
        
        return (False, None)


    def winner(self, board):
        """
        Indicates the winner of the game
        :return: state, the winner
        """

        global Tie, NoWinner

        # Check in row
        state, _winner = self.tmp_winner(board)
        if _winner != None:
            return (state, _winner)
        
        # tmp_board is transpose of the main board
        tmp_board = [[row[i] for row in board] for i in range(len(board[0]))]
        
        # Check in column
        state, _winner = self.tmp_winner(tmp_board)
        if _winner != None:
            return (state, _winner)
        
        # Check in diagonal
        diagonal_lst_1 = []
        for i in range(SIZE):
            diagonal_lst_1 += [board[i][i]]

        diagonal_lst_2 = []
        for i in range(SIZE):
            diagonal_lst_2 += [board[i][SIZE - 1 - i]]

        state, _winner = self.tmp_winner([diagonal_lst_1, diagonal_lst_2])
        if _winner != None:
            return (state, _winner)

        # not terminal
        for row in board:
            for c in row:
                if c == None:
                    return (False, NoWinner)
        
        # Tie
        return (True, Tie)


    def tmp_terminal(self, board):
        """
        Checks there is None cell in board or not.
        :return: True or False
        """

        for i in range(SIZE):
            for si in board[i]:
                if si == None:
                    return True

        return False


    def is_terminal(self, board):
        """
        Checks the game is over or not.
        :return: True or False
        """

        global Tie, NoWinner

        return self.winner(board)[0]


    def utility(self, board):
        """
        :return: 1 if winner is X, -1 if winner is O, 0 otherwise
        """

        global X, O, Score

        state, _winner = self.winner(board)

        if _winner == X:
            return Score.win.value

        elif _winner == O:
            return Score.lose.value

        else:
            return Score.tie.value


    def max_value(self, board, state, alpha, beta):
        """
        Maximixes between 2 nodes.

        :param alpha:
        :param beta:
        :return: a (value, action) pair
        """

        if self.is_terminal(board):
            return self.utility(board), None

        v = - math.inf

        for act in self.actions(board):
            v2, a2 = self.min_value(self.result(board, act), state, alpha, beta)
            
            if v >= beta:
                return v, act
                
            if v2 > v:
                v, move = v2, act
                alpha = max(alpha, v)
            
        return v, move


    def min_value(self, board, state, alpha, beta):
        """
        Minimizes between 2 nodes.

        :param alpha:
        :param beta:
        :return: a (value, action) pair
        """

        if self.is_terminal(board):
            return self.utility(board), None

        v = math.inf

        for act in self.actions(board):
            v2, a2 = self.max_value(self.result(board, act), state, alpha, beta)

            if v <= alpha:
                return v, act

            if v2 < v:
                v, move = v2, act
                beta = min(beta, v)            

        return v, move


    def alpha_beta_search(self, board, state):
        """
        Alpha-Beta Search

        :return: An action
        """

        global X, O

        if self.to_move(board) == X:
            value, move = self.max_value(board, state, -math.inf, math.inf)

        else:
            value, move = self.min_value(board, state, -math.inf, math.inf)

        return move
