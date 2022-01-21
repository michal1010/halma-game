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
                    counter_coords, move_coords, player_color):
    '''
    Cheks if we are moving the counter in the right direction.
    In advantage of the player are only moves in direction of
    oponent start squares.
    '''
    xc, yc = counter_coords
    xm, ym = move_coords
    delta_x = xm - xc
    delta_y = ym - yc
    # player_color = board.moving_player()
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
    black_coords = moves_distances(board, 'black')
    max_distances(black_coords)


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


def moves_distances(board_object: Board, color):
    '''
    Cheks all the possible moves for every counter and
    append its distance to the dict list {(x, y): ["distances of moves"]}.
    '''
    black_coords, white_coords = finding_counters(board_object)
    board = board_object.board()
    distance_coords = []
    def jump_move_distances(counter_coords, distances,
                            last_counter_coords=None):
        '''
        Cheks all the possible jump_moves for every counter and
        append its distance to the dict list {(x, y): ["distances of moves"]}.
        '''
        xc, yc = counter_coords

        distance_coords.append(counter_coords)

        # Cheking all the options of jump_move for the counter
        if (
            xc-2 > -1 and yc-2 > -1 and board[yc-1][xc-1] != 'o' and
            board[yc-2][xc-2] == 'o' and (xc-2, yc-2) != last_counter_coords
            and 'right direction' == right_direction(board_object,
                                                     counter_coords, (xc-2, yc-2), 'b')
        ):
            jump_move_distances((xc-2, yc-2), distances, counter_coords)
        if (
            yc-2 > -1 and board[yc-1][xc] != 'o' and board[yc-2][xc] == 'o'
            and (xc, yc-2) != last_counter_coords and
            'right direction' == right_direction(board_object, counter_coords,
                                                 (xc, yc-2), 'b')
        ):
            jump_move_distances((xc, yc-2), distances, counter_coords)
        if (
            yc-2 > -1 and xc+2 < 16 and board[yc-1][xc+1] != 'o' and
            board[yc-2][xc+2] == 'o' and (xc+2, yc-2) != last_counter_coords and
            'right direction' == right_direction(board_object, counter_coords,
                                                 (xc+2, yc-2), 'b')
        ):
            jump_move_distances((xc+2, yc-2), distances, counter_coords)
        if (
            xc+2 < 16 and board[yc][xc+1] != 'o' and board[yc][xc+2] == 'o'
            and (xc+2, yc) != last_counter_coords and
            'right direction' == right_direction(board_object, counter_coords,
                                                 (xc+2, yc), 'b')
        ):
            jump_move_distances((xc+2, yc), distances, counter_coords)
        if (
            xc+2 < 16 and yc+2 < 16 and board[yc+1][xc+1] != 'o' and
            board[yc+2][xc+2] == 'o' and (xc+2, yc+2) != last_counter_coords
            and 'right direction' == right_direction(board_object, counter_coords,
                                                     (xc+2, yc+2), 'b')
        ):
            jump_move_distances((xc+2, yc+2), distances, counter_coords)
        if (
            yc+2 < 16 and board[yc+1][xc] != 'o' and board[yc+2][xc] == 'o'
            and (xc, yc+2) != last_counter_coords and
            'right direction' == right_direction(board_object, counter_coords,
                                                 (xc, yc+2), 'b')
        ):
            jump_move_distances((xc, yc+2), distances, counter_coords)
        if (
            xc-2 > -1 and yc+2 < 16 and board[yc+1][xc-1] != 'o' and
            board[yc+2][xc-2] == 'o' and (xc-2, yc+2) != last_counter_coords
            and 'right direction' == right_direction(board_object, counter_coords,
                                                     (xc-2, yc+2), 'b')
        ):
            jump_move_distances((xc-2, yc+2), distances, counter_coords)
        if (
            xc-2 > -1 and board[yc][xc-1] != 'o' and board[yc][xc-2] == 'o'
            and (xc-2, yc) != last_counter_coords and
            'right direction' == right_direction(board_object, counter_coords,
                                                 (xc-2, yc), 'b')
        ):
            jump_move_distances((xc-2, yc), distances, counter_coords)

        if last_counter_coords is not None and len(distance_coords) > 1:
            max_distance = distance_made(distance_coords[0], distance_coords[-1])
            distances.append(max_distance)
        elif len(distance_coords) == 1:
            distances.append(0)
        distance_coords.clear()

    if color == 'black':
        color_coords = black_coords
    elif color == 'white':
        color_coords = white_coords

    for counter_coords in color_coords.keys():
        distances = []
        jump_move_distances(counter_coords, distances)
        color_coords[counter_coords] = distances.copy()
        distances.clear()

    return color_coords


def max_distances(color_coords: dict):
    '''
    From dict in form {key: [...]} creates
    dict in form {key: max([...])}
    '''
    for key in color_coords.keys():
        color_coords[key] = max(color_coords(key))


def distance_made(counter_coords, move_coords):
    'Returns what distance you are making in this move.'
    xc, yc = counter_coords
    xm, ym = move_coords
    delta_x = xm - xc
    delta_y = ym - yc
    distance = round(sqrt(delta_x**2 + delta_y**2), 1)
    return distance
