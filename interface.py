import imp
from aplication_logic import (
    AnotherCounterOnTheSquareError, Board,
    IndexOutOfBoardError, InvalidCounterCoord,
    InvalidMoveError, NotMovedError
)
from ai_player import ai_turn
import time
from constants import (
    BOARD_TEST
)


def beggining_prints(player1_color, player2_color):
    print(f'Player1 has color {player1_color}', '')
    print(f'Player2 has color {player2_color}', '')
    print('Player1 starts the play.')


def taking_user_coords():
    xc = int(input('Enter the first coord:\t'))
    yc = int(input('Enter the second coord:\t'))
    print('Enter coords of place where you want to move your counter.')
    xm = int(input('Enter the first coord:\t'))
    ym = int(input('Enter the second coord:\t'))

    counter_coords = (xc, yc)
    move_coords = (xm, ym)
    return counter_coords, move_coords


def end_of_the_game(board: Board, player1_color):
    if board.who_is_the_winner() is not None:
        winner_color = board.who_is_the_winner()
        winner = 'Player1' if winner_color == player1_color else 'Player2'
        print(f'{winner} has won the game.')
        return True
    else:
        return False


def human_game(board: Board, player1_color):
    while True:
        if board.moving_player() == player1_color:
            player = 'Player1'
        else:
            player = 'Player2'
        print(f'{player} turn')
        print_the_board(board)
        print('Enter coords of the counter that your want to move.')
        try:
            counter_coords, move_coords = taking_user_coords()
            board.move(counter_coords, move_coords)
        except UnboundLocalError and ValueError:
            print('Coord must be an integer nubmer. Try again\t')
        except InvalidCounterCoord:
            print('You typed invalid counter coords.\nTry again.')
            continue
        except NotMovedError:
            print('You need to move the counter during your turn.\n Try again')
            continue
        except IndexOutOfBoardError:
            print('You typed coords out of the board.\nTry again.')
            continue
        except AnotherCounterOnTheSquareError:
            print('There is another counter on the pointed square.\nTry again')
            continue
        except InvalidMoveError:
            print('Your move is invalid.\nTry again.')
            continue

        if end_of_the_game(board, player1_color):
            break


def game_mode():
    mode = ''
    while (mode.lower() != 'ai vs human' and mode.lower() != 'human vs human'
           and mode.lower() != 'ai vs ai'):
        info = '''Select if you want to play against normal player or ai player.
Type normal if you chosed normal player or ai if you chosed ai player.\n'''
        mode = input(info)
        if (mode.lower() != 'ai vs human' and mode.lower() != 'human vs human'
           and mode.lower() != 'ai vs ai'):
            print('You chosed invalid option.')
    return mode


def ai_human_game(board: Board, player1_color):
    while True:
        if board.moving_player() == player1_color:
            player = 'Player1'
        else:
            player = 'Player2'
        print(f'{player} turn')
        print_the_board(board)
        print('Enter coords of the counter that your want to move.')
        try:
            counter_coords, move_coords = taking_user_coords()
            board.move(counter_coords, move_coords)
        except UnboundLocalError and ValueError:
            print('Coord must be an integer nubmer. Try again\t')
        except InvalidCounterCoord:
            print('You typed invalid counter coords.\nTry again.')
            continue
        except NotMovedError:
            print('You need to move the counter during your turn.\n Try again')
            continue
        except IndexOutOfBoardError:
            print('You typed coords out of the board.\nTry again.')
            continue
        except AnotherCounterOnTheSquareError:
            print('There is another counter on the pointed square.\nTry again')
            continue
        except InvalidMoveError:
            print('Your move is invalid.\nTry again.')
            continue

        if end_of_the_game(board, player1_color):
            break


def ai_game(board: Board, player1_color):
    while True:
        # board._board = BOARD_TEST
        if board.moving_player() == player1_color:
            player = 'Player1'
        else:
            player = 'Player2'
        print(f'{player} turn')
        print_the_board(board)
        ai_turn(board)
        # time.sleep(3)
        # try:
        #     counter_coords, moai ve_coords = taking_user_coords()
        #     board.move(counter_coords, move_coords)
        # except UnboundLocalError and ValueError:
        #     print('Coord must be an integer nubmer. Try again\t')
        # except InvalidCounterCoord:
        #     print('You typed invalid counter coords.\nTry again.')
        #     continue
        # except NotMovedError:
        #     print('You need to move the counter during your turn.\n Try again')
        #     continue
        # except IndexOutOfBoardError:
        #     print('You typed coords out of the board.\nTry again.')
        #     continue
        # except AnotherCounterOnTheSquareError:
        #     print('There is another counter on the pointed square.\nTry again')
        #     continue
        # except InvalidMoveError:
        #     print('Your move is invalid.\nTry again.')
        #     continue

        if end_of_the_game(board, player1_color):
            break


def main():
    board = Board()
    mode = game_mode()
    player1_color = board.moving_player()
    player2_color = 'white' if player1_color == 'black' else 'white'
    beggining_prints(player1_color, player2_color)
    if mode == 'human vs human':
        human_game(board, player1_color)
    elif mode == 'ai vs human':
        ai_human_game(board, player1_color)
    else:
        ai_game(board, player1_color)


def print_the_board(board: Board):
    i = 0
    print('    ', end='')
    for element in range(0, 16):
        if element <= 9:
            print(element, end='  ')
        else:
            print(element, end=' ')
    print('\t')
    for row in board.board():
        if i <= 9:
            print(' ' + str(i), end='  ')
        else:
            print(i, end='  ')
        for element in row:
            print(element, end='  ')
        print('\n')
        i += 1


if __name__ == '__main__':
    main()
