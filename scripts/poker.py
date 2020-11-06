import numpy as np

class PokerGame:

    shared_cards = np.array([])
    
    def __init__(self, NumberOfPlayers = 2):
        self.players = np.array([Player(i) for i in range(NumberOfPlayers)])
        self.deck = Deck()

    def play(self):
        
        self.shared_cards = np.array([])
        self.deck.shuffle_deck()

        print("START")
        self.display_players()

        # initial draw
        for player in self.players:
            player.add_cards(self.deck.draw_card(numberOfDraws=2))
        
        print("Initial draw.")
        self.display_players()

        # flop draw
        print("flop")
        self.shared_cards = self.deck.draw_card(numberOfDraws=3)
        self.display_table()

        # turn draw
        print("turn")
        self.shared_cards = self.deck.draw_card()
        self.display_table()

        # river draw
        print("river")
        self.shared_cards = self.deck.draw_card()
        self.display_table()
    
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
    
    def add_cards(self, cards):
        self.cards = np.append(self.cards, cards)
    
    def display(self):
        print(f"Player Number: {self.number}")
        for card in self.cards:
            card.display()

class PokerHand:

    def __init__(self, cards = None):
        self.cards = cards
    
    def get_cards(self):
        return self.cards
    
    def display(self):
        for card in self.cards:
            card.display()

class Deck:

    suits = ['spades', 'clubs', 'hearts', 'diamonds']

    def __init__(self):
        self.deck = self.new_deck()

    def new_deck(self):
        deck = np.array([])

        for suit in self.suits:
            for value in range(14):
                card = Card(suit, value)
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

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def get_suit(self):
        return self.suit
    
    def get_value(self):
        return self.value

    def display(self):
        print(f"Suit: {self.suit}, Value: {self.value}")

def main():
    game = PokerGame(NumberOfPlayers=2)
    game.play()

if __name__ == "__main__":
    main()