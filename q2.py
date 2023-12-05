import re
from dataclasses import dataclass
from enum import StrEnum

_PATTERN = re.compile(r'\s*(?P<num>\d+)\s+(?P<colour>red|green|blue)\s*')

class Colour(StrEnum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'

@dataclass
class Observation:
    red: int = 0
    green: int = 0
    blue: int = 0

def read() -> dict[int, list[list[Observation]]]:
    with open('input2.txt') as f:
        data = {}
        game_num = 0
        for line in f.read().split('\n'):
            if not line:
                continue
            game_num += 1
            game, observations = line.split(':', maxsplit=1)
            assert game == f"Game {game_num}", f"{game} not #{game_num}"
            game = []
            for observation in observations.split(';'):
                obs = Observation()
                for colour in observation.split(','):
                    m = _PATTERN.match(colour)
                    assert m
                    num = int(m.group('num'))
                    c = m.group('colour')
                    if c == 'red':
                        obs.red = num
                    elif c == 'green':
                        obs.green = num
                    elif c == 'blue':
                        obs.blue = num
                    else:
                        raise AssertionError(f"unknown colour {c}")
                game.append(obs)
            data[game_num] = game
    return data
                
