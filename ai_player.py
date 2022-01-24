from aplication_logic import Board
from math import sqrt
import copy

from constants import (
    BLACK_WINNING_COORDS,
    WHITE_WINNING_COORDS,
)


def ai_turn(board: Board):
    """
    Make ai turn during the game.
    """
    counter_coords, move_coords = move(board)
    board = enabling_end_phase(move_coords, board)
    counter_coords, move_coords = begin_end_phase(
        move_coords, counter_coords, board
    )
    board.move(counter_coords, move_coords)


def move(board: Board, direction=None, counters_not_winning=None):
    """
    Returns coords of counter that should be moved and
    coords of move that should be done.
    """
    counter_moves = move_distance(board, direction)
    color = board.moving_player()
    counter_moves_max = max_distances(counter_moves, color)
    counter_coords, move_coords = the_best_move(
        counter_moves_max, color, counters_not_winning
    )
    return counter_coords, move_coords


def move_distance(board, direction=None):
    """
    Cheks all the possible moves for every counter and
    append its distance to the dict in form
    {(x, y): {(xm, ym): distance made in this move}.
    xm, ym - move_coords
    """
    distances_coords = jump_move_distances(board, direction)
    # If jump move was not possible in case of a counter
    # we are adding possible normal move of this counter to
    # the distances_coords dict
    distances_coords_full = normal_move_distances(
        board, distances_coords, direction
    )
    return distances_coords_full


def jump_move_distances(board_object: Board, direction=None):
    """
    Cheks all the possible jump moves for every counter and
    append its distance to the dict in form
    {(x, y): {(xm, ym): distance made in this move}.
    xm, ym - move_coords
    """
    color = board_object.moving_player()
    black_coords, white_coords = finding_counters(board_object)
    board = board_object.board()
    distance_coords = []

    if color == "black":
        color_coords = black_coords
    elif color == "white":
        color_coords = white_coords
    distances_dict = {}

    for counter_coords in color_coords.keys():
        distances = {}
        distances = possible_jump_move(
            board_object,
            board,
            counter_coords,
            distances,
            distance_coords,
            direction=direction,
        )
        distances_dict[counter_coords] = distances.copy()
        distance_coords.clear()

    return distances_dict


def possible_jump_move(
    board_object,
    board,
    counter_coords,
    distances,
    distance_coords,
    last_counter_coords=None,
    direction=None,
):
    """
    Cheks all the possible jump_moves for given counter and
    append its distance to the dict in form
    {(xm, ym): distance}.
    xm, ym - move_coords
    """
    xc, yc = counter_coords
    color = board_object.moving_player()
    distance_coords.append(counter_coords)

    # Cheking all the options of jump_move for the counter
    if (
        xc - 2 > -1
        and yc - 2 > -1
        and board[yc - 1][xc - 1] != "-"
        and board[yc - 2][xc - 2] == "-"
        and (xc - 2, yc - 2) != last_counter_coords
        and "right direction"
        == right_direction(
            board_object,
            counter_coords,
            (xc - 2, yc - 2),
            color,
            direction,
        )
    ):
        distances = possible_jump_move(
            board_object,
            board,
            (xc - 2, yc - 2),
            distances,
            distance_coords,
            counter_coords,
            direction,
        )
    if (
        yc - 2 > -1
        and board[yc - 1][xc] != "-"
        and board[yc - 2][xc] == "-"
        and (xc, yc - 2) != last_counter_coords
        and "right direction"
        == right_direction(
            board_object, counter_coords, (xc, yc - 2), color, direction
        )
    ):
        distances = possible_jump_move(
            board_object,
            board,
            (xc, yc - 2),
            distances,
            distance_coords,
            counter_coords,
            direction,
        )
    if (
        yc - 2 > -1
        and xc + 2 < 16
        and board[yc - 1][xc + 1] != "-"
        and board[yc - 2][xc + 2] == "-"
        and (xc + 2, yc - 2) != last_counter_coords
        and "right direction"
        == right_direction(
            board_object,
            counter_coords,
            (xc + 2, yc - 2),
            color,
            direction,
        )
    ):
        distances = possible_jump_move(
            board_object,
            board,
            (xc + 2, yc - 2),
            distances,
            distance_coords,
            counter_coords,
            direction,
        )
    if (
        xc + 2 < 16
        and board[yc][xc + 1] != "-"
        and board[yc][xc + 2] == "-"
        and (xc + 2, yc) != last_counter_coords
        and "right direction"
        == right_direction(
            board_object, counter_coords, (xc + 2, yc), color, direction
        )
    ):
        distances = possible_jump_move(
            board_object,
            board,
            (xc + 2, yc),
            distances,
            distance_coords,
            counter_coords,
            direction,
        )
    if (
        xc + 2 < 16
        and yc + 2 < 16
        and board[yc + 1][xc + 1] != "-"
        and board[yc + 2][xc + 2] == "-"
        and (xc + 2, yc + 2) != last_counter_coords
        and "right direction"
        == right_direction(
            board_object,
            counter_coords,
            (xc + 2, yc + 2),
            color,
            direction,
        )
    ):
        distances = possible_jump_move(
            board_object,
            board,
            (xc + 2, yc + 2),
            distances,
            distance_coords,
            counter_coords,
            direction,
        )
    if (
        yc + 2 < 16
        and board[yc + 1][xc] != "-"
        and board[yc + 2][xc] == "-"
        and (xc, yc + 2) != last_counter_coords
        and "right direction"
        == right_direction(
            board_object, counter_coords, (xc, yc + 2), color, direction
        )
    ):
        distances = possible_jump_move(
            board_object,
            board,
            (xc, yc + 2),
            distances,
            distance_coords,
            counter_coords,
            direction,
        )
    if (
        xc - 2 > -1
        and yc + 2 < 16
        and board[yc + 1][xc - 1] != "-"
        and board[yc + 2][xc - 2] == "-"
        and (xc - 2, yc + 2) != last_counter_coords
        and "right direction"
        == right_direction(
            board_object,
            counter_coords,
            (xc - 2, yc + 2),
            color,
            direction,
        )
    ):
        distances = possible_jump_move(
            board_object,
            board,
            (xc - 2, yc + 2),
            distances,
            distance_coords,
            counter_coords,
            direction,
        )
    if (
        xc - 2 > -1
        and board[yc][xc - 1] != "-"
        and board[yc][xc - 2] == "-"
        and (xc - 2, yc) != last_counter_coords
        and "right direction"
        == right_direction(
            board_object, counter_coords, (xc - 2, yc), color, direction
        )
    ):
        distances = possible_jump_move(
            board_object,
            board,
            (xc - 2, yc),
            distances,
            distance_coords,
            counter_coords,
            direction,
        )

    if last_counter_coords is not None and len(distance_coords) > 1:
        max_distance = round(distance_made(distance_coords[0],
                                           distance_coords[-1]), 2)
        move_coords = distance_coords[-1]
        distances[move_coords] = max_distance
    return distances


def normal_move_distances(
    board: Board, distances_coords: dict, direction=None
):
    """
    Cheks all the possible normal moves for every counter and
    adds them to the dict made in jump_move_distances_function.
    Dict is in form {(x, y): {(xm, ym): distance made in this move}.
    """
    distances_coords_full = copy.deepcopy(distances_coords)
    for counter_coords, moves_values in distances_coords.items():
        if moves_values == {}:
            distances_coords_full[counter_coords] = possible_normal_move(
                counter_coords, board, direction
            )
    return distances_coords_full


def possible_normal_move(
    counter_coords: tuple, board_object: Board, direction=None
):
    """
    Cheks possible normal move for given counter.
    Returns move_coords and made distance.
    """

    xc, yc = counter_coords
    board = board_object.board()
    board_range = range(0, 16)
    color = board_object.moving_player()

    if (
        yc + 1 in board_range
        and xc + 1 in board_range
        and board[yc + 1][xc + 1] == "-"
        and right_direction(
            board_object, (xc, yc), (xc + 1, yc + 1), color, direction
        )
        == "right direction"
    ):
        move_coords = xc + 1, yc + 1

        distance = round(sqrt(2), 2)
    elif (
        yc - 1 in board_range
        and xc - 1 in board_range
        and board[yc - 1][xc - 1] == "-"
        and right_direction(
            board_object, (xc, yc), (xc - 1, yc - 1), color, direction
        )
        == "right direction"
    ):
        move_coords = xc - 1, yc - 1
        distance = round(sqrt(2), 2)
    elif (
        yc - 1 in board_range
        and xc + 1 in board_range
        and board[yc - 1][xc + 1] == "-"
        and right_direction(
            board_object, (xc, yc), (xc + 1, yc - 1), color, direction
        )
        == "right direction"
    ):
        move_coords = xc + 1, yc - 1
        distance = round(sqrt(2), 2)
    elif (
        yc + 1 in board_range
        and xc - 1 in board_range
        and board[yc + 1][xc - 1] == "-"
        and right_direction(
            board_object, (xc, yc), (xc - 1, yc + 1), color, direction
        )
        == "right direction"
    ):
        move_coords = xc - 1, yc + 1
        distance = round(sqrt(2), 2)
    elif (
        yc + 1 in board_range
        and board[yc + 1][xc] == "-"
        and right_direction(
            board_object, (xc, yc), (xc, yc + 1), color, direction
        )
        == "right direction"
    ):
        move_coords = xc, yc + 1
        distance = 1
    elif (
        yc - 1 in board_range
        and board[yc - 1][xc] == "-"
        and right_direction(
            board_object, (xc, yc), (xc, yc - 1), color, direction
        )
        == "right direction"
    ):
        move_coords = xc, yc - 1
        distance = 1
    elif (
        xc + 1 in board_range
        and board[yc][xc + 1] == "-"
        and right_direction(
            board_object, (xc, yc), (xc + 1, yc), color, direction
        )
        == "right direction"
    ):
        move_coords = xc + 1, yc
        distance = 1
    elif (
        xc - 1 in board_range
        and board[yc][xc - 1] == "-"
        and right_direction(
            board_object, (xc, yc), (xc - 1, yc), color, direction
        )
        == "right direction"
    ):
        move_coords = xc - 1, yc
        distance = 1
    else:
        move_coords = None
        distance = 0
    return {move_coords: distance}


def enabling_end_phase(move_coords, board: Board):
    "Checking if end phase began."
    color = board.moving_player()
    if move_coords is None:
        if color == "black":
            board.end_phase_b = True
        else:
            board.end_phase_w = True
    return board


def begin_end_phase(move_coords, counter_coords, board: Board):
    "If end_phase is enabled starts end_phase function."
    color = board.moving_player()
    if board.end_phase_w and color == "white":
        counter_coords, move_coords = end_phase(board)
    elif board.end_phase_b and color == "black":
        counter_coords, move_coords = end_phase(board)
    return counter_coords, move_coords


def end_phase(board: Board):
    """
    Returns coords of counter that should be moved and
    coords of move that should be done in end phase of the game.
    """
    empty_winning_coords, counters_not_winning = finding_winning_coords(board)
    color = board.moving_player()
    if color == "white":
        direction = empty_winning_coords[-1]
    else:
        direction = empty_winning_coords[0]
    counter_coords, move_coords = move(board, direction, counters_not_winning)
    return counter_coords, move_coords


def finding_winning_coords(board: Board):
    color = board.moving_player()
    if color == "black":
        winning_coords = BLACK_WINNING_COORDS
    else:
        winning_coords = WHITE_WINNING_COORDS
    empty_winning_coords = []
    conuters_not_winning = []
    black_coords, white_coords = finding_counters(board)
    color_coords = black_coords if color == "black" else white_coords
    for coords in winning_coords:
        if coords not in color_coords.keys():
            empty_winning_coords.append(coords)
    for counter in color_coords.keys():
        if counter not in winning_coords:
            conuters_not_winning.append(counter)
    return empty_winning_coords, conuters_not_winning


def finding_counters(board: Board):
    """
    Functions finds coords of all counters on the board.
    Returns two dicts in form {(xc, yc): []},
    one with white counters coords and one with black counters coords
    """
    white_coords = {}
    black_coords = {}
    board = board.board()
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == "b":
                black_coords[x, y] = []
            elif board[y][x] == "w":
                white_coords[x, y] = []
    return black_coords, white_coords


def max_distances(distances_coords: dict, color):
    """
    From dict in form
    {(xc, yc): {(xm, ym): distance made in this move}.
    xm, ym - counter move coords
    xc, yc - counter beggining coords
    creates dict in form
    {xc, yc: {move_coords: (xm, ym), max_distance: distance}}
    """
    counters_moves = {}
    max_distance = 0
    max_coords = None
    for counter_coords, move_values in distances_coords.items():
        if color == "white":
            reversed_move_values = list(move_values.items())[::-1]
        else:
            reversed_move_values = move_values.items()
        for move_coords, distance in reversed_move_values:
            if distance > max_distance:
                max_distance = distance
                max_coords = move_coords
        counters_moves[counter_coords] = {
            "move_coords": max_coords,
            "max_distance": max_distance,
        }
        max_distance = 0
        move_coords = None
    return counters_moves


def the_best_move(counter_coords_dict: dict, color, counters_not_winning=None):
    """
    Peaks from dict in form
    {xc, yc: {move_coords: (xm, ym), max_distance: distance}}
    pair of key and move_coords value with the biggest max_distance.
    """
    counter = (-1, -1)
    move = None
    distance = 0

    for counter_coords, move_values in counter_coords_dict.items():
        if (
            counters_not_winning is None
            or counter_coords in counters_not_winning
        ):
            x1, y1 = counter_coords
            x2, y2 = counter
            if color == "black":
                direction_condition = sum(counter_coords) < sum(counter) or (
                    sum(counter_coords) == sum(counter) and x1 > x2
                )
            elif color == "white":
                direction_condition = sum(counter_coords) > sum(counter) or (
                    sum(counter_coords) == sum(counter) and x1 < x2
                )
            if distance < move_values["max_distance"] or (
                distance == move_values["max_distance"] and direction_condition
            ):
                distance = move_values["max_distance"]
                counter = counter_coords
                move = move_values["move_coords"]
    return counter, move


def distance_made(counter_coords, move_coords):
    "Returns what distance you are making in this move."
    xc, yc = counter_coords
    xm, ym = move_coords
    delta_x = xm - xc
    delta_y = ym - yc
    distance = round(sqrt(delta_x ** 2 + delta_y ** 2), 2)
    return distance


def right_direction(
    board: Board, counter_coords, move_coords, player_color, direction=None
):
    """
    Cheks if we are moving the counter in the right direction.
    In advantage of the player are only moves in direction of
    oponent start squares.
    """
    xc, yc = counter_coords
    xm, ym = move_coords

    if player_color == "black":
        direction = (15, 15) if direction is None else direction
        current_distance = distance_made(counter_coords, direction)
        move_distance = distance_made(move_coords, direction)
    elif player_color == "white":
        direction = (0, 0) if direction is None else direction
        current_distance = distance_made(counter_coords, direction)
        move_distance = distance_made(move_coords, direction)
    if current_distance > move_distance:
        return "right direction"
    else:
        return "wrong direction"
