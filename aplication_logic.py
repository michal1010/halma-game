from random import choice
from constants import BOARD_END, BOARD_START


class InvalidMoveError(Exception):
    pass


class InvalidCounterCoord(Exception):
    pass


class NotMovedError(InvalidMoveError):
    pass


class IndexOutOfBoardEroor(Exception):
    pass


class Board:
    '''
    Class contains all of the functions resposnible
    for moving counters in game, and board itself.
    '''
    def __init__(self) -> None:
        self._moving_player = self.who_starts_the_play()

    def moving_player(self):
        return self._moving_player

    _board = BOARD_START

    def board(self):
        return self._board

    def normal_move(self, counter_coords, move_coords) -> None:
        '''
        Move fore a one space; Move that is not a jump
        counter_coords - touple (x, y);
        directories of the counter, that should be moved
        move_coords - touple (x, y);
        directories to which the counter should be moved
        '''
        try:
            self._coords_are_not_positive(counter_coords, move_coords)
            self._normal_move_is_valid(counter_coords, move_coords)
            self._counter_is_on_pointed_field(counter_coords)
            xc, yc = counter_coords
            xm, ym = move_coords
            self._board[ym][xm] = self._board[yc][xc]
        except IndexError as e:
            raise IndexOutOfBoardEroor('You mooved out of board: ' + str(e))

        self._board[yc][xc] = 'o'

    def _normal_move_is_valid(self, counter_coords, move_coords):
        xc, yc = counter_coords
        xm, ym = move_coords
        if xm not in self._normal_move_range(xc):
            raise InvalidMoveError('You can not move this many squares')
        if ym not in self._normal_move_range(yc):
            raise InvalidMoveError('You can not move this many squares')
        if xc == xm and yc == ym:
            raise NotMovedError('You have not moved')
        if self._board[ym][xm] != 'o':
            raise InvalidMoveError('There is another counter on this square')

    def _counter_is_on_pointed_field(self, counter_coords):
        xc, yc = counter_coords
        if self._board[yc][xc] != self._moving_player:
            raise InvalidCounterCoord('Your counter is not on the pointed field')

    def _coords_are_not_positive(self, counter_coords, move_coords):
        '''
        Chceck is coordinates are positive numbers.
        Python uses negative numbers while taking value from list,
        it can not work in our program.
        '''
        xc, yc = counter_coords
        xm, ym = move_coords
        if xc < 0 or yc < 0 or xm < 0 or ym < 0:
            raise IndexOutOfBoardEroor('Coordintes you have chosen are out of board.')

    def _normal_move_range(self, i):
        '''
        Returns range within coordintes can change during normal move
        '''
        return range(i-1, i+2)

    def jump_move(self, x: int, y: int) -> None:
        '''
        Move that is a jump above other counter.
        Function is recursive, because it is possible
        to make few jumps in one turn.
        x, y - directories
        '''
        pass

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
