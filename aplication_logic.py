from random import choice
from constants import BOARD_END, BOARD_START
import copy


class InvalidNormalMove(Exception):
    pass


class InvalidCounterCoord(Exception):
    pass


class NotMovedError(InvalidNormalMove):
    pass


class IndexOutOfBoardEroor(Exception):
    pass


class InvalidJumpMove(Exception):
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

    def which_move()
    pass

    def normal_move(self, counter_coords, move_coords) -> None:
        '''
        Move for a one space; Move that is not a jump
        counter_coords - touple (x, y);
        directories of the counter, that should be moved
        move_coords - touple (x, y);
        directories to which the counter should be moved
        '''
        try:
            self._coords_are_not_positive(counter_coords, move_coords)
            self._normal_move_is_valid(counter_coords, move_coords)
            self._counter_is_on_pointed_square(counter_coords)
            xc, yc = counter_coords
            xm, ym = move_coords
            self._board[ym][xm] = self._board[yc][xc]
            self._board[yc][xc] = 'o'
        except IndexError as e:
            raise IndexOutOfBoardEroor('You mooved out of board: ' + str(e))

    def _normal_move_is_valid(self, counter_coords, move_coords):
        'Cheks if normal_move is valid'
        xc, yc = counter_coords
        xm, ym = move_coords
        if xm not in self._normal_move_range(xc):
            raise InvalidNormalMove('You can not move this many squares')
        elif ym not in self._normal_move_range(yc):
            raise InvalidNormalMove('You can not move this many squares')
        elif xc == xm and yc == ym:
            raise NotMovedError('You have not moved')
        elif self._board[ym][xm] != 'o':
            raise InvalidNormalMove('There is another counter on this square')

    def _counter_is_on_pointed_square(self, counter_coords):
        'Cheks if counter is on given field'
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
        'Returns range within coordintes can change during normal move'
        return range(i-1, i+2)

    def jump_move(self, counter_coords, move_coords) -> None:
        '''
        Move that is a jump above other counter.
        counter_coords - touple (x, y);
        directories of the counter, that should be moved
        move_coords - touple (x, y);
        directories to which the counter should be moved
        '''
        try:
            self._coords_are_not_positive(counter_coords, move_coords)
            self._counter_is_on_pointed_square(counter_coords)
            self._jump_move_is_valid(counter_coords, move_coords)
            xc, yc = counter_coords
            xm, ym = move_coords
            self._board[ym][xm] = self._board[yc][xc]
            self._board[yc][xc] = 'o'
        except IndexError as e:
            raise IndexOutOfBoardEroor('You mooved out of board: ' + str(e))

    def _jump_move_range(self, counter_coords):
        'Returns range within coordintes can change during jump move'
        xc, yc = counter_coords
        range_coords = [
            (xc-2, yc-2), (xc, yc-2), (xc+2, yc-2),
            (xc+2, yc), (xc+2, yc+2), (xc, yc-2),
            (xc-2, yc+2)
        ]
        return range_coords

    def _jump_move_is_valid(self, counter_coords, move_coords):
        'Cheks if jump_move is valid'
        xc, yc = counter_coords
        xm, ym = move_coords
        if xc == xm and yc == ym:
            raise NotMovedError('You have not moved.')
        elif move_coords not in self._jump_move_range(counter_coords):
            raise InvalidJumpMove('You can not move this number of squers')
        elif self._board[ym][xm] != 'o':
            raise InvalidJumpMove('There is another counter on this square')
        # xb, yb coordinates of square that need to be filed with a counter
        # if jump move is valid
        xb = (xc + xm)//2
        yb = (yc + ym)//2
        if self._board[yb][xb] == 'o':
            raise InvalidJumpMove('There is no counter to jump above')

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
