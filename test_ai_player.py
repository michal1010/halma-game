from ai_player import (
    ai_turn,
    finding_counters,
    jump_move_distances,
    jump_move_distances_valid,
    max_distances,
    possible_normal_move,
    right_direction,
    distance_made,
    the_best_move,
)
from aplication_logic import Board
from constants import BOARD_AFTER_COMBO_JUMP_MOVE3

# ----------------------- DISTANCE_MADE TESTS ---------------------------


def test_distance_made_int_outcome():
    counter_coords = (5, 7)
    move_coords = (7, 7)
    distance = distance_made(counter_coords, move_coords)
    assert distance == 2


def test_distance_made_float_outcome():
    counter_coords = (5, 7)
    move_coords = (4, 6)
    distance = distance_made(counter_coords, move_coords)
    assert distance == 1.41


# ---------------------- RIGHT_DIRECTION TESTS -----------------------------


def test_right_direction_player_b():
    board = Board()
    board._moving_player = "b"
    counter_coords = (5, 7)
    move_coords = (4, 6)
    direction = right_direction(board, counter_coords, move_coords, "black")
    assert direction == "wrong direction"
    counter_coords = (5, 7)
    move_coords = (5, 8)
    direction = right_direction(board, counter_coords, move_coords, "black")
    assert direction == "right direction"


def test_right_direction_player_w():
    board = Board()
    board._moving_player = "w"
    counter_coords = (5, 7)
    move_coords = (4, 6)
    direction = right_direction(board, counter_coords, move_coords, "white")
    assert direction == "right direction"
    counter_coords = (5, 7)
    move_coords = (5, 8)
    direction = right_direction(board, counter_coords, move_coords, "white")
    assert direction == "wrong direction"


# ------------------------------- MOVE FUNCTIONS TESTS -------------------


def test_finding_counters():
    board = Board()
    board._board = BOARD_AFTER_COMBO_JUMP_MOVE3
    black_coords, white_coords = finding_counters(board)
    black_coords2 = {
        (0, 0): [],
        (1, 0): [],
        (2, 0): [],
        (3, 0): [],
        (4, 0): [],
        (0, 1): [],
        (1, 1): [],
        (2, 1): [],
        (3, 1): [],
        (4, 1): [],
        (0, 2): [],
        (1, 2): [],
        (2, 2): [],
        (3, 2): [],
        (2, 3): [],
        (4, 4): [],
        (5, 4): [],
        (2, 5): [],
        (3, 5): [],
    }
    white_coords2 = {
        (14, 11): [],
        (15, 11): [],
        (13, 12): [],
        (14, 12): [],
        (15, 12): [],
        (12, 13): [],
        (13, 13): [],
        (14, 13): [],
        (15, 13): [],
        (11, 14): [],
        (12, 14): [],
        (13, 14): [],
        (14, 14): [],
        (15, 14): [],
        (11, 15): [],
        (12, 15): [],
        (13, 15): [],
        (14, 15): [],
        (15, 15): [],
    }
    assert black_coords2 == black_coords
    assert white_coords2 == white_coords


# def test_moves_distances_standard():
#     board = Board()
#     color_coords = {(0, 0): [0], (1, 0): [0], (2, 0): [2.8],
#                     (3, 0): [2.0, 2.8], (4, 0): [2.0], (0, 1): [0],
#                     (1, 1): [2.8], (2, 1): [2.8], (3, 1): [2.0, 2.0],
#                     (4, 1): [0], (0, 2): [2.8], (1, 2): [2.8],
#                     (2, 2): [2.0, 2.0], (3, 2): [2.8], (0, 3): [2.8, 2.0],
#                     (1, 3): [2.0, 2.0], (2, 3): [2.8], (0, 4): [2.0],
#                     (1, 4): [0]}
#     assert color_coords == moves_distances(board, 'black')


def test_moves_distances_combo_jump_move():
    board = Board()
    # color_coords = {(0, 0): [], (1, 0): [], (2, 0): [2.8],
    #                 (3, 0): [2.0, 2.8], (4, 0): [2.0], (0, 1): [],
    #                 (1, 1): [2.8], (2, 1): [2.8], (3, 1): [2.0, 2.0],
    #                 (4, 1): [], (0, 2): [2.8], (1, 2): [2.8],
    #                 (2, 2): [2.0, 2.0], (3, 2): [2.8], (0, 3): [2.8, 2.0],
    #                 (1, 3): [2.0, 2.0], (2, 3): [2.8], (0, 4): [2.0],
    #                 (1, 4): []}
    board._board = BOARD_AFTER_COMBO_JUMP_MOVE3
    # color_coords = moves_distances(board, 'black')
    ai_turn(board)
    pass


def test_possible_normal_move():
    board = Board()
    board._moving_player = 'black'
    counter_coords = (2, 4)
    assert possible_normal_move(counter_coords, board) == {
        (3, 5): 1.41
    }


def test_jump_move_distances_valid():
    distances = {}
    distances_coords = []
    counter_coords = (3, 0)
    board = Board()
    board._moving_player = 'black'
    board._board = BOARD_AFTER_COMBO_JUMP_MOVE3
    distnaces_function = jump_move_distances_valid(
        board, board.board(), counter_coords, distances,
        distances_coords
    )
    assert distnaces_function == {(5, 0): 1.18, (5, 2): 2.81}


def test_max_distances_black():
    distances_coords = {
        (1, 1): {
            (1, 2): 1,
            (2, 1): 1,
        },
        (3, 3): {(4, 4): 1.41, (5, 5): 2.83},
    }
    max_distances_coords = {
        (1, 1): {"move_coords": (1, 2), "max_distance": 1},
        (3, 3): {"move_coords": (5, 5), "max_distance": 2.83},
    }
    assert max_distances(distances_coords, "black") == max_distances_coords


def test_max_distances_white():
    distances_coords = {
        (2, 2): {
            (1, 2): 1,
            (2, 1): 1,
        },
        (6, 6): {(4, 4): 1.41, (5, 5): 2.83},
    }
    max_distances_coords = {
        (2, 2): {"move_coords": (2, 1), "max_distance": 1},
        (6, 6): {"move_coords": (5, 5), "max_distance": 2.83},
    }
    assert max_distances(distances_coords, "white") == max_distances_coords


def test_the_best_move():
    counter_moves_max = {
        (0, 0): {"move_coords": None, "max_distance": 0},
        (2, 0): {"move_coords": (4, 2), "max_distance": 2.82},
        (2, 1): {"move_coords": (4, 3), "max_distance": 2.82},
        (2, 2): {"move_coords": (4, 2), "max_distance": 1.35},
    }
    counter_coords = (2, 0)
    move_coords = (4, 2)
    assert the_best_move(counter_moves_max, "black") == (
        counter_coords,
        move_coords,
    )
