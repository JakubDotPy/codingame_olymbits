import sys
from dataclasses import dataclass
from dataclasses import field
from functools import partial
from itertools import count
from collections import Counter

log = partial(print, file=sys.stderr, flush=True)

RESET_STR = 'GAME_OVER'

player_idx = int(input())
nb_games = int(input())

@dataclass
class HurdleGame:
    gpu: str  # ASCII representation of the racetrack. .....#...#...#................
    reg_0: int  # position of player 1  
    reg_1: int  # position of player 2  
    reg_2: int  # position of player 3  
    reg_3: int  # stun timer for player 1 
    reg_4: int  # stun timer for player 2 
    reg_5: int  # stun timer for player 3 
    reg_6: int  # unused

    reg: list[int] = field(init=False, default_factory=list)

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

    @property
    def stun(self):
        return self.reg[player_idx + 3]

    @property
    def next_ahead(self):
        """return str of next 3 fields"""
        pp = self.reg[player_idx] + 1  # player pos
        look = self.gpu[pp: pp + 3]
        if (rem := (3 - len(look))) > 0:
            look += '.' * rem
        return look


def prepare_steps(gpu):
    gpu = gpu.replace('.#', 'U')
    gpu = gpu.replace('...', 'R')
    gpu = gpu.replace('..', 'D')
    gpu = gpu.replace('.', 'L')
    return gpu

def best_ahead(parts):
    c = Counter(parts)
    log(sorted(c.most_common()))
    return sorted(c.most_common())[0][0]


# game loop
for turn in count():

    # score
    for _ in range(3):
        score_info = input()

    games = [
        HurdleGame.from_input()
        for _ in range(nb_games)
    ]

    for g in games:
        if g.stun:
            log('stunned')
        else:
            log(g.next_ahead)

    combined = best_ahead(
        (g.next_ahead for g in games if not g.stun)
    )

    log(combined, ' - selected')
    
    moves = {
        '#' : 'UP',
        '...': 'RIGHT',
        '..' : 'DOWN',
        '.'  : 'LEFT',
    }

    selected_move = 'UP'  # default, one place
    for pattern, move in moves.items():
        if combined.startswith(pattern):
            selected_move = move
            break

    log(selected_move)
    print(selected_move)
