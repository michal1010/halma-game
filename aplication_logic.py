from random import choice


class Board:
    '''
    Class is containing all of the functions resposnible
    for moving counters in game, and board itself.
    '''
    def __init__(self) -> None:
        self._moving_player = self.who_starts_the_play()

    def moving_player(self):
        return self._moving_player

    # b - black counter; w - white counter; o - blanck spacke
    board = [
        ['b', 'b', 'b', 'b', 'b', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
        ['b', 'b', 'b', 'b', 'b', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
        ['b', 'b', 'b', 'b', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
        ['b', 'b', 'b', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
        ['b', 'b', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
        ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
        ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
        ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
        ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
        ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
        ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
        ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
        ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'w', 'w'],
        ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'w', 'w', 'w'],
        ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'w', 'w', 'w', 'w'],
        ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'w', 'w', 'w', 'w', 'w'],
        ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'w', 'w', 'w', 'w', 'w'],
    ]

    def normal_move(self, x: int, y: int) -> None:
        '''
        Move fore a one space; Move that is not a jump
        x, y - directories, where I the counter should go
        '''
        pass

    def jump_move(self, x: int, y: int) -> None:
        '''
        Move that is a jump above other counter.
        Function is recursive, because it is possible
        to make few jumps in one turn.
        x, y - directories
        '''
        pass

    def who_starts_the_play(self) -> str:
        'It draw of the begining of the game which player should move first.'
        posibilities = ('w', 'b')
        first_player = choice(posibilities)
        return first_player
