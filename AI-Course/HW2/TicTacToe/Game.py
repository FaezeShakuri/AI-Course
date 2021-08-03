import Board as tictactoe
import colorama
import time

def main():
    # Initialize TicTacToe
    game = tictactoe.Game()

    # Set board
    board = game._board

    # Set state
    state = game._state

    # at first, AI turn is false
    AI_turn = False


    print(f"   -- TicTacToe --  \n")
    
    print(f"X or O ?")
    user = str(input()).upper()

    if user == tictactoe.X:
        print(f"Your player -> {colorama.Fore.BLUE + tictactoe.X + colorama.Style.RESET_ALL}\nAI player   -> {colorama.Fore.RED + tictactoe.O + colorama.Style.RESET_ALL}\n")

    elif user == tictactoe.O:
        print(f"Your player -> {colorama.Fore.RED + tictactoe.O + colorama.Style.RESET_ALL}\nAI player   -> {colorama.Fore.BLUE + tictactoe.X + colorama.Style.RESET_ALL}\n")

    while True:

        # Get the player
        player = game.to_move(board)

        # If game is over
        _state, _winner = game.winner(board)
        if _state:
            if _winner == tictactoe.Tie:
                print(colorama.Fore.GREEN + f"{tictactoe.Tie}." + colorama.Style.RESET_ALL)
            
            else:
                print(colorama.Fore.GREEN + f"{_winner} won." + colorama.Style.RESET_ALL)
            
            break

        if player != user:
            if AI_turn:
                print(colorama.Fore.YELLOW + f"AI is thinking..." + colorama.Style.RESET_ALL)
                time.sleep(1)

                # Calls minimax algorithm
                move = game.alpha_beta_search(board, state)

                # Makes a action 
                board = game.result(board, move)

                # Print board
                game.print_board(board)

                AI_turn = False

            else:
                # AI turn
                print(f"   -- AI turn --  ")

                AI_turn = True
        
        elif player == user:
            
            # User turn
            print(f"   -- Your turn --  ")

            print(f"Enter i and j")

            print(f"i:")
            i = int(input())

            print("j:")
            j = int(input())
            
            if board[i][j] == None:
                board = game.result(board, (i, j))
            
            # Print board
            game.print_board(board)


main()