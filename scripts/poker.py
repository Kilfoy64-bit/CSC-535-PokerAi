import numpy as np

class PokerGame:

    shared_cards = np.array([])
    
    def __init__(self, NumberOfPlayers = 2):
        self.players = np.array([Player(i) for i in range(NumberOfPlayers)])
        self.deck = Deck()

    def play(self):
        
        self.shared_cards = np.array([])
        # self.deck.display_deck()
        self.deck.shuffle_deck()

        print("START")
        # self.display_players()

        # initial draw
        for player in self.players:
            player.add_cards(self.deck.draw_card(numberOfDraws=2))
        
        print("Initial draw.")
        self.display_players()

        # flop draw
        # print("flop")
        self.shared_cards = self.deck.draw_card(numberOfDraws=3)
        # self.display_table()

        # turn draw
        # print("turn")
        self.shared_cards = np.append(self.shared_cards, self.deck.draw_card())
        # self.display_table()

        # river draw
        # print("river")
        self.shared_cards = np.append(self.shared_cards, self.deck.draw_card())
        self.display_table()
    
    # TODO: write functionality to calculate and assign possible poker hands to winner, then classify each poker hand
    # and determine the winner basec on the player's strongest possible poker hand.
    def determine_winner(self):
        pass
    
    def display_players(self):
        for player in self.players:
            player.display()
    
    def display_table(self):
        print("Table:")
        for card in self.shared_cards:
            card.display()

class Player:
    
    def __init__(self, number):
        self.cards = np.array([])
        self.number = number
        # NOTE: poker_hands will hold all possible PokerHands available to the player object
        # self.poker_hands = np.array([])
    
    def add_cards(self, cards):
        self.cards = np.append(self.cards, cards)
    
    def display(self):
        print(f"Player {self.number}")
        for card in self.cards:
            card.display()
    
    # Write functionality that given 7 cards (2 unique player cards and 5 shared table cards)
    # Determine every combination of cards in sets of 5 (order does not matter)
    def determine_hands(self, cards):
        pass

class PokerHand:

    def __init__(self, cards = None):
        self.cards = cards
        self.classifications = self.classify()
    
    def get_cards(self):
        return self.cards
    
    def display(self):
        for card in self.cards:
            card.display()
        
    def classify(self):

        classifications = set()
        flush = True
        straight = True
        ranks = {}

        sorted_cards = np.sort(self.cards)

        previous_card = None
        high_ace = False

        for card in sorted_cards:

            rank = card.get_rank()
            suit = card.get_suit()

            if rank not in ranks:
                ranks[rank] = 1
            else:
                ranks[rank] += 1
            
            if previous_card is None:
                previous_card = card

            else:
                if rank is 1 and high_ace:
                    rank = 14

                previous_rank = previous_card.get_rank()
                previous_suit = previous_card.get_suit()

                if previous_suit is not suit:
                    flush = False
                
                
                if previous_rank is not rank - 1:
                    straight = False
                
                # Handling high ace cases
                if previous_rank is 1 and not straight:
                    sorted_cards = np.delete(sorted_cards, 0)
                    sorted_cards = np.append(sorted_cards, previous_card)
                    high_ace = True
                    straight = True

        high_card = max(ranks, key = ranks.get)

        # Card Classifications
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
        if straight:
                classification = CardsClassification(4, high_card)
                classifications.add(classification)

        if flush:
            classification = CardsClassification(5, high_card)
            classifications.add(classification)

        if straight and flush:
            classification = CardsClassification(8, high_card)
            classifications.add(classification)

        if straight and flush and high_card is 1:
            classification = CardsClassification(9)

        for rank, appearances in ranks.items():
            # Check for full house
            if 1 or 3 in classifications:
                if appearances is 2 or 3:
                    classification = CardsClassification(6)
                    classifications.add(classification)

            # Check Pair
            if appearances is 2:
                if 1 in classifications:
                    classification = CardsClassification(2)
                    classifications.add(classification)
                classification = CardsClassification(1, rank)
                classifications.add(classification)

            # Check 3 of a kind
            if appearances is 3:
                classification = CardsClassification(3, rank)
                classifications.add(classification)

            # Checks 4 of a kind
            if appearances is 4:
                classification = CardsClassification(7, rank)
                classifications.add(classification)

        return classifications

class CardsClassification:
    def __init__(self, classification, rank = None):
        self.classification = classification
        self.rank = rank

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

def main():
    game = PokerGame(NumberOfPlayers=2)
    game.play()

if __name__ == "__main__":
    main()