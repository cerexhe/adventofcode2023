def find_digit(s: str) -> int:
    for c in s:
        if '0' <= c <= '9':
            return ord(c) - ord('0')

sum = 0
with open('input1.txt') as f:
    for line in f.read().split():
        sum += find_digit(line) * 10 + find_digit(line[::-1])
print(sum)