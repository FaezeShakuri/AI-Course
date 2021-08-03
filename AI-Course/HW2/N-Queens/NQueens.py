import random
import colorama


QUEEN = ' * '
CELL  = ' - '

class NQueens:
    def __init__(self, sizeOfBoard):
        global CELL

        # n is size of board
        self.n = sizeOfBoard

        self.board = [self.n * [CELL] for _ in range(self.n)]

        # Position of queens
        self.queens = []
    

    def transpose(self, board):
        return [[row[i] for row in board] for i in range(len(board[0]))]


    def show_board(self, board):
        global QUEEN

        for row in self.transpose(board):
            for cell in row:
                if cell == QUEEN:
                    print(colorama.Fore.YELLOW + cell + colorama.Style.RESET_ALL, end = " ")
                else:
                    print(cell, end = " ")
            print("\n")
        print()


    def is_queen(self, q):
        """
        Checks the q is in queens list or not.

        :param q: a queen like (row, index of queen)
        :return: True or False
        """

        if q not in self.queens:
            return False
        
        return True


    def set_random_queens(self):
        """
        Sets a random queen in each row of the board.
        :return: 
        """

        global QUEEN

        # tmpBoard is transpose of board
        # tmpBoard = self.transpose(self.board)

        for i in range(self.n):

            # Gets a random index for queen
            queenIndex = random.randint(0, self.n - 1)

            # Sets ' * ' as queen in board
            self.board[i][queenIndex] = QUEEN

            # Adds position of random queen
            self.queens += [(i, queenIndex)]


    def get_random_gueen(self):
        """
        :return: A random queen
        """

        # Gets a random index for queen
        queenIndex = random.randint(0, self.n - 1)

        # Return the position of random queen
        return self.queens[queenIndex]


    def conflicts(self, q):
        """
        Checks the queen is under attack or it is safe and counts the number of attacks

        :param q: A queen -> (row, index of queen)
        :return: A tuple  -> (True or False, number of attacks)
        """

        _row, _index = q

        # Number of attacks
        count = 0

        # Check in row
        for q2 in self.queens:
            row, index = q2
            if row == _row and index != _index:
                count += 1
        
        # Check in column
        for q2 in self.queens:
            row, index = q2
            if row != _row and index == _index:
                count += 1

        # Check in diagonal
        for q2 in self.queens:
            row, index = q2
            if q2 != q and abs(row - _row) == abs(index - _index):
                count += 1

        if count == 0:
            # No conflicts
            return False, 0

        else:
            return True, count


    def terminal(self):
        """
        Checks the board to make sure that all queens are safe.

        :return: True or False
        """

        for q in self.queens:
            if self.conflicts(q)[0]:
                return False
        
        return True


    def result(self, current, new):
        """
        Moves a queen from current position to new position.

        :param current: Current position of queen
        :param new:     New position of queen
        :return: 
        """

        if not self.is_queen(current):
            return -1
        
        # Remove current queen
        self.queens.remove(current)
        self.board[current[0]][current[1]] = ' - '

        # Add new queen
        self.queens += [new]
        self.board[new[0]][new[1]] = ' * '

        return 1

    
    def actions(self, q):
        """
        Finds all possible positions that the q can go

        :param q: A queen -> (row, index of queen)
        :return:  List of positions
        """
        _row, _index = q
        acts = []
        
        for i in range(self.n):
            acts += [(_row, i)]

        return acts