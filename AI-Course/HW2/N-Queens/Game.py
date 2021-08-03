import MinConflicts as MC
import NQueens as NQ
import colorama


def main():
    n = int(input("Enter n: (n is size of the board like 4) \n"))

    game = NQ.NQueens(n)

    max_steps = 100000

    result, count = MC.minConflicts(game, max_steps)

    if result != None:
        print(colorama.Fore.GREEN + f"WOW! We found a solution for this board in {count} steps: \n" + colorama.Style.RESET_ALL)
        game.show_board(result.board)

    else:
        print(colorama.Fore.RED + f"Oops! No solution.\n(Max steps = {max_steps})" + colorama.Style.RESET_ALL)

main()