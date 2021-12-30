from aplication_logic import Board
from math import sqrt


def ai_turn(board: Board):
    '''
    Make ai turn during the game.
    '''
    if board.turn_number() <= 8:
        begining(board)
    else:
        move(board)


def begining(board: Board):
    '''
    Function makes set of moves on the board
    that are the best to do on the begining of the game.
    '''
    pass


def right_direction(board: Board,
                    counter_coords, move_coords):
    '''
    Cheks if we are moving the counter in the right direction.
    In advantage of the player are only moves in direction of oponent start squares.
    '''
    xc, yc = counter_coords
    xm, ym = move_coords
    delta_x = xm - xc
    delta_y = ym - yc
    player_color = board.moving_player()
    if player_color == 'b':
        if delta_x >= 0 and delta_y >= 0:
            return 'right direction'
        else:
            return 'wrong direction'
    elif player_color == 'w':
        if delta_x <= 0 and delta_y <= 0:
            return 'right direction'
        else:
            return 'wrong direction'


def move(board: Board):
    '''
    Makes the best possible move after the beginig faze of the game.
    '''
    pass


def finding_counters(board: Board):
    '''
    Functions finds coords of all counters on the board.
    Returns two dicts in form {(xc, yc): []},
    one with white counters coords and one with black counters coords
    '''
    white_coords = {}
    black_coords = {}
    board = board.board()
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == 'b':
                black_coords[x, y] = []
            elif board[y][x] == 'w':
                white_coords[x, y] = []
    return black_coords, white_coords


def moves_distances(board: Board):
    '''
    Cheks all the possible moves for every counter and
    append its distance to the dict list {(x, y): ["distances of moves"]}.
    '''
    black_coords, white_coords = finding_counters(board)


    def jump_move_distances(board: Board, counter_coords, color,
                            last_counter_coords=None):
        '''
        Cheks all the possible jump_moves for every counter and
        append its distance to the dict list {(x, y): ["distances of moves"]}.
        '''
        xc, yc = counter_coords
        board = board.board()

        # Cheking all the options of jump_move for the counter
        if (
            xc-2 > -1 and yc-2 > -1 and board[yc-1][xc-1] != 'o' and
            board[yc-2][xc-2] == 'o' and (xc-2, yc-2) != last_counter_coords
        ):
            jump_move_distances(board, (xc-2, yc-2), color, counter_coords)
        if (
            yc-2 > -1 and board[yc-1][xc] != 'o' and board[yc-2][xc] == 'o'
            and (xc, yc-2) != last_counter_coords
        ):
            jump_move_distances(board, (xc, yc-2), color, counter_coords)
        if (
            yc-2 > -1 and xc+2 < 16 and board[yc-1][xc+1] != 'o' and
            board[yc-2][xc+2] == 'o' and (xc+2, yc-2) != last_counter_coords
        ):
            jump_move_distances(board, (xc+2, yc-2), color, counter_coords)
        if (
            xc+2 < 16 and board[yc][xc+1] != 'o' and board[yc][xc+2] == 'o'
            and (xc+2, yc) != last_counter_coords
        ):
            jump_move_distances(board, (xc+2, yc), color, counter_coords)
        if (
            xc+2 < 16 and yc+2 < 16 and board[yc+1][xc+1] != 'o' and
            board[yc+2][xc+2] == 'o' and (xc+2, yc+2) != last_counter_coords
        ):
            jump_move_distances(board, (xc+2, yc+2), color, counter_coords)
        if (
            yc+2 < 16 and board[yc+1][xc] != 'o' and board[yc+2][xc] == 'o'
            and (xc, yc+2) != last_counter_coords
        ):
            jump_move_distances(board, (xc, yc+2), color, counter_coords)
        if (
            xc-2 > -1 and yc+2 < 16 and board[yc+1][xc-1] != 'o' and
            board[yc+2][xc-2] == 'o' and (xc-2, yc+2) != last_counter_coords
        ):
            jump_move_distances(board, (xc-2, yc+2), color, counter_coords)
        if (
            xc-2 < 16 and board[yc][xc-1] != 'o' and board[yc][xc-2] == 'o'
            and (xc-2, yc) != last_counter_coords
        ):
            jump_move_distances(board, (xc-2, yc), color, counter_coords)

        # if color == 'black':
        #     black_coords[]

    for counter_coords in black_coords.keys():
        jump_move_distances(board, counter_coords, color='black')


def distance_made(counter_coords, move_coords):
    'Returns what distance you are making in this move.'
    xc, yc = counter_coords
    xm, ym = move_coords
    delta_x = xm - xc
    delta_y = ym - yc
    distance = round(sqrt(delta_x**2 + delta_y**2), 1)
    return distance
