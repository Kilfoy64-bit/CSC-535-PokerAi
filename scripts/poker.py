import numpy as np
import pandas as pd
import operator

class PokerGame:

    shared_cards = np.array([])
    
    def __init__(self, NumberOfPlayers = 2):
        self.players = np.array([Player(i) for i in range(NumberOfPlayers)])
        self.deck = Deck()

    def play(self):
        
        self.shared_cards = np.array([])
        # self.deck.display_deck()
        self.deck.shuffle_deck()

        # print("START")
        # initial draw
        for player in self.players:
            player.add_cards(self.deck.draw_card(numberOfDraws=2))
        
        # print("Initial draw.")
        # self.display_players()

        # flop draw
        self.draw_cards(3)
        # self.display_table()

        # turn draw
        self.draw_cards(1)
        # self.display_table()

        # river draw
        self.draw_cards(1)

        # self.display_table()

        # self.display_players()

        winner, classification = self.determine_winner()
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

        poker_hands = ["Highest card", "One pair", "Two pair", "Three of a kind", "Straight", "Flush", "Full house", "Four of a kind", "Straight flush", "Royal flush"]
        hand_name = poker_hands[classification]
        # print(f"#{winner.number} won with {hand_name}")
        return winner.number, self.players, self.shared_cards

    def determine_winner(self):

        classifications = {}
        classification_type = None
        winner = None

        for player in self.players:
            players_hand = player.get_poker_hand()
            hand_classifications = players_hand.get_classifications()
            # print(f"CLASSIFICATIONS FOR PLAYER {player.number}")
            # for c in hand_classifications:
            #     c.display()
            hand_classification = max(hand_classifications)

            classifications[player] = hand_classification
        
        winner = max(classifications.items(), key=operator.itemgetter(1))[0]
        classification_type = classifications[winner].get_classification()

        return winner, classification_type
    
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

    def __init__(self, cards):
        self.cards = cards
        self.classifications = set()
        self.classify()
    
    def get_classifications(self):
        return self.classifications
    
    def get_cards(self):
        return self.cards
    
    def display(self):
        for card in self.cards:
            card.display()

    def classify(self):

        sorted_cards = np.sort(self.cards, axis=None)

        flush = False
        straight = False

        ranks = {}
        suits = {}

        straight_count = 1
        straight_cards = np.array([])

        ace_present = False

        highest_rank = 0
        high_card = None
        
        previous_card = None

        for i in range(len(sorted_cards)):

            card = sorted_cards[i]
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
            
            if previous_card is None:
                previous_card = card

            else:
                
                if highest_rank < rank:
                    highest_rank = rank
                    high_card = card

                previous_rank = previous_card.get_rank()
                
                # Accumulates points towards a straight classification
                if previous_rank == rank - 1:
                    straight_count += 1
                # Resets points
                else:
                    straight_count = 1
                
                # Defines straight
                if straight_count >= 5:
                    straight = True
                    straight_cards = np.arrays([sorted_cards[i-4], sorted_cards[i-3], sorted_cards[i-2], sorted_cards[i-1], sorted_cards[i]])

                # Handles ace high straights
                elif straight_count == 4 and rank == 13 and ace_present:
                    straight = True
                    straight_cards = np.arrays([sorted_cards[i-3], sorted_cards[i-2], sorted_cards[i-1], sorted_cards[i], sorted_cards[0]])

        if straight:
            self.assign_classification(handClassification=4, cards=straight_cards)

        # Assigns junk card classification
        if ace_present:
            high_card = sorted_cards[0]
        self.assign_classification(handClassification=0, cards=high_card)

        # Checking for float classification
        for suit, cards in suits.items():
            if len(cards) == 5:
                flush = True

            if flush:
                self.assign_classification(handClassification=5, cards=cards)

                # Checking for special straight classifications (straight flush, royal flush)
                if straight:
                    if cards == straight_cards:
                        self.assign_classification(handClassification=8, cards=cards)

                        if cards[-1].rank == 1:
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
    
    def assign_classification(self, handClassification, cards):
        classification = CardsClassification(handClassification)
        classification.set_cards(cards)
        self.classifications.add(classification)

class CardsClassification:

    cards = np.array([])

    def __init__(self, classification):
        self.classification = classification
    
    def set_cards(self, cards):
        self.cards = np.append(self.cards, cards)
    
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
        self.deck = self.new_deck()

    def new_deck(self):
        deck = np.array([])

        for suit in self.suits:
            for rank in range(1,14):
                card = Card(suit, rank)
                deck = np.append(deck, card)

        return deck
    
    def shuffle_deck(self):
        np.random.shuffle(self.deck)

    def display_deck(self, numberOfCards = 52):
        for index in range(numberOfCards):
            self.deck[index].display()
    
    def draw_card(self, numberOfDraws = 1):
        cards = np.random.choice(self.deck, numberOfDraws, replace=False)
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

def createDataset(numberOfRuns):

    columns = ['rank1', 'suit1', 'rank2', 'suit2', 'rank3', 'suit3',
               'rank4', 'suit4', 'rank5', 'suit5', 'rank6', 'suit6',
               'rank7', 'suit7', 'class', 'win']

    games = pd.DataFrame(columns=columns)

    for i in range(numberOfRuns):


        game = PokerGame(NumberOfPlayers=2)
        winner, players, shared_cards = game.play()

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
            if winner == player.number:
                row['win'] = 1
            else:
                row['win'] = -1

            perspectives[player.number] = row
        
        for perspective in perspectives:
            games = games.append(perspectives[perspective], ignore_index = True)
        
        # print(perspectives)
        # player1 = players[1]

        # row['class'] = classification
        # row['win'] =
    print(games)
    games.to_csv('games.csv')

def main():
    games = 100
    createDataset(games)

if __name__ == "__main__":
    main()