from aplication_logic import (
    AnotherCounterOnTheSquareError,
    Board,
    IndexOutOfBoardError,
    InvalidCounterCoord,
    InvalidMoveError,
    NotMovedError,
)
from ai_player import ai_turn
import time


def beggining_prints(player1_color, player2_color):
    "Prints information about which player have which color."
    print(f"Player1 has color {player1_color}", "")
    print(f"Player2 has color {player2_color}", "")
    print("Player1 starts the play.")


def taking_user_coords():
    print("Enter coords of the counter that your want to move.")
    xc = int(input("Enter the first coord:\t"))
    yc = int(input("Enter the second coord:\t"))
    print("Enter coords of place where you want to move your counter.")
    xm = int(input("Enter the first coord:\t"))
    ym = int(input("Enter the second coord:\t"))

    counter_coords = (xc, yc)
    move_coords = (xm, ym)
    return counter_coords, move_coords


def end_of_the_game(board: Board, player1_color):
    "Cheks if the game is finished."
    if board.who_is_the_winner() is not None:
        winner_color = board.who_is_the_winner()
        winner = "Player1" if winner_color == player1_color else "Player2"
        print(f"{winner} has won the game.")
        print_the_board(board)
        return True
    else:
        return False


def who_is_which_player(moving_color, player_color):
    "Cheks which player starts the game."
    if moving_color == player_color:
        player = "Player1"
    else:
        player = "Player2"
    return player


def who_is_ai_player(color):
    "Cheks which player Player1 or Player2 is ai."
    if color == "black":
        print("Player1 is ai")
        ai = True
    else:
        print("Player2 is ai")
        ai = False
    return ai


def game_mode():
    """Enable chosing game mode.
    Human vs human, ai vs human or ai vs ai"""
    mode = ""
    while mode != "1" and mode != "2" and mode != "3":
        info = """Select game mode human vs human, ai vs human, ai vs ai.
1. human vs human
2. ai vs human
3. ai vs ai
Type the mode you want to select.\n"""
        mode = input(info)
        if mode != "1" and mode != "2" and mode != "3":
            print("You chosed invalid option.")
    return mode


def human_game(board: Board, player1_color):
    """
    Loop with human vs human game mode.
    """
    while True:
        moving_color = board.moving_player()
        player = who_is_which_player(moving_color, player1_color)
        print(f"{player} turn")
        print_the_board(board)
        try:
            counter_coords, move_coords = taking_user_coords()
            board.move(counter_coords, move_coords)
        except UnboundLocalError and ValueError:
            print("Coord must be an integer nubmer. Try again\t")
        except InvalidCounterCoord:
            print("You typed invalid counter coords.\nTry again.")
            continue
        except NotMovedError:
            print("You need to move the counter during your turn.\n Try again")
            continue
        except IndexOutOfBoardError:
            print("You typed coords out of the board.\nTry again.")
            continue
        except AnotherCounterOnTheSquareError:
            print("There is another counter on the pointed square.\nTry again")
            continue
        except InvalidMoveError:
            print("Your move is invalid.\nTry again.")
            continue

        if end_of_the_game(board, player1_color):
            break


def ai_human_game(board: Board, player1_color):
    "Ai vs human game mode."
    ai = who_is_ai_player(player1_color)
    while True:
        if board.moving_player() == player1_color:
            player = "Player1"
        else:
            player = "Player2"
        print(f"{player} turn")
        print_the_board(board)
        if ai is False:
            try:

                counter_coords, move_coords = taking_user_coords()
                board.move(counter_coords, move_coords)
            except UnboundLocalError and ValueError:
                print("Coord must be an integer nubmer. Try again\t")
            except InvalidCounterCoord:
                print("You typed invalid counter coords.\nTry again.")
                continue
            except NotMovedError:
                print(
                    "You need to move the counter during your turn.\nTry again"
                )
                continue
            except IndexOutOfBoardError:
                print("You typed coords out of the board.\nTry again.")
                continue
            except AnotherCounterOnTheSquareError:
                print(
                    "There is another counter on the pointed square.\nTry again"
                )
                continue
            except InvalidMoveError:
                print("Your move is invalid.\nTry again.")
                continue
            ai = True
        else:
            print("Ai turn")
            time.sleep(3)
            ai_turn(board)
            ai = False

        if end_of_the_game(board, player1_color):
            break


def ai_game(board: Board, player1_color):
    "Ai vs ai game mode."
    while True:
        # board._board = BOARD_TEST
        if board.moving_player() == player1_color:
            player = "Player1"
        else:
            player = "Player2"
        print(f"{player} turn")
        print_the_board(board)
        ai_turn(board)
        time.sleep(1)

        if end_of_the_game(board, player1_color):
            break


def main():
    "Main function of the interface module."
    board = Board()
    mode = game_mode()
    player1_color = board.moving_player()
    player2_color = "white" if player1_color == "black" else "white"
    beggining_prints(player1_color, player2_color)
    if mode == "1":
        human_game(board, player1_color)
    elif mode == "2":
        ai_human_game(board, player1_color)
    else:
        ai_game(board, player1_color)


def print_the_board(board: Board):
    "Prints the board with counter."
    i = 0
    print("    ", end="")
    for element in range(0, 16):
        if element <= 9:
            print(element, end="  ")
        else:
            print(element, end=" ")
    print("\t")
    for row in board.board():
        if i <= 9:
            print(" " + str(i), end="  ")
        else:
            print(i, end="  ")
        for element in row:
            print(element, end="  ")
        print("\n")
        i += 1


if __name__ == "__main__":
    main()
