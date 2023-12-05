CANDIDATES = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    **{str(i): i for i in range(1, 10)},
}

REVERSE_CANDIDATES = { k[::-1]: v for k, v in CANDIDATES.items() }

def find_digit(s: str, candidates) -> int:
    for i in range(0, len(s)):
        sub = s[i:]
        for c, num in candidates.items():
            if sub.startswith(c):
                return num

sum = 0
with open('input1.txt') as f:
    for line in f.read().split():
        sum += find_digit(line, CANDIDATES) * 10 + find_digit(line[::-1], REVERSE_CANDIDATES)
print(sum)