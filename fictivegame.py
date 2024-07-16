import random
from collections import Counter

# Define the deck and the payouts for each hand
deck = [f"{rank}{suit}" for rank in '23456789TJQKA' for suit in 'SHDC']
payouts = {
    'royal_flush': 800,
    'straight_flush': 50,
    'four_of_a_kind': 25,
    'full_house': 9,
    'flush': 6,
    'straight': 4,
    'three_of_a_kind': 3,
    'two_pair': 2,
    'jacks_or_better': 1,
    'nothing': 0
}

# Helper functions to evaluate each hand
def evaluate_hand(cards):
    values = sorted(['--23456789TJQKA'.index(card[0]) for card in cards])
    suits = [card[1] for card in cards]

    if is_royal_flush(values, suits):
        return 'royal_flush'
    if is_straight_flush(values, suits):
        return 'straight_flush'
    if is_four_of_a_kind(values):
        return 'four_of_a_kind'
    if is_full_house(values):
        return 'full_house'
    if is_flush(suits):
        return 'flush'
    if is_straight(values):
        return 'straight'
    if is_three_of_a_kind(values):
        return 'three_of_a_kind'
    if is_two_pair(values):
        return 'two_pair'
    if is_jacks_or_better(values):
        return 'jacks_or_better'
    return 'nothing'

def is_royal_flush(values, suits):
    for suit in 'SHDC':
        if set(values) >= {10, 11, 12, 13, 14} and suits.count(suit) >= 5:
            return True
    return False

def is_straight_flush(values, suits):
    for suit in 'SHDC':
        suited_cards = [value for value, card_suit in zip(values, suits) if card_suit == suit]
        if is_straight(suited_cards):
            return True
    return False

def is_four_of_a_kind(values):
    return 4 in Counter(values).values()

def is_full_house(values):
    counter = Counter(values)
    return 3 in counter.values() and 2 in counter.values()

def is_flush(suits):
    return any(suits.count(suit) >= 5 for suit in 'SHDC')

def is_straight(values):
    values = sorted(set(values))
    if len(values) < 5:
        return False
    for i in range(len(values) - 4):
        if values[i + 4] - values[i] == 4:
            return True
    return values[-4:] == [2, 3, 4, 5, 14]  # Special case for Ace-low straight

def is_three_of_a_kind(values):
    return 3 in Counter(values).values()

def is_two_pair(values):
    return len([count for count in Counter(values).values() if count == 2]) == 2

def is_jacks_or_better(values):
    high_cards = [11, 12, 13, 14]
    counter = Counter(values)
    return any(count >= 2 and value in high_cards for value, count in counter.items())

# Function to simulate hands and calculate the EV
def simulate_hands(num_simulations, num_cards=10):
    ev_sum = 0

    for _ in range(num_simulations):
        hand = random.sample(deck, num_cards)
        best_hand_type = evaluate_hand(hand)
        ev_sum += payouts[best_hand_type]

    average_ev = ev_sum / num_simulations
    return average_ev

# Simulate hands to estimate the EV
num_simulations = 1000000
average_ev = simulate_hands(num_simulations)
print(f"Estimated EV for 10-card deal: {average_ev:.6f}")
