
# 0: Nothing in hand; not a recognized poker hand 
# 1: One pair; one pair of equal ranks within five cards
# 2: Two pairs; two pairs of equal ranks within five cards
# 3: Three of a kind; three equal ranks within five cards
# 4: Straight; five cards, sequentially ranked with no gaps
# 5: Flush; five cards with the same suit
# 6: Full house; pair + different rank three of a kind
# 7: Four of a kind; four equal ranks within five cards
# 8: Straight flush; straight + flush
# 9: Royal flush; {Ace, King, Queen, Jack, Ten} + flush

import numpy as np
import pandas as pd
import operator
import Perceptron


class PokerGame:

    shared_cards = np.array([])
    
    def __init__(self, NumberOfPlayers = 2):
        self.players = np.array([Player(i) for i in range(NumberOfPlayers)])
        self.deck = Deck()
        self.poker_ai = PokerAI()

    def play(self):
        
        self.shared_cards = np.array([])
        # self.deck.display_deck()
        # self.deck.shuffle_deck()

        print("START")
        self.progress_stage(stageName='Draw', drawCards=2)
        self.progress_stage(stageName='Flop', drawCards = 3)
        self.progress_stage(stageName='Turn', drawCards = 1)
        self.progress_stage(stageName='River', drawCards = 1)

        winner, classification = self.determine_winner()

        poker_hands = ["Highest card", "One pair", "Two pair", "Three of a kind",
                       "Straight", "Flush", "Full house", "Four of a kind", 
                       "Straight flush", "Royal flush"]

        hand_name = poker_hands[classification.get_classification()]

        print(f"#{winner.number} won with {hand_name}")
        print(f"Winning cards: ")
        classification.display()

        return winner, self.players, self.shared_cards

    def determine_winner(self):

        winner = None
        highest_classification = CardsClassification(-1)

        for player in self.players:

            player_hand = player.get_poker_hand()
            hand_classifications = player_hand.get_classifications()
            player_hand_classification = max(hand_classifications)

            # player_hand.display_classifications()
           
            if highest_classification.get_classification() < player_hand_classification.get_classification():
                highest_classification = player_hand_classification
                winner = player

            elif highest_classification.get_classification() == player_hand_classification.get_classification():

                winner_cards = winner.get_poker_hand().get_cards()
                player_cards = player_hand.get_cards()

                for i in range(len(player_cards) - 1, 0, -1):

                    if player_cards[i] > winner_cards[i]:
                        winner = player
            
        return winner, highest_classification

    def progress_stage(self, stageName, drawCards):

        print(f'Stage: {stageName}')
        
        if stageName == "Draw":
            for player in self.players:
                player.add_cards(self.deck.draw_card(numberOfDraws=drawCards))
        else:
            self.draw_cards(numberOfCards=drawCards)
        
        self.display_players()
        self.display_table()
        self.AI_advice(stageName)

    def AI_advice(self, stageName):
        for player in self.players:
            continue_playing = self.poker_ai.suggest_move(stageName, player.get_poker_hand())
            if continue_playing:
                print(f"AI determines player #{player.number} should check.")
            else:
                print(f"AI determines player #{player.number} should fold.")
    def display_players(self):
        for player in self.players:
            player.display()
    
    def display_table(self):
        print("Table:")
        for card in self.shared_cards:
            card.display()
    
    def draw_cards(self, numberOfCards):

        cards = self.deck.draw_card(numberOfCards)
        self.shared_cards = np.append(self.shared_cards, cards)
        
        for player in self.players:
            player.add_cards(cards)

class Player:
    
    def __init__(self, number):
        self.cards = np.array([])
        self.number = number
        self.poker_hand = None
    
    def add_cards(self, cards):
        self.cards = np.append(self.cards, cards)
        self.set_poker_hand(self.cards)
    
    def set_poker_hand(self, cards):
        self.poker_hand = PokerHand(cards)
    
    def get_poker_hand(self):
        return self.poker_hand

    def display(self):
        print(f"Player {self.number}")
        self.poker_hand.display()

class PokerHand:
    
    suits = {}
    ranks = {}

    def __init__(self, cards):
        self.cards = np.sort(cards, axis=None)
        self.classifications = set()
        self.classify()
    
    def get_classifications(self):
        return self.classifications
    
    def get_cards(self):
        return self.cards
    
    def display(self):
        for card in self.cards:
            card.display()
    
    def display_classifications(self):
        print("CLASSIFICATIONS FOR HAND:")
        self.display()
        for classification in self.classifications:
            classification.display()

    def classify(self):

        straight = False

        ranks = {}
        suits = {}

        straight_count = 1
        straight_cards = np.array([])

        ace = False
        high_card = None
        
        previous_card = None

        for i in range(len(self.cards)):

            card = self.cards[i]
            rank = card.get_rank()
            suit = card.get_suit()

            if rank not in ranks:
                ranks[rank] = np.array([card])
            else:
                ranks[rank] = np.append(ranks[rank], card)
            
            if suit not in suits:
                suits[suit] = np.array([card])
            else:
                suits[suit] = np.append(suits[suit], card)
            
            if rank == 1:
                ace = True

            if previous_card is not None:
                
                previous_rank = previous_card.get_rank()
                
                # Accumulates points towards a straight classification
                # print(f"previous_rank: {previous_rank}")
                # print(f"rank: {rank}")
                if previous_rank == rank - 1:
                    straight_count += 1
                # Resets points
                else:
                    straight_count = 1
        
                # Defines straight
                if straight_count >= 5:
                    straight = True
                    straight_cards = np.array([self.cards[i-4], self.cards[i-3], self.cards[i-2], self.cards[i-1], self.cards[i]])

                # Handles ace high straights
                if straight_count >= 4 and rank == 13 and ace:
                    straight = True
                    straight_cards = np.array([self.cards[0], self.cards[i-3], self.cards[i-2], self.cards[i-1], self.cards[i]])
            
            previous_card = card

        if straight:
            self.assign_classification(handClassification=4, cards=straight_cards)

        # Assigns junk card classification
        if ace:
            high_card = self.cards[0]
        else:
            high_card = self.cards[-1]
        self.assign_classification(handClassification=0, cards=high_card)

        # Checking for float classification
        for suit, cards in suits.items():

            cards = np.sort(cards, axis=None)
            
            frequency = len(cards)
            # print(frequency)

            if frequency >= 5:

                if frequency > 5:
                    difference = frequency - 5
                    if ace: 
                        cards_top_four = cards[difference + 1:]
                        cards = np.array([cards[0]])
                        cards = np.append(cards, cards_top_four)
                       
                    else:
                        cards = np.array(cards[difference:])
                
                self.assign_classification(handClassification=5, cards=cards)

                # Checking for special straight classifications (straight flush, royal flush)
                if straight:
                    
                    if np.equal(cards, straight_cards).all():
                        self.assign_classification(handClassification=8, cards=cards)

                        if straight_cards[-1].rank == 13 and ace:
                            self.assign_classification(handClassification=9, cards=cards)
        
        # Checking for pair classifications (pair, two pair, 3oak, 4oak, full house)
        pairs = np.array([])
        for rank, cards in ranks.items():

            appearances = len(cards)
            # print(f"rank: {rank}, appearances: {appearances}, cards: {cards}")
            # Check Pair
            if appearances == 2:

                # Check for full house
                if len(pairs) == 2:
                    pairs = np.append(pairs, cards)
                    self.assign_classification(handClassification=2, cards=pairs)
                
                if len(pairs) == 3:
                    pairs = np.append(pairs, cards)
                    self.assign_classification(handClassification=6, cards=pairs)

                pairs = cards
                self.assign_classification(handClassification=1, cards=cards)

            # Check 3 of a kind
            if appearances == 3:
                # Check for full house
                if len(pairs) == 2:
                    pairs = np.append(pairs, cards)
                    self.assign_classification(handClassification=6, cards=pairs)

                pairs = cards
                self.assign_classification(handClassification=3, cards=cards)

            # Checks 4 of a kind
            if appearances == 4:
                self.assign_classification(handClassification=7, cards=cards)

        self.suits = suits
        self.ranks = ranks

    def assign_classification(self, handClassification, cards):
        classification = CardsClassification(handClassification)
        classification.set_cards(cards)
        self.classifications.add(classification)
    
    def median(self):

        median = None
        median_index = len(self.cards)//2 - 1

        if len(self.cards) % 2 == 0:
            first = self.cards[median_index].rank
            second = self.cards[median_index + 1].rank
            median = (first + second)/2.0
        else:
            median = self.cards[median_index].rank
        
        return median
    
    def card_range(self):
        range = self.cards[-1].rank - self.cards[0].rank
        return range
    
    # probability of suit mode
    def suit_mode(self):
        
        mode = 0.0

        for suit, cards in self.suits.items():

            suit_frequency = len(cards)

            if mode < suit_frequency:
                mode = suit_frequency
        
        return mode/len(self.cards)

    # number of duplicate ranked cards
    def count_duplicates(self):

        duplicates = 0

        for rank, cards in self.ranks.items():
            if len(cards) > 2:
                duplicates += 1
        
        return duplicates

    # most frequent duplicate classification (2: pair, 2-pair; 3: ThreeOAK; 4: FourOAK)
    def most_frequent_duplicate(self):

        largest_duplicate = 1

        for c in self.classifications:

            classification = c.get_classification()

            if classification == 1 or classification == 2:
                largest_duplicate = 2

            elif classification == 3:
                largest_duplicate = 3
                
            elif classification == 7:
                largest_duplicate = 4
        
        return largest_duplicate

    # max sequence size
    def sequence_size(self):

        max_sequence = 0
        sequence = 0
        previous_card = None

        for i in range(len(self.cards)):

            card = self.cards[i]

            if previous_card is None:
                previous_card = card
            else:
                
                rank = card.get_rank()
                previous_rank = previous_card.get_rank()
                
                if previous_rank == rank - 1:
                    sequence += 1

                if max_sequence < sequence:
                    max_sequence = sequence

        return max_sequence

class PokerAI():

    perceptrons = {}
    filename = './datasets/trained_model.txt'

    def __init__(self):
        self.build_perceptrons(self.filename)
    
    def calculate_inputs(self, pokerHand):

        median = pokerHand.median()
        card_range = pokerHand.card_range()
        suit_mode = pokerHand.suit_mode()
        duplicate_count = pokerHand.count_duplicates()
        most_frequent_duplicate = pokerHand.most_frequent_duplicate()
        sequence_size = pokerHand.sequence_size()
        
        inputs = np.array([median, card_range, suit_mode, duplicate_count, most_frequent_duplicate, sequence_size])

        return inputs

    def suggest_move(self, stageName, pokerHand):
        check = True

        inputs = self.calculate_inputs(pokerHand)
        decision = self.perceptrons[stageName].classify(inputs)

        if decision != 1:
            check = False

        return check

    def build_perceptrons(self, filename):

        trained_model_info = pd.read_csv(filename)

        perceptron_info = {}

        for i in trained_model_info.index:

            perceptron_name = trained_model_info.Name.iloc[i]
            weight_str = trained_model_info['Weights'].iloc[i].split()
            bias = float(trained_model_info['Bias'].iloc[i])
            
            weights = np.array([])

            for weight in weight_str:
                weights = np.append(weights, float(weight))
            
            perceptron_info[perceptron_name] = (weights, bias)

        for name, info in perceptron_info.items():

            weights = info[0]
            bias = info[1]

            self.perceptrons[name] = Perceptron.Perceptron(wvec_size=5, lrate=.2, weights=weights, bias=bias)

class CardsClassification:

    cards = np.array([])

    def __init__(self, classification):
        self.classification = classification
    
    def set_cards(self, cards):
        self.cards = np.append(self.cards, cards)
        self.cards = np.sort(self.cards, axis=None)
    
    def get_classification(self):
        return self.classification
    
    def display(self):
        print()
        print(f"classification: {self.classification}")
        for card in self.cards:
            card.display()
        print()
    
    def __lt__(self, other):
        return self.classification < other.classification

class Deck:

    suits = ['spades', 'clubs', 'hearts', 'diamonds']

    def __init__(self):
        self.cards = self.new_deck()

    def new_deck(self):
        deck = np.array([])

        for suit in self.suits:
            for rank in range(1,14):
                card = Card(suit, rank)
                deck = np.append(deck, card)

        return deck
    
    def shuffle_deck(self):
        np.random.shuffle(self.cards)

    def display_deck(self):
        for card in self.cards:
            card.display()
    
    def draw_card(self, numberOfDraws = 1):
        cards = self.cards[range(numberOfDraws)]
        self.cards = np.delete(self.cards, range(numberOfDraws))
        return cards

class Card:

    card_names = {1: 'Ace', 11: 'Jack', 12: 'Queen', 13: 'King'}

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        if self.rank in self.card_names:
            self.name = self.card_names[self.rank]
        else:
            self.name = rank
    
    def get_suit(self):
        return self.suit
    
    def get_rank(self):
        return self.rank

    def display(self):
        print(f"{self.name} of {self.suit}.")
        
    def __lt__(self, other):
        return self.rank < other.rank

def playGames(numberOfRuns=1, save=False):

    columns = ['rank1', 'suit1', 'rank2', 'suit2', 'rank3', 'suit3',
               'rank4', 'suit4', 'rank5', 'suit5', 'rank6', 'suit6',
               'rank7', 'suit7', 'class', 'win']

    games = pd.DataFrame(columns=columns)

    for i in range(numberOfRuns):

        print(f'game: {i}')

        game = PokerGame(NumberOfPlayers=2)
        winner, players, shared_cards = game.play()

        if save:
            perspectives = {}
            for player in players:

                row = {}

                for i in range(len(player.cards)):
                    card = player.cards[i]

                    row[f'rank{i + 1}'] = player.cards[i].rank
                    row[f'suit{i + 1}'] = player.cards[i].suit
                
                for i in range(len(shared_cards)):

                    card = shared_cards[i]

                    row[f'rank{i + len(players) + 1}'] = card.rank
                    row[f'suit{i + len(players) + 1}'] = card.suit
                
                row['class'] = max(player.poker_hand.classifications).classification

                if winner is None:
                    row['win'] = 1
                else:
                    if winner.number == player.number:
                        row['win'] = 1
                    else:
                        row['win'] = -1

                perspectives[player.number] = row
            
            for perspective in perspectives:
                games = games.append(perspectives[perspective], ignore_index = True)
        
            # print(games)
    if save:
        games.to_csv('games.csv')

def main():
    playGames(numberOfRuns=10000,save=True)

if __name__ == "__main__":
    main()