from aplication_logic import (
    AnotherCounterOnTheSquareError, Board,
    IndexOutOfBoardError, InvalidCounterCoord,
    InvalidMoveError, NotMovedError
)


def beggining_prints(player1_color, player2_color):
    print(f'Player1 has color {player1_color}', '')
    print(f'Player2 has color {player2_color}', '')
    print('Player1 starts the play.')


def taking_user_coords():
    try:
        xc = int(input('Enter the first coord:\t'))
        yc = int(input('Enter the second coord:\t'))
        print('Enter coords of place where you want to move your counter.')
        xm = int(input('Enter the first coord:\t'))
        ym = int(input('Enter the second coord:\t'))
    except ValueError:
        print('Coord must be an integer nubmer. Try again\t')
    counter_coords = (xc, yc)
    move_coords = (xm, ym)
    return counter_coords, move_coords


def end_of_the_game(board: Board):
    if board.who_is_the_winner() is not None:
        winner_color = board.who_is_the_winner()
        winner = 'Player1' if winner_color == player1_color else 'Player2'
        print(f'{winner} has won the game.')


def main():
    board = Board()
    board.who_starts_the_play()

    player1_color = board.moving_player()
    player2_color = 'white' if player1_color == 'black' else 'white'
    beggining_prints(player1_color, player2_color)
    while True:
        if board.moving_player() == player1_color:
            player = 'Player1'
        else:
            player = 'Player2'
        print(f'{player} turn')
        print_the_board(board)
        print('Enter coords of the counter that your want to move.')
        counter_coords, move_coords = taking_user_coords()
        try:
            board.move(counter_coords, move_coords)
        except InvalidCounterCoord:
            print('You typed invalid counter coords.\nTry again.')
            continue
        except NotMovedError:
            print('You need to move the counter during your turn.\n Try again')
            continue
        except IndexOutOfBoardError:
            print('You typed coords out of board.\nTry again.')
            continue
        except AnotherCounterOnTheSquareError:
            print('There is another counter on the pointed square.\nTry again')
            continue
        except InvalidMoveError:
            print('Your move is invalid.\nTry again.')
            continue
        end_of_the_game(board)


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
