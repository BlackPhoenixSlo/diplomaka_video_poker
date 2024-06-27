import random
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed

class VideoPokerGame:
    def __init__(self):
        self.deck = [f"{rank}{suit}" for rank in '23456789TJQKA' for suit in 'SHDC']

    def deal_hand(self):
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
        elif strategy == 'basic':
            final_hand = self.basic_strategy(initial_hand)
        else:
            raise ValueError("Unknown strategy")
        return self.evaluate_hand(final_hand)

    def perfect_strategy(self, hand):
        hand_ranks = '23456789TJQKA'
        all_hands = self.generate_all_possible_hands(hand)
        best_hand = max(all_hands, key=self.evaluate_hand)

        values = sorted(['--23456789TJQKA'.index(card[0]) for card in hand])
        suits = [card[1] for card in hand]
        
        if self.is_royal_flush(hand):
            return hand
        if self.is_straight_flush(hand):
            return hand
        if self.is_four_of_a_kind(values):
            return hand
        if self.is_full_house(values):
            return hand
        if self.is_flush(hand):
            return hand
        if self.is_straight(values):
            return hand
        if self.is_three_of_a_kind(values):
            return hand
        if self.is_two_pair(values):
            return hand
        if self.is_jacks_or_better(values):
            return hand
        
        four_to_royal_flush = self.four_to_royal_flush(hand)
        if four_to_royal_flush:
            return four_to_royal_flush
        four_to_straight_flush = self.four_to_straight_flush(hand)
        if four_to_straight_flush:
            return four_to_straight_flush
        three_to_royal_flush = self.three_to_royal_flush(hand)
        if three_to_royal_flush:
            return three_to_royal_flush
        four_to_flush = self.four_to_flush(hand)
        if four_to_flush:
            return four_to_flush
        four_to_outside_straight = self.four_to_outside_straight(hand)
        if four_to_outside_straight:
            return four_to_outside_straight
        
        high_cards = [card for card in hand if card[0] in 'JQKA']
        if high_cards:
            return high_cards

        return []

    def worst_strategy(self, hand):
        values = [card[0] for card in hand]
        keep = [card for card in hand if values.count(card[0]) == 1]
        new_cards = self.deck[5:5 + (5 - len(keep))]
        return keep + new_cards

    def random_strategy(self, hand):
        return hand

    def basic_strategy(self, hand):
        values = ['--23456789TJQKA'.index(card[0]) for card in hand]
        counter = Counter(values)
        keep = [hand[i] for i in range(5) if counter[values[i]] > 1 or values[i] > 10]
        new_cards = self.deck[5:5 + (5 - len(keep))]
        return keep + new_cards

    def generate_all_possible_hands(self, hand):
        return [hand]

    def evaluate_hand(self, hand):
        if not hand:
            return 0
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
        values = [card[0] for card in hand]
        suits = [card[1] for card in hand]
        for suit in 'SHDC':
            if values.count('T') > 0 and values.count('J') > 0 and values.count('Q') > 0 and values.count('K') > 0 and suits.count(suit) >= 4:
                return [card for card in hand if card[1] == suit and card[0] in 'TJQK']

    def four_to_straight_flush(self, hand):
        values = [card[0] for card in hand]
        suits = [card[1] for card in hand]
        for suit in 'SHDC':
            for start in '23456789TJQ':
                seq = start + ''.join(chr(ord(start) + i) for i in range(1, 4))
                if all(val in values for val in seq) and suits.count(suit) >= 4:
                    return [card for card in hand if card[1] == suit and card[0] in seq]

    def three_to_royal_flush(self, hand):
        values = [card[0] for card in hand]
        suits = [card[1] for card in hand]
        for suit in 'SHDC':
            if values.count('T') > 0 and values.count('J') > 0 and suits.count(suit) >= 3:
                return [card for card in hand if card[1] == suit and card[0] in 'TJQK']

    def four_to_flush(self, hand):
        suits = [card[1] for card in hand]
        for suit in 'SHDC':
            if suits.count(suit) == 4:
                return [card for card in hand if card[1] == suit]

    def four_to_outside_straight(self, hand):
        values = [card[0] for card in hand]
        for start in '23456789TJQ':
            seq = start + ''.join(chr(ord(start) + i) for i in range(1, 4))
            if all(val in values for val in seq):
                return [card for card in hand if card[0] in seq]

def simulate_hand(strategy1, strategy2):
    game = VideoPokerGame()
    reward1 = game.play_hand(strategy1)
    reward2 = game.play_hand(strategy2)
    return reward1, reward2

def monte_carlo_simulation(strategy1, strategy2, num_simulations):
    rewards1 = []
    rewards2 = []

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(simulate_hand, strategy1, strategy2) for _ in range(num_simulations)]
        for future in as_completed(futures):
            reward1, reward2 = future.result()
            rewards1.append(reward1)
            rewards2.append(reward2)

    ME = sum(rewards1) / num_simulations
    IP = sum([abs(r - ME) for r in rewards1]) / num_simulations
    IC = sum([abs(r - ME) for r in rewards2]) / num_simulations

    randomness_power = IC / (abs(ME) + IP + IC)
    avg_return1 = sum(rewards1) / num_simulations
    avg_return2 = sum(rewards2) / num_simulations

    return randomness_power, avg_return1, avg_return2

def main():
    num_simulations = 100000  # Increase number of simulations for more stable results
    
    strategy_pairs = [
        ('perfect', 'worst'),
        ('perfect', 'random'),
        ('basic', 'random'),
        ('basic', 'worst'),
        ('perfect', 'basic')
    ]
    
    for strategy1, strategy2 in strategy_pairs:
        randomness_power, avg_return1, avg_return2 = monte_carlo_simulation(strategy1, strategy2, num_simulations)
        print(f"Moč naključja (Randomness Power) for {strategy1} vs {strategy2}: {randomness_power}")
        print(f"Average Return for {strategy1}: {avg_return1}")
        print(f"Average Return for {strategy2}: {avg_return2}")

if __name__ == "__main__":
    main()
