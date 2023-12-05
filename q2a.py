from q2 import read, Observation

def possible(game: list[Observation], red: int = 12, green: int = 13, blue: int = 14):
    for obs in game:
        if obs.red > red or obs.green > green or obs.blue > blue:
            return False
    return True

def power(game: list[Observation]) -> int:
    r = g = b = 0
    for obs in game:
        r = max(r, obs.red)
        g = max(g, obs.green)
        b = max(b, obs.blue)
    return r * g * b

data = read()
sum = 0
power_sum = 0
for game_num, game in data.items():
    if possible(game):
        sum += game_num
    power_sum += power(game)

print(sum)
print(power_sum)