from random import choice
from constants import BOARD_END, BOARD_START
import copy


class InvalidCounterCoord(Exception):
    pass


class NotMovedError(Exception):
    pass


class IndexOutOfBoardError(Exception):
    pass


class AnotherCounterOnTheSquareError(Exception):
    pass


class InvalidMoveError(Exception):
    pass


class Board:
    """
    Class contains all of the functions resposnible
    for moving counters in game, and board itself.
    """

    def __init__(self) -> None:
        self._moving_player = self.who_starts_the_play()
        # I am not sure if it is the best solution
        self._board = copy.deepcopy(BOARD_START)
        self._moves_made = 0
        self._turn_number = 0
        self.end_phase_b = False
        self.end_phase_w = False

    def turn_number(self):
        return self._turn_number

    def moving_player(self):
        "Gives information which player turn is now black or white"
        return self._moving_player

    def board(self):
        return self._board

    def move(self, counter_coords, move_coords) -> None:
        """
        Moves the counter to chosen position.
        Cheks if we are doing _normal_move or _jump_move and
        select the right one.
        """
        self._move_is_valid(counter_coords, move_coords)
        move = self._which_move_is_it(counter_coords, move_coords)
        if move == "_normal_move":
            self._normal_move(counter_coords, move_coords)
        elif move == "_jump_move":
            self._jump_move(counter_coords, move_coords)
        self._moves_made += 1
        self._turn_number = self._moves_made // 2

    def _which_move_is_it(self, counter_coords, move_coords):
        "Cheks if which move the player wants to make."
        xm, ym = move_coords
        xc, yc = counter_coords
        range_x = self._normal_move_range(xc)
        range_y = self._normal_move_range(yc)
        if xm in range_x and ym in range_y:
            return "_normal_move"
        else:
            return "_jump_move"

    def _move_is_valid(self, counter_coords, move_coords):
        "Cheks if move over all is valid"
        xc, yc = counter_coords
        xm, ym = move_coords
        board_range = range(0, 16)
        player_counter = "b" if self._moving_player == "black" else "w"
        # Cheking if given coords are in range.
        if (
            xc not in board_range
            or yc not in board_range
            or xm not in board_range
            or ym not in board_range
        ):
            raise IndexOutOfBoardError("Given coords are invalid.")

        # Checking if we are moving the counter
        if xc == xm and yc == ym:
            raise NotMovedError("You have not moved")

        # Checking if our counter is on the pointed square

        elif self._board[yc][xc] != player_counter:
            info = "Your counter is not on the pointed square"
            raise InvalidCounterCoord(info)

        # Checking if there is no counter on our move_square
        elif self._board[ym][xm] != "-":
            info = "There is another counter on this square"
            raise AnotherCounterOnTheSquareError(info)

    def _jump_move(self, counter_coords, move_coords):
        """
        Move that is a jump above other counter. Can be multiple.
        counter_coords - touple (x, y);
        directories of the counter, that should be moved
        move_coords - touple (x, y);
        directories to which the counter should be moved
        """
        # auxiliary variable for recursive function
        self._combo_move_is_valid = False
        self._jump_move_validation(counter_coords, move_coords)
        if self._combo_move_is_valid:
            xc, yc = counter_coords
            xm, ym = move_coords
            self._board[ym][xm] = self._board[yc][xc]
            self._board[yc][xc] = "-"
            self._change_moving_player()
        else:
            raise InvalidMoveError("You can not move to this square.")

    def _jump_move_validation(
        self, counter_coords, move_coords, previous_coords=None
    ):
        """
        Cheks recursively if this jump_move is possible.
        All the options of jump_move for this counter are being checked.
        If the move is possible object atrirbute _combo_move_is_valid
        gets value True.
        """
        xc, yc = counter_coords
        board = self._board
        previous_coords = [] if previous_coords is None else previous_coords
        previous_coords.append(counter_coords)
        # Cheking if we get to the position that is pointed by the player
        if counter_coords == move_coords:
            self._combo_move_is_valid = True

        # Cheking all the options of jump_move for the counter
        if (
            xc - 2 > -1
            and yc - 2 > -1
            and board[yc - 1][xc - 1] != "-"
            and board[yc - 2][xc - 2] == "-"
            and (xc - 2, yc - 2) not in previous_coords
        ):
            self._jump_move_validation(
                (xc - 2, yc - 2), move_coords, previous_coords
            )
        if (
            yc - 2 > -1
            and board[yc - 1][xc] != "-"
            and board[yc - 2][xc] == "-"
            and (xc, yc - 2) not in previous_coords
        ):
            self._jump_move_validation(
                (xc, yc - 2), move_coords, previous_coords
            )
        if (
            yc - 2 > -1
            and xc + 2 < 16
            and board[yc - 1][xc + 1] != "-"
            and board[yc - 2][xc + 2] == "-"
            and (xc + 2, yc - 2) not in previous_coords
        ):
            self._jump_move_validation(
                (xc + 2, yc - 2), move_coords, previous_coords
            )
        if (
            xc + 2 < 16
            and board[yc][xc + 1] != "-"
            and board[yc][xc + 2] == "-"
            and (xc + 2, yc) not in previous_coords
        ):
            self._jump_move_validation(
                (xc + 2, yc), move_coords, previous_coords
            )
        if (
            xc + 2 < 16
            and yc + 2 < 16
            and board[yc + 1][xc + 1] != "-"
            and board[yc + 2][xc + 2] == "-"
            and (xc + 2, yc + 2) not in previous_coords
        ):
            self._jump_move_validation(
                (xc + 2, yc + 2), move_coords, previous_coords
            )
        if (
            yc + 2 < 16
            and board[yc + 1][xc] != "-"
            and board[yc + 2][xc] == "-"
            and (xc, yc + 2) not in previous_coords
        ):
            self._jump_move_validation(
                (xc, yc + 2), move_coords, previous_coords
            )
        if (
            xc - 2 > -1
            and yc + 2 < 16
            and board[yc + 1][xc - 1] != "-"
            and board[yc + 2][xc - 2] == "-"
            and (xc - 2, yc + 2) not in previous_coords
        ):
            self._jump_move_validation(
                (xc - 2, yc + 2), move_coords, previous_coords
            )
        if (
            xc - 2 > -1
            and board[yc][xc - 1] != "-"
            and board[yc][xc - 2] == "-"
            and (xc - 2, yc) not in previous_coords
        ):
            self._jump_move_validation(
                (xc - 2, yc), move_coords, previous_coords
            )

    def _normal_move(self, counter_coords, move_coords) -> None:
        """
        Move for a one space; Move that is not a jump
        counter_coords - tuple (x, y);
        directories of the counter, that should be moved
        move_coords - touple (x, y);
        directories to which the counter should be moved
        """
        xc, yc = counter_coords
        xm, ym = move_coords
        self._board[ym][xm] = self._board[yc][xc]
        self._board[yc][xc] = "-"
        self._change_moving_player()

    def _normal_move_range(self, i):
        "Returns range within coordintes can change during normal move"
        return range(i - 1, i + 2)

    def _change_moving_player(self):
        if self._moving_player == "black":
            self._moving_player = "white"
        else:
            self._moving_player = "black"

    def who_starts_the_play(self) -> str:
        "It draw at the begining of the game which player should move first."
        posibilities = ("white", "black")
        first_player = choice(posibilities)
        return first_player

    def who_is_the_winner(self):
        "Cheks if player has won the play"
        board = self._board
        for i in range(0, 6):
            if BOARD_END[i] != board[i]:
                break
        else:
            winner = "white"
            return winner
        for i in range(11, 15):
            if BOARD_END[i] != board[i]:
                break
        else:
            winner = "black"
            return winner
        winner = None
        return winner
