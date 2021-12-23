from aplication_logic import Board, IndexOutOfBoardEroor, InvalidMoveError, NotMovedError
from constants import BLACK_WON_EXAMPLE, BOARD_AFTER_MOVE_1, WHITE_WON_EXAMPLE
import pytest


def test_who_starts_the_play(monkeypatch):

    def returnW(a):
        return 'w'

    directory = 'aplication_logic.Board.who_starts_the_play'
    monkeypatch.setattr(directory, returnW)

    board = Board()
    assert board.moving_player() == 'w'


def test_who_is_the_winnerB():
    board = Board()
    board._board = BLACK_WON_EXAMPLE
    winner = board.who_is_the_winner()
    assert winner == 'black'


def test_who_is_the_winnerW():
    board = Board()
    board._board = WHITE_WON_EXAMPLE
    winner = board.who_is_the_winner()
    assert winner == 'white'


def test_normal_move_valid():
    board = Board()
    board._moving_player = 'b'
    counter_coord = (0, 4)
    move_coord = (1, 5)
    board.normal_move(counter_coord, move_coord)
    assert board.board() == BOARD_AFTER_MOVE_1


def test_normal_move_not_moved():
    board = Board()
    board._moving_player = 'b'
    counter_coord = (0, 4)
    move_coord = (0, 4)
    with pytest.raises(NotMovedError):
        board.normal_move(counter_coord, move_coord)


def test_normal_move_not_in_range():
    board = Board()
    board._moving_player = 'b'
    counter_coord = (0, 4)
    move_coord = (4, 5)
    with pytest.raises(InvalidMoveError):
        board.normal_move(counter_coord, move_coord)


def test_normal_move_another_counter_on_the_square():
    board = Board()
    board._moving_player = 'b'
    counter_coord = (0, 4)
    move_coord = (0, 3)
    with pytest.raises(InvalidMoveError):
        board.normal_move(counter_coord, move_coord)


def test_normal_move_out_of_board_plus_coord():
    board = Board()
    board._moving_player = 'w'
    counter_coord = (15, 15)
    move_coord = (16, 15)
    with pytest.raises(IndexOutOfBoardEroor):
        board.normal_move(counter_coord, move_coord)


def test_normal_move_out_of_board_minus_coord():
    board = Board()
    board._moving_player = 'b'
    counter_coord = (0, 4)
    move_coord = (-1, 4)
    with pytest.raises(IndexOutOfBoardEroor):
        board.normal_move(counter_coord, move_coord)
