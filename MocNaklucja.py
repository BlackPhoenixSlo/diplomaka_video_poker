import random
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed

class VideoPokerGame:
    def __init__(self):
        self.deck = [f"{rank}{suit}" for rank in '23456789TJQKA' for suit in 'SHDC']

    def reset_deck(self):
        self.deck = [f"{rank}{suit}" for rank in '23456789TJQKA' for suit in 'SHDC']
    
    def deal_hand(self):
        self.reset_deck()
        random.shuffle(self.deck)
        return self.deck[:5]

    def play_hand(self, strategy):
        initial_hand = self.deal_hand()
        if strategy == 'perfect':
            final_hand = self.perfect_strategy(initial_hand)
        elif strategy == 'worst':
            final_hand = self.worst_strategy(initial_hand)
        elif strategy == 'random':
            final_hand = self.random_strategy(initial_hand)
        elif strategy == 'none':
            final_hand = self.random_strategy(initial_hand)
        elif strategy == 'all':
            final_hand = self.random_strategy(initial_hand)
        elif strategy == 'basic':
            final_hand = self.basic_strategy(initial_hand)
        elif strategy == 'amateur':
            final_hand = self.amateur_strategy(initial_hand)
        else:
            raise ValueError("Unknown strategy")
        return self.evaluate_hand(final_hand)
    

    def perfect_strategy(self, hand):
        values = sorted(['--23456789TJQKA'.index(card[0]) for card in hand])
        suits = [card[1] for card in hand]
        
        if self.is_royal_flush(hand):
            return hand
        if self.is_straight_flush(hand):
            return hand
        if self.is_four_of_a_kind(values):
            return hand
        four_to_royal_flush = self.four_to_royal_flush(hand)
        if four_to_royal_flush:
            return self.complete_hand(four_to_royal_flush, hand)
        if self.is_full_house(values):
            return hand
        if self.is_flush(hand):
            return hand
        if self.is_straight(values):
            return hand
        if self.is_three_of_a_kind(values):
            return self.keep_three_of_a_kind(hand)
        four_to_straight_flush = self.four_to_straight_flush(hand)
        if four_to_straight_flush:
            return self.complete_hand(four_to_straight_flush, hand)
        if self.is_two_pair(values):
            return self.keep_two_pair(hand)
        if self.is_jacks_or_better(values):
            return self.keep_jacks_or_better(hand)
        three_to_royal_flush = self.three_to_royal_flush(hand)
        if three_to_royal_flush:
            return self.complete_hand(three_to_royal_flush, hand)
        four_to_flush = self.four_to_flush(hand)
        if four_to_flush:
            return self.complete_hand(four_to_flush, hand)
        four_to_outside_straight = self.four_to_outside_straight(hand)
        if four_to_outside_straight:
            return self.complete_hand(four_to_outside_straight, hand)

        high_cards = [card for card in hand if card[0] in 'JQKA']
        if high_cards:
            return self.complete_hand(high_cards, hand)

        return self.complete_hand([], hand)

    def keep_two_pair(self, hand):
        pairs = [card for card in hand if sum(1 for x in hand if x[0] == card[0]) == 2]
        return self.complete_hand(pairs, hand)

    def keep_jacks_or_better(self, hand):
        values = [card[0] for card in hand]
        high_pairs = [card for card in hand if values.count(card[0]) == 2 and card[0] in 'JQKA']
        if high_pairs:
            return self.complete_hand(high_pairs, hand)
        return self.complete_hand([], hand)

    def keep_three_of_a_kind(self, hand):
        values = [card[0] for card in hand]
        three_kind = [card for card in hand if values.count(card[0]) == 3]
        if three_kind:
            return self.complete_hand(three_kind, hand)
        return self.complete_hand([], hand)

    def complete_hand(self, keep, hand):
        needed = 5 - len(keep)
        new_cards = [card for card in self.deck if card not in hand][:needed]
        return keep + new_cards

    def evaluate_hand(self, hand):
        if len(hand) != 5:
            raise ValueError("Hand must contain exactly 5 cards")
        values = sorted(['--23456789TJQKA'.index(card[0]) for card in hand])
        if self.is_royal_flush(hand):
            return 800
        elif self.is_straight_flush(hand):
            return 50
        elif self.is_four_of_a_kind(values):
            return 25
        elif self.is_full_house(values):
            return 9
        elif self.is_flush(hand):
            return 6
        elif self.is_straight(values):
            return 4
        elif self.is_three_of_a_kind(values):
            return 3
        elif self.is_two_pair(values):
            return 2
        elif self.is_jacks_or_better(values):
            return 1
        else:
            return 0

    def is_royal_flush(self, hand):
        suits = [card[1] for card in hand]
        values = sorted(['--23456789TJQKA'.index(card[0]) for card in hand])
        return len(set(suits)) == 1 and values == [10, 11, 12, 13, 14]

    def is_straight_flush(self, hand):
        suits = [card[1] for card in hand]
        values = sorted(['--23456789TJQKA'.index(card[0]) for card in hand])
        return len(set(suits)) == 1 and values == list(range(min(values), min(values) + 5))

    def is_four_of_a_kind(self, values):
        return 4 in Counter(values).values()

    def is_full_house(self, values):
        counter = Counter(values)
        return set(counter.values()) == {2, 3}

    def is_flush(self, hand):
        suits = [card[1] for card in hand]
        return len(set(suits)) == 1

    def is_straight(self, values):
        return values == list(range(min(values), min(values) + 5)) or values == [2, 3, 4, 5, 14]

    def is_three_of_a_kind(self, values):
        return 3 in Counter(values).values()

    def is_two_pair(self, values):
        return list(Counter(values).values()).count(2) == 2

    def is_jacks_or_better(self, values):
        high_cards = [11, 12, 13, 14]
        counter = Counter(values)
        for card, count in counter.items():
            if count >= 2 and card in high_cards:
                return True
        return False

    def four_to_royal_flush(self, hand):
        suits = [card[1] for card in hand]
        values = [card[0] for card in hand]
        for suit in 'SHDC':
            suited_cards = [card for card in hand if card[1] == suit and card[0] in 'TJQKA']
            if len(suited_cards) == 4:
                return suited_cards
        return []

    def four_to_straight_flush(self, hand):
        suits = [card[1] for card in hand]
        values = [card[0] for card in hand]
        for suit in 'SHDC':
            suited_cards = [card for card in hand if card[1] == suit]
            if len(suited_cards) >= 4:
                value_indices = sorted(['--23456789TJQKA'.index(card[0]) for card in suited_cards])
                for i in range(len(value_indices) - 3):
                    if value_indices[i+3] - value_indices[i] == 3:
                        return suited_cards
        return []

    def three_to_royal_flush(self, hand):
        suits = [card[1] for card in hand]
        values = [card[0] for card in hand]
        for suit in 'SHDC':
            suited_cards = [card for card in hand if card[1] == suit and card[0] in 'TJQKA']
            if len(suited_cards) == 3:
                return suited_cards
        return []

    def four_to_flush(self, hand):
        suits = [card[1] for card in hand]
        for suit in 'SHDC':
            if suits.count(suit) == 4:
                return [card for card in hand if card[1] == suit]
        return []

    def four_to_outside_straight(self, hand):
        values = [card[0] for card in hand]
        for start in '23456789TJQ':
            seq = start + ''.join(chr(ord(start) + i) for i in range(1, 4))
            if all(val in values for val in seq):
                return [card for card in hand if card[0] in seq]
        return []
    
    def amateur_strategy(self, hand):
        values = [card[0] for card in hand]
        suits = [card[1] for card in hand]
        
        # Keep any pairs
        pairs = [card for card in hand if values.count(card[0]) == 2]
        if pairs:
            return self.complete_hand(pairs, hand)

        # Keep any high cards (J, Q, K, A)
        high_cards = [card for card in hand if card[0] in 'JQKA']
        if high_cards:
            return self.complete_hand(high_cards, hand)

        # Keep any suited cards
        for suit in 'SHDC':
            suited_cards = [card for card in hand if card[1] == suit]
            if len(suited_cards) >= 3:
                return self.complete_hand(suited_cards, hand)
        
        # Otherwise, just keep one random card
        return self.complete_hand([random.choice(hand)], hand)

    def worst_strategy(self, hand):
        perfect_keep = self.perfect_strategy(hand)
        discard = [card for card in hand if card not in perfect_keep]
        return self.complete_hand(discard, hand)

    def random_strategy(self, hand):
        # Randomly decide whether to keep or discard each card
        keep = [card for card in hand if random.choice([True, False])]
        return self.complete_hand(keep, hand)
    
    def all_strategy(self, hand):
        # Randomly decide whether to keep or discard each card
        return self.complete_hand([], hand)
    def none_strategy(self, hand):
        # Randomly decide whether to keep or discard each card
        return hand


    def basic_strategy(self, hand):
        values = ['--23456789TJQKA'.index(card[0]) for card in hand]
        counter = Counter(values)
        keep = [hand[i] for i in range(5) if counter[values[i]] > 1 or values[i] > 10]
        return self.complete_hand(keep, hand)
    
def simulate_hand(strategy):
    game = VideoPokerGame()
    reward = game.play_hand(strategy)
    return reward

def monte_carlo_simulation(strategy, num_simulations):
    rewards_strategy = []
    rewards_perfect = []

    with ProcessPoolExecutor() as executor:
        futures_strategy = [executor.submit(simulate_hand, strategy) for _ in range(num_simulations)]
        futures_perfect = [executor.submit(simulate_hand, 'perfect') for _ in range(num_simulations)]
        
        for future in as_completed(futures_strategy):
            rewards_strategy.append(future.result())
            
        for future in as_completed(futures_perfect):
            rewards_perfect.append(future.result())

    # Calculate ME using the average return of the perfect strategy
    ME = sum(rewards_perfect) / num_simulations -1
    

    # Calculate IP for the given strategy
    IP = sum(rewards_strategy) / num_simulations 

    # Calculate IC for the given strategy
    IC = 0.3371187

    print(sum(rewards_strategy) / num_simulations)
    return ME, IP, IC

def calculate_relative_influence_of_randomness(strategy, num_simulations):
    ME, IP, IC = monte_carlo_simulation(strategy, num_simulations)
    if abs(ME) + abs(IP) + abs(IC) != 0:
        c_g = IC / (abs(ME) + abs(IP) + abs(IC))
    else:
        c_g = 0  # or handle this edge case as required
    return c_g

def main():
    num_simulations = 100000  # Increase number of simulations for more stable results
    
    strategies = [  'all','none','random']
    
    for strategy in strategies:
        c_g = calculate_relative_influence_of_randomness(strategy, num_simulations)
        print(f"Relative Influence of Randomness (c(g)) for {strategy} strategy: {c_g}")

if __name__ == "__main__":
    main()
