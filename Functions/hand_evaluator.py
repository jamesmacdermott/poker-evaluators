''' 
Input Parameters:
- Two-Dimensional array constructed of 7 card objects, for every player in the game
- For example: [[<deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB410>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CBB90>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB680>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB6E0>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB140>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB890>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CBB00>], [<deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB470>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB560>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB680>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB6E0>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB140>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CB890>, <deck_of_cards.deck_of_cards.Card object at 0x00000236B56CBB00>]]
'''

import heapq
from collections import Counter
import time

def fill_with_highest_cards(cards: list[object], besthand: list[object]) -> list[int]:
    cards = get_hand_values([card for card in cards if card not in besthand])
    besthand = get_hand_values(besthand)
    return besthand + heapq.nlargest(5-len(besthand),cards)

def get_hand_values(hand: list[object]) -> list[int]:
    return [card.value for card in hand]

def pair(hand) -> tuple:
    hand_values = get_hand_values(hand)
    counts = Counter(hand_values)
    pairs = []
    for card in hand:
        if counts[card.value] == 2:
            pairs.append(card)
    pairs = sorted(pairs, reverse=True)
    if len(pairs) == 2:
        return fill_with_highest_cards(hand,pairs)
    return 0

def twopair(hand) -> tuple:
    hand_values = get_hand_values(hand)
    counts = Counter(hand_values)
    pairs = []
    for card in hand:
        if counts[card.value] == 2:
            pairs.append(card)
    pairs = sorted(pairs, reverse=True)
    if len(pairs) == 4:
        return fill_with_highest_cards(hand,pairs)
    elif len(pairs) > 4:
        return fill_with_highest_cards(hand,heapq.nlargest(4,pairs))
    return 0

def threeofakind(hand):
    hand_values = get_hand_values(hand)
    counts = Counter(hand_values)
    trips = []
    for card in hand:
        if counts[card.value] == 3 and card not in trips:
            trips.append(card)
    trips = sorted(trips, reverse=True)
    if len(trips) == 3:
        return fill_with_highest_cards(hand,trips)
    return 0

def straight(hand):
    hand_values = sorted(list(set(get_hand_values(hand))),reverse=True)
    if 14 in hand_values:
        hand_values.append(1)
    straight = 0
    consecutive = 1
    for card in range(0,len(hand_values)-1):
        if hand_values[card] != hand_values[card+1]+1:
            consecutive = 1
        else:
            consecutive += 1
        if consecutive == 5:
            return hand_values[card-3:card+2]
    return 0

def flush(hand):
    suits = ([],[],[],[])
    for card in hand:
        suits[card.suit].append(card.value)
    for suit in suits:
        if len(suit) >= 5:
            return heapq.nlargest(5,suit)
    return 0
    
def fullhouse(hand):
    hand_values = get_hand_values(hand)
    counts = Counter(hand_values)
    trips = []
    for card in hand_values:
        if counts[card] == 3:
            trips.append(card)
    trips = heapq.nlargest(3,trips)
    pairs = []
    for card in hand_values:
        if counts[card] >= 2 and card not in trips:
            pairs.append(card)
    if trips and pairs:
        return trips + heapq.nlargest(2,pairs)
    return 0

def fourofakind(hand):
    hand_values = get_hand_values(hand)
    counts = Counter(hand_values)
    for card in hand:
        if counts[card.value] == 4:
            hand_values  = [v for v in hand_values if v != card.value]
            return [card.value]*4 + heapq.nlargest(1,hand_values)
    return 0

def straightflush(hand):
    suits = ([],[],[],[])
    for card in hand:
        suits[card.suit].append(card.value)
    if any(len(suit) >=5 for suit in suits):
        for suit in suits:
            if len(suit) >= 5:
                suit = sorted(suit,reverse=True)
                straight = 0
                consecutive = 1
                for card in range(0,len(suit)-1):
                    if suit[card] != suit[card+1]+1:
                        consecutive = 1
                    else:
                        consecutive += 1
                    if consecutive == 5:
                        return suit[card-3:card+2]
                        
    return 0

def royalflush(hand):
    RoyalFlush = straightflush(hand)
    if type(RoyalFlush) == list:
        if RoyalFlush == [14,13,12,11,10]:
            return RoyalFlush
    return 0

def best_hands_allplayers(hands):
    hand_functions = [royalflush,straightflush,fourofakind,fullhouse,flush,straight,threeofakind,twopair,pair]
    player = 0
    best_hands_allplayers = [None for p in range(0,len(hands))]
    while player < len(hands):
        rank = 9
        for handrank in hand_functions:
            besthand = handrank(hands[player])
            if besthand != 0:
                break
            rank -= 1
        if besthand == 0:
            besthand = fill_with_highest_cards(hands[player],[])
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
        return hands[0]
    if maxrank == 9:
        return 'splitpot'
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
            return hands[0]
    return 'splitpot'

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

# Example deck and hands setup (simplified for this example)

hands = [[Card(14, 2), Card(10, 2), Card(11, 2), Card(12, 2), Card(13, 2), Card(1, 3), Card(2, 3)],[Card(14, 2), Card(10, 2), Card(11, 2), Card(12, 2), Card(13, 2), Card(1, 3), Card(2, 3)],[Card(14, 2), Card(10, 2), Card(11, 2), Card(12, 2), Card(13, 2), Card(1, 3), Card(2, 3)],[Card(14, 2), Card(10, 2), Card(11, 2), Card(12, 2), Card(13, 2), Card(1, 3), Card(2, 3)],[Card(14, 2), Card(10, 2), Card(11, 2), Card(12, 2), Card(13, 2), Card(1, 3), Card(2, 3)],[Card(14, 2), Card(10, 2), Card(11, 2), Card(12, 2), Card(13, 2), Card(1, 3), Card(2, 3)],[Card(14, 2), Card(10, 2), Card(11, 2), Card(12, 2), Card(13, 2), Card(1, 3), Card(2, 3)]]

t = time.time()
print("\n")
for i in range(0,1):
    x = evaluate_hand(hands)
print(time.time()-t)
