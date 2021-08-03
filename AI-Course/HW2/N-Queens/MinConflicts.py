import NQueens
import time

def conflicts(game, q, v, current):
    """
    Finds a position for q with minimum of conflicts.

    """

    result = (None, None)
    min_attacks = v

    # act is a position for queen
    for act in current.actions(q):

        # Moves queen to this position -> act
        current.result(q, act)

        # Gets the number of attacks at this postion
        number_of_conflicts = current.conflicts(act)[1]

        # Minimizes the number of attacks
        if number_of_conflicts < min_attacks:
            min_attacks = number_of_conflicts
            result = act

        # Move queen back
        current.result(act, q)
    
    return result
            
            
def minConflicts(game, max_steps):
    """
    min-conflicts algorithm

    :param game: A csp
    :param max_steps: The number of steps allowed before giving up
    """

    # minimum attacks
    v = game.n + 1

    # An initial complete assignment for csp
    current = game
    current.set_random_queens()
    
    # Shows the initial board
    print(f"Initial board with random positions for queens:\n")
    current.show_board(current.board)

    # The number of steps
    count = 0

    # Start of algorithm
    print(f"Compter is thinking...\n")
    time.sleep(1)

    for i in range(max_steps):
        count += 1

        # If current is a solutioon for csp then return current
        if current.terminal():
            return current, count
        
        # A randomly chosen conflcted queen
        var = current.get_random_gueen()
        
        # Minimizes the number of attacks
        value = conflicts(game, var, v, current)

        # Move queen
        current.result(var, value)
    
    return None, count
