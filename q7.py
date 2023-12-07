import functools
from enum import Enum

class HandType(Enum):
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

card_rank = {
    **{ str(c): c for c in range(2, 10) },
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}

def hand_type(lookup: dict[str, int]) -> HandType:
    hand_type = HandType.HIGH_CARD
    for v in lookup.values():
        if v == 5:
            hand_type = HandType.FIVE_OF_A_KIND
        elif v == 4:
            hand_type = HandType.FOUR_OF_A_KIND
        elif v == 3:
            if hand_type == HandType.PAIR:
                hand_type = HandType.FULL_HOUSE
            else:
                assert hand_type == HandType.HIGH_CARD
                hand_type = HandType.THREE_OF_A_KIND
        elif v == 2:
            if hand_type == HandType.THREE_OF_A_KIND:
                hand_type = HandType.FULL_HOUSE
            elif hand_type == HandType.PAIR:
                hand_type = HandType.TWO_PAIR
            else:
                assert hand_type == HandType.HIGH_CARD
                hand_type = HandType.PAIR
        else:
            assert v == 1
    return hand_type

class Hand:
    original: str
    hand_type: HandType
    wildcard_hand_type: HandType

    def __repr__(self) -> str:
        return f'{self.original} ({self.hand_type}/{self.wildcard_hand_type})'

    def __init__(self, hand: str):
        assert len(hand) == 5
        self.original = hand
        lookup = {}
        for c in hand:
            if c not in lookup:
                lookup[c] = 1
            else:
                lookup[c] += 1

        self.hand_type = hand_type(lookup)
        wildcards = lookup.pop('J', 0)
        self.wildcard_hand_type = hand_type(lookup)
        if wildcards >= 4:
            self.wildcard_hand_type = HandType.FIVE_OF_A_KIND
        elif wildcards == 3:
            if self.wildcard_hand_type == HandType.PAIR:
                self.wildcard_hand_type = HandType.FIVE_OF_A_KIND
            else:
                assert self.wildcard_hand_type == HandType.HIGH_CARD
                self.wildcard_hand_type = HandType.FOUR_OF_A_KIND
        elif wildcards == 2:
            if self.wildcard_hand_type == HandType.THREE_OF_A_KIND:
                self.wildcard_hand_type = HandType.FIVE_OF_A_KIND
            elif self.wildcard_hand_type == HandType.PAIR:
                self.wildcard_hand_type = HandType.FOUR_OF_A_KIND
            else:
                assert self.wildcard_hand_type == HandType.HIGH_CARD
                self.wildcard_hand_type = HandType.THREE_OF_A_KIND
        elif wildcards == 1:
            if self.wildcard_hand_type == HandType.FOUR_OF_A_KIND:
                self.wildcard_hand_type = HandType.FIVE_OF_A_KIND
            elif self.wildcard_hand_type == HandType.THREE_OF_A_KIND:
                self.wildcard_hand_type = HandType.FOUR_OF_A_KIND
            elif self.wildcard_hand_type == HandType.TWO_PAIR:
                self.wildcard_hand_type = HandType.FULL_HOUSE
            elif self.wildcard_hand_type == HandType.PAIR:
                self.wildcard_hand_type = HandType.THREE_OF_A_KIND
            else:
                assert self.wildcard_hand_type == HandType.HIGH_CARD
                self.wildcard_hand_type = HandType.PAIR

def read_data() -> list[(Hand, int)]:
    hands = []
    with open('input7.txt') as f:
        for line in f.read().split('\n'):
            line = line.strip()
            if not line:
                continue

            hand, bid = line.split(' ')
            bid = int(bid)
            assert len(hand) == 5
            assert bid > 0
            hands.append((Hand(hand), bid))
    return hands

def compare_hands(a: (Hand, int), b: (Hand, int)) -> int:
    a = a[0]
    b = b[0]
    if a.hand_type.value > b.hand_type.value:
        return 1
    elif a.hand_type.value < b.hand_type.value:
        return -1

    for ca, cb in zip(a.original, b.original):
        ra = card_rank[ca]
        rb = card_rank[cb]
        if ra > rb:
            return 1
        elif ra < rb:
            return -1

    raise AssertionError(f"always expect a winner, got {a} = {b}?!")

def compare_wildcards(a: (Hand, int), b: (Hand, int)) -> int:
    a = a[0]
    b = b[0]

    if a.wildcard_hand_type.value > b.wildcard_hand_type.value:
        return 1
    elif a.wildcard_hand_type.value < b.wildcard_hand_type.value:
        return -1

    for ca, cb in zip(a.original, b.original):
        ra = 1 if ca == 'J' else card_rank[ca]
        rb = 1 if cb == 'J' else card_rank[cb]
        if ra > rb:
            return 1
        elif ra < rb:
            return -1

    raise AssertionError(f"always expect a winner, got {a} = {b}?!")

def rank_hands(hands: list[(Hand, int)], cmp) -> list[(Hand, int)]:
    return sorted(hands, key=functools.cmp_to_key(cmp))

data = read_data()

def score(cmp) -> int:
    ranked = rank_hands(data, cmp)

    rank = 1
    prod = 0
    for _, bid in ranked:
        prod += bid * rank
        rank += 1
    return prod

print(score(compare_hands))
print(score(compare_wildcards))
