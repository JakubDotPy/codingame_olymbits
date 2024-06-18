import sys
from dataclasses import dataclass
from dataclasses import field
from functools import partial
from itertools import chain
from collections import Counter
from operator import itemgetter

log = partial(print, file=sys.stderr, flush=True)

RESET_STR = 'GAME_OVER'

player_idx = int(input())
nb_games = int(input())


@dataclass
class ArcadeGame:
    gpu: str  
    reg_0: int
    reg_1: int
    reg_2: int
    reg_3: int
    reg_4: int
    reg_5: int
    reg_6: int

    reg: list[int] = field(init=False, default_factory=list)

    move_abbrev: dict[str, str] = field(init=False, default_factory=lambda: {
        'U': 'UP',
        'D': 'DOWN',
        'L': 'LEFT',
        'R': 'RIGHT',
    })

    descision_weight: int = field(init=False, default=1)

    def __post_init__(self):
        self.reg = [
            self.reg_0,
            self.reg_1,
            self.reg_2,
            self.reg_3,
            self.reg_4,
            self.reg_5,
            self.reg_6,
        ]

    @classmethod
    def from_input(cls):
        gpu, *regs = input().split()
        return cls(gpu, *map(int, regs))


class HurdleGame(ArcadeGame):

    moves = {
        '#' : 'UP',
        '...': 'RIGHT',
        '..' : 'DOWN',
        '.'  : 'LEFT',
    }

    @property
    def look_ahead(self):
        """return str of next 3 fields"""
        pp = self.reg[player_idx] + 1  # player pos
        look = self.gpu[pp: pp + 3].rjust(3, '.')
        return look
    
    def next_move(self):
        move = next(
            (
                v 
                for k, v in self.moves.items()
                if self.look_ahead.startswith(k)
            ),
            'UP'  # default
        )
        log(f'Hurdle: {move}')
        return move


class Archery(ArcadeGame):

    moves = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0),
    }

    def new_positions(self) -> dict[str, tuple[int]]:
        coord_pos = itemgetter(player_idx * 2, player_idx * 2 + 1)
        x, y = coord_pos(self.reg)
        try:
            v = int(self.gpu[0])
        except ValueError:
            v = 0
        new_pos = {
            move: abs(x + dx * v) + abs(y + dy * v)
            for move, (dx, dy) in self.moves.items()
        }
        return new_pos

    def next_move(self) -> str:
        positions = self.new_positions()
        best_first = sorted(positions.items(), key=itemgetter(1))
        best_move = best_first[0][0]
        log(f'Archer: {best_move}')
        return best_move


class Roller(ArcadeGame):
    
    def next_move(self):
        # go for zero risk  
        # TODO: improve this
        letter = self.gpu[1]
        move = self.move_abbrev.get(letter, 'UP')
        log(f'Roller: {move}')
        return move


class Diving(ArcadeGame):
    
    descision_weight = 2

    def next_move(self):
        # TODO: improve this
        letter = self.gpu[0]
        move = self.move_abbrev.get(letter, 'UP')
        log(f'Diving: {move}')
        return move


def log_score():
    scores = [
        tuple(map(int, input().split()))
        for _ in range(3)
    ]
    my_score = scores[player_idx]
    (
        total,
        hurdle_gold,
        hurdle_silver,
        hurdle_bronze,
        archer_gold,
        archer_silver,
        archer_bronze,
        roller_gold,
        roller_silver,
        roller_bronze,
        dive_gold,
        dive_silver,
        dive_bronze,
    ) = my_score

    log(f"Hurdles: {hurdle_gold} {hurdle_silver} {hurdle_bronze}")
    log(f"Archery: {archer_gold} {archer_silver} {archer_bronze}")
    log(f"Roller : {roller_gold} {roller_silver} {roller_bronze}")
    log(f"Diving : {dive_gold} {dive_silver} {dive_bronze}")

while True:

    log_score()

    games = [
        HurdleGame.from_input(),
        Archery.from_input(),
        Roller.from_input(),
        Diving.from_input(),
    ]

    moves = chain.from_iterable([
            [g.next_move()] * g.descision_weight
            for g in games
        ])
    best_move = Counter(moves).most_common(1)[0][0]

    print(best_move)

