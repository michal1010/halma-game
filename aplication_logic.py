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
    '''
    Class contains all of the functions resposnible
    for moving counters in game, and board itself.
    '''
    def __init__(self) -> None:
        self._moving_player = self.who_starts_the_play()
        # I am not sure if it is the best solution
        self._board = copy.deepcopy(BOARD_START)

    def moving_player(self):
        return self._moving_player

    def board(self):
        return self._board

    def move(self, counter_coords, move_coords) -> None:
        '''
        Moves the counter to chosen position.
        Cheks if we are doing _normal_move or _jump_move and
        select the right one.
        '''
        self._move_is_valid(counter_coords, move_coords)
        move = self._which_move_is_it(counter_coords, move_coords)
        if move == '_normal_move':
            self._normal_move(counter_coords, move_coords)
        elif move == '_jump_move':
            self._jump_move(counter_coords, move_coords)
        else:
            info = 'Your move_coords are not in allowable range.'
            raise InvalidMoveError(info)

    def _which_move_is_it(self, counter_coords, move_coords):
        'Cheks if which move the player wants to make.'
        xm, ym = move_coords
        xc, yc = counter_coords
        range_x = self._normal_move_range(xc)
        range_y = self._normal_move_range(yc)
        jump_range = self._jump_move_range(counter_coords)
        if xm in range_x and ym in range_y:
            return '_normal_move'
        elif move_coords in jump_range:
            return '_jump_move'
        else:
            return None

    def _move_is_valid(self, counter_coords, move_coords):
        'Cheks if move over all is valid'
        xc, yc = counter_coords
        xm, ym = move_coords
        board_range = range(0, 16)

        # Cheking if given coords are in range.
        if (
            xc not in board_range or yc not in board_range or
            xm not in board_range or ym not in board_range
        ):
            raise IndexOutOfBoardError('Given coords are invalid.')

        # Checking if we are moving the counter
        elif xc == xm and yc == ym:
            raise NotMovedError('You have not moved')

        # Checking if our counter is on pointed square
        elif self._board[yc][xc] != self._moving_player:
            info = 'Your counter is not on the pointed square'
            raise InvalidCounterCoord(info)

        # Checking if there is no counter on our move_square
        elif self._board[ym][xm] != 'o':
            info = 'There is another counter on this square'
            raise AnotherCounterOnTheSquareError(info)

    def _normal_move(self, counter_coords, move_coords) -> None:
        '''
        Move for a one space; Move that is not a jump
        counter_coords - tuple (x, y);
        directories of the counter, that should be moved
        move_coords - touple (x, y);
        directories to which the counter should be moved
        '''
        xc, yc = counter_coords
        xm, ym = move_coords
        self._board[ym][xm] = self._board[yc][xc]
        self._board[yc][xc] = 'o'
        self._change_moving_player()

    def _normal_move_range(self, i):
        'Returns range within coordintes can change during normal move'
        return range(i-1, i+2)

    def _jump_move(self, counter_coords, move_coords) -> None:
        '''
        Move that is a jump above other counter.
        counter_coords - touple (x, y);
        directories of the counter, that should be moved
        move_coords - touple (x, y);
        directories to which the counter should be moved
        '''
        xc, yc = counter_coords
        xm, ym = move_coords
        self._board[ym][xm] = self._board[yc][xc]
        self._board[yc][xc] = 'o'
        self._change_moving_player()

    def _jump_move_range(self, counter_coords):
        'Returns range within coordintes can change during jump move'
        xc, yc = counter_coords
        range_coords = [
            (xc-2, yc-2), (xc, yc-2), (xc+2, yc-2),
            (xc+2, yc), (xc+2, yc+2), (xc, yc+2),
            (xc-2, yc+2)
        ]
        return range_coords

    def _jump_move_is_valid(self, counter_coords, move_coords):
        '''Cheks if _jump_move is valid.
           If there is a counter to jump above.
        '''
        xc, yc = counter_coords
        xm, ym = move_coords
        xb = (xc + xm)//2
        yb = (yc + ym)//2
        if self._board[yb][xb] == 'o':
            raise InvalidMoveError('There is no counter to jump above')

    def _change_moving_player(self):
        if self._moving_player == 'b':
            self._moving_player = 'w'
        else:
            self._moving_player = 'b'

    def who_starts_the_play(self) -> str:
        'It draw at the begining of the game which player should move first.'
        posibilities = ('w', 'b')
        first_player = choice(posibilities)
        return first_player

    def who_is_the_winner(self):
        'Cheks if player has won the play'
        board = self._board
        for i in range(0, 6):
            if BOARD_END[i] != board[i]:
                break
        else:
            winner = 'white'
            return winner
        for i in range(11, 15):
            if BOARD_END[i] != board[i]:
                break
        else:
            winner = 'black'
            return winner
        winner = None
        return winner
