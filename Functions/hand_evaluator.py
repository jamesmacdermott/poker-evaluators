''' 
Input Parameters:
- Two-Dimensional array constructed of 7 card objects, for every player in the game
- For example: [[<deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB410>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CBB90>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB680>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB6E0>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB140>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB890>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CBB00>], [<deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB470>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB560>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB680>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB6E0>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB140>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB890>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CBB00>]]
'''

import heapq
from collections import Counter
import time


def pair(hand,suits,vals,counts) -> list[int]:
    pairs = [val for val, count in counts.items() if count == 2]*2
    if pairs:
        pairs.sort(reverse=True)
        return pairs[:2] + heapq.nlargest(3, (val for val in vals if val not in pairs[:2]))
    return 0

def twopair(hand,suits,vals,counts) -> list[int]:
    pairs = [val for val, count in counts.items() if count == 2]*2
    if len(pairs) >= 4:
        pairs.sort(reverse=True)
        return pairs[:4] + heapq.nlargest(1, (val for val in vals if val not in pairs[:4]))
    return 0

def threeofakind(hand,suits,vals,counts) -> list[int]:
    trips = [val for val, count in counts.items() if count == 3]
    if trips:
        return trips[:1]*3 + heapq.nlargest(2, (val for val in vals if val not in trips))
    return 0

def straight(hand,suits,vals,counts) -> list[int]:
    vals = sorted(set(vals), reverse=True)
    if 14 in vals:
        vals.append(1)
    for i in range(len(vals) - 4):
        if vals[i] - vals[i + 4] == 4:
            return vals[i:i + 5]
    return 0

def flush(hand,suits,vals,counts) -> list[int]:
    for suit in suits:
        if len(suit) >= 5:
            return heapq.nlargest(5, suit)
    return 0
    
def fullhouse(hand,suits,vals,counts) -> list[int]:
    trips = [val for val, count in counts.items() if count == 3]
    pairs = [val for val, count in counts.items() if count >= 2 and val not in trips]
    if trips and pairs:
        return trips[:1]*3 + pairs[:1]*2
    return 0

def fourofakind(hand,suits,vals,counts) -> list[int]:
    quads = [val for val, count in counts.items() if count == 4]
    if quads:
        return quads[:1]*4 + heapq.nlargest(1, (val for val in vals if val not in quads))
    return 0

def straightflush(hand,suits,vals,counts) -> list[int]:
    for suit in suits:
        if len(suit) >= 5:
            straight = sorted(set(suit), reverse=True)
            for i in range(len(straight) - 4):
                if straight[i] - straight[i + 4] == 4:
                    return straight[i:i + 5]
    return 0

def royalflush(hand,suits,vals,counts):
    for suit in suits:
        if set([10, 11, 12, 13, 14]).issubset(set(suit)):
            return [14, 13, 12, 11, 10]
    return 0

def best_hands_allplayers(hands):
    hand_functions = [royalflush,straightflush,fourofakind,fullhouse,flush,straight,threeofakind,twopair,pair]
    player = 0
    best_hands_allplayers = [None for p in range(0,len(hands))]
    while player < len(hands):
        rank = 9
        suits = ([],[],[],[])
        vals = []
        for card in hands[player]:
            suits[card.suit].append(card.value)
            vals.append(card.value)
        cardcounts = Counter(vals)
        for handrank in hand_functions:
            if rank in (9,8,5):
                if any(len(suit) >=5 for suit in suits):
                    besthand = handrank(hands[player],suits,vals,cardcounts)
                else:
                    besthand = 0
            else:
                besthand = handrank(hands[player],suits,vals,cardcounts)
            if besthand != 0:
                break
            rank -= 1
        if not(besthand):
            besthand = heapq.nlargest(5,vals)
            rank = 0
        best_hands_allplayers[player] = (besthand,rank,player)
        player += 1
    return best_hands_allplayers

def evaluate_hand(hands):
    f = time.time()
    hands = best_hands_allplayers(hands)
    maxrank = max(hand[1] for hand in hands)
    hands = [hand for hand in hands if hand[1] == maxrank]
    if len(hands) == 1:
        return hands[0][2]
    if maxrank == 9:
        return "Pot Split Between Players: " + ', '.join(map(str, (hand[2] for hand in hands)))

    cardstocompare = {
        0: (0,1,2,3,4),
        1: (0,2,3,4),
        2: (0,2,4),
        3: (0,3,4),
        4: (0,1,2,3,4),
        5: (0,1,2,3,4),
        6: (0,3),
        7: (0,4),
        8: (0,1,2,3,4)
    } # Rank -> List of cards to check
    for comparing in cardstocompare[maxrank]:
        maxval = max(hand[0][comparing] for hand in hands)
        hands = [hand for hand in hands if hand[0][comparing] == maxval]
        if len(hands) == 1:
            return hands[0][2]
    return "Pot Split Between Players: " + ', '.join(map(str, (hand[2] + 1 for hand in hands)))

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

# Example deck and hands setup (simplified for this example)

# hands = [[Card(14, 1), Card(10, 2), Card(4, 2), Card(12, 2), Card(13, 2), Card(5, 1), Card(2, 3)],
#          [Card(14, 1), Card(10, 2), Card(4, 2), Card(12, 2), Card(13, 2), Card(5, 1), Card(2, 3)],
#          [Card(14, 1), Card(10, 2), Card(4, 2), Card(12, 2), Card(13, 2), Card(5, 1), Card(2, 3)],
#          [Card(14, 1), Card(10, 2), Card(4, 2), Card(12, 2), Card(13, 2), Card(5, 1), Card(2, 3)],
#          [Card(14, 1), Card(10, 2), Card(4, 2), Card(12, 2), Card(13, 2), Card(5, 1), Card(2, 3)],
#          [Card(14, 1), Card(10, 2), Card(4, 2), Card(12, 2), Card(13, 2), Card(5, 1), Card(2, 3)]]

# t = time.time()
# print("\n")
# for i in range(0,10000):
#     x = evaluate_hand(hands)
# print(time.time()-t)
