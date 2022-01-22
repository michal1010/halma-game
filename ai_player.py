from aplication_logic import Board
from math import sqrt
import copy


def ai_turn(board: Board):
    '''
    Make ai turn during the game.
    '''
    # if board.turn_number() <= 8:
    #     begining(board)
    # else:
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
    if player_color == 'black':
        if delta_x >= 0 and delta_y >= 0:
            return 'right direction'
        else:
            return 'wrong direction'
    elif player_color == 'white':
        if delta_x <= 0 and delta_y <= 0:
            return 'right direction'
        else:
            return 'wrong direction'


def move(board: Board):
    '''
    Makes the best possible move after the beginig faze of the game.
    '''
    counter_moves = jump_move_distances(board)
    counter_moves_max = max_distances(counter_moves)
    counter_coords, move_coords = the_best_move(counter_moves_max)
    board.move(counter_coords, move_coords)


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


def move_distance(board):
    '''
    Cheks all the possible moves for every counter and
    append its distance to the dict in form
    {(x, y): {(xm, ym): distance made in this move}.
    xm, ym - move_coords
    '''
    distances_coords = jump_move_distances(board)
    # If jump move was not possible in case of a counter
    # we are adding possible normal move of this counter to
    # the distances_coords dict
    distances_coords_full = normal_move_distances(board, distances_coords)
    return distances_coords_full


def normal_move_distances(board: Board, distances_coords: dict):
    '''
    Cheks all the possible normal moves for every counter and
    adds them to the dict made in jump_move_distances_function.
    Dict is in form {(x, y): {(xm, ym): distance made in this move}.
    '''
    distances_coords_full = copy.deepcopy(distances_coords)
    for counter_coords, moves_values in distances_coords.items():
        if moves_values == {}:
            distances_coords_full[counter_coords] = possible_normal_moves(counter_coords)
    return distances_coords_full


def possible_normal_moves(board_object: Board):
    '''
    Cheks all the possible normal moves for every counter and
    append its to a dict in form
    {(xm, ym): distance made in this move}
    xm, ym - move coords
    '''
    board = board_object.board()
    color = board.moving_player()
    black_coords, white_coords = finding_counters(board)
    if color == 'black':
        color_coords = black_coords
    elif color == 'white':
        color_coords = white_coords
    move_distance = {}
    for counter_coords in color_coords.keys():
        move_coords, distance = possible_normal_move(counter_coords, board)
        move_distance[move_coords] = distance
    return move_distance


def possible_normal_move(counter_coords: tuple, board: list):
    '''
    Cheks possible normal move for given counter.
    Returns move_coords and made distance.
    '''
    xc, yc = counter_coords
    if board[xc+1][xc+1] == 'o':
        move_coords = xc+1, yc+1
        distance = round(sqrt(2), 1)
    elif xc >= yc and board[yc+1][xc] == 'o':
        move_coords = xc, yc+1
        distance = 1
    elif xc < yc and board[yc][xc+1] == 'o':
        move_coords = xc+1, yc
        distance = 1
    return move_coords, distance


def jump_move_distances(board_object: Board):
    '''
    Cheks all the possible jump moves for every counter and
    append its distance to the dict in form
    {(x, y): {(xm, ym): distance made in this move}.
    xm, ym - move_coords
    '''
    color = board_object.moving_player()
    black_coords, white_coords = finding_counters(board_object)
    board = board_object.board()
    distance_coords = []
    def jump_move_distances_valid(counter_coords, distances,
                            last_counter_coords=None):
        '''
        Cheks all the possible jump_moves for given counter and
        append its distance to the dict in form
        {(xm, ym): distance}.
        xm, ym - move_coords
        '''
        xc, yc = counter_coords

        distance_coords.append(counter_coords)

        # Cheking all the options of jump_move for the counter
        if (
            xc-2 > -1 and yc-2 > -1 and board[yc-1][xc-1] != 'o' and
            board[yc-2][xc-2] == 'o' and (xc-2, yc-2) != last_counter_coords
            and 'right direction' == right_direction(board_object,
                                                     counter_coords, (xc-2, yc-2), color)
        ):
            jump_move_distances_valid((xc-2, yc-2), distances, counter_coords)
        if (
            yc-2 > -1 and board[yc-1][xc] != 'o' and board[yc-2][xc] == 'o'
            and (xc, yc-2) != last_counter_coords and
            'right direction' == right_direction(board_object, counter_coords,
                                                 (xc, yc-2), color)
        ):
            jump_move_distances_valid((xc, yc-2), distances, counter_coords)
        if (
            yc-2 > -1 and xc+2 < 16 and board[yc-1][xc+1] != 'o' and
            board[yc-2][xc+2] == 'o' and (xc+2, yc-2) != last_counter_coords and
            'right direction' == right_direction(board_object, counter_coords,
                                                 (xc+2, yc-2), color)
        ):
            jump_move_distances_valid((xc+2, yc-2), distances, counter_coords)
        if (
            xc+2 < 16 and board[yc][xc+1] != 'o' and board[yc][xc+2] == 'o'
            and (xc+2, yc) != last_counter_coords and
            'right direction' == right_direction(board_object, counter_coords,
                                                 (xc+2, yc), color)
        ):
            jump_move_distances_valid((xc+2, yc), distances, counter_coords)
        if (
            xc+2 < 16 and yc+2 < 16 and board[yc+1][xc+1] != 'o' and
            board[yc+2][xc+2] == 'o' and (xc+2, yc+2) != last_counter_coords
            and 'right direction' == right_direction(board_object, counter_coords,
                                                     (xc+2, yc+2), color)
        ):
            jump_move_distances_valid((xc+2, yc+2), distances, counter_coords)
        if (
            yc+2 < 16 and board[yc+1][xc] != 'o' and board[yc+2][xc] == 'o'
            and (xc, yc+2) != last_counter_coords and
            'right direction' == right_direction(board_object, counter_coords,
                                                 (xc, yc+2), color)
        ):
            jump_move_distances_valid((xc, yc+2), distances, counter_coords)
        if (
            xc-2 > -1 and yc+2 < 16 and board[yc+1][xc-1] != 'o' and
            board[yc+2][xc-2] == 'o' and (xc-2, yc+2) != last_counter_coords
            and 'right direction' == right_direction(board_object, counter_coords,
                                                     (xc-2, yc+2), color)
        ):
            jump_move_distances_valid((xc-2, yc+2), distances, counter_coords)
        if (
            xc-2 > -1 and board[yc][xc-1] != 'o' and board[yc][xc-2] == 'o'
            and (xc-2, yc) != last_counter_coords and
            'right direction' == right_direction(board_object, counter_coords,
                                                 (xc-2, yc), color)
        ):
            jump_move_distances_valid((xc-2, yc), distances, counter_coords)

        if last_counter_coords is not None and len(distance_coords) > 1:
            max_distance = distance_made(distance_coords[0], distance_coords[-1])
            move_coords = distance_coords[-1]
            distances[move_coords] = max_distance
        # elif len(distance_coords) == 1:
        #     distances
        if len(distance_coords) > 1:
            distance_coords.pop()

    if color == 'black':
        color_coords = black_coords
    elif color == 'white':
        color_coords = white_coords

    distances_coords = {}

    for counter_coords in color_coords.keys():
        distances = {}
        jump_move_distances_valid(counter_coords, distances)
        distances_coords[counter_coords] = distances.copy()
        distances.clear()
        distance_coords.clear()

    return distances_coords


def max_distances(distances_coords: dict):
    '''
    From dict in form
    {(xc, yc): {(xm, ym): distance made in this move}.
    xm, ym - counter move coords
    xc, yc - counter beggining coords
    creates dict in form
    {xc, yc: {move_coords: (xm, ym), max_distance: distance}}
    '''
    counters_moves = {}
    max_distance = 0
    max_coords = None
    for counter_coords, move_values in distances_coords.items():
        for move_coords, distance in move_values.items():
            if distance > max_distance:
                max_distance = distance
                max_coords = move_coords
        counters_moves[counter_coords] = {
            'move_coords': max_coords,
            'max_distance': max_distance
        }
        max_distance = 0
    return counters_moves


def the_best_move(counter_coords):
    '''
    Peaks from dict in form
    {xc, yc: {move_coords: (xm, ym), max_distance: distance}}
    pair of key and move_coords value with the biggest max_distance.
    '''
    counter = None
    move = None
    distance = 0
    for counter_coords, move_values in counter_coords.items():
        if distance < move_values['max_distance']:
            distance = move_values['max_distance']
            counter = counter_coords
            move = move_values['move_coords']
    return counter, move


def distance_made(counter_coords, move_coords):
    'Returns what distance you are making in this move.'
    xc, yc = counter_coords
    xm, ym = move_coords
    delta_x = xm - xc
    delta_y = ym - yc
    distance = round(sqrt(delta_x**2 + delta_y**2), 1)
    return distance
