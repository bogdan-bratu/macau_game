import random
import typing

class Card():
    def __init__(self, rank, suit) -> None:
        self.rank = rank
        self.suit = suit
    
    def __str__(self) -> str:
        return f'{self.rank} {self.suit}'

class Deck():
    def __init__(self) -> None:
        self.deck = []
        self.make_deck()

    def __str__(self) -> str:
        s = ''
        for card in self.deck:
            s += f'{card}\n'
        return s

    def make_deck(self):
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit))
        return self
    
    def get_deck(self):
        return self.deck
    
class Pile():
    def __init__(self) -> None:
        self.pile = None
        self.pile_changed_suit = None

    def __str__(self):
        return f"\nPile\n{self.pile}"

    def show_pile(self):
        print(self.__str__())
        if self.pile_changed_suit:
            print(f'Changed suit to: {self.pile_changed_suit}')

    def get_initial_card(self, deck):
        card = deck.pop(random.randint(0, len(deck) - 1))
        self.update_pile(card)

    def update_pile(self, card):
        self.pile = card

    def get_pile(self):
        if self.pile_changed_suit:
            return Card(rank='bla', suit=self.pile_changed_suit)
        else: 
            return self.pile
    
    def set_suit(self, suit):
        self.pile_changed_suit = suit
        pass

class Player():
    def __init__(self) -> None:
        self.hand = []

    def __str__(self) -> str:
        s = ''
        for card in self.hand:
            s += f"{card} \t"
        return s
    
    def draw_card(self, deck):
        card = deck.get_deck().pop(random.randint(0, len(deck.get_deck()) - 1))
        self.hand.append(card)
        return self

    def draw_cards_beginning(self, deck):
        for i in range(5):
            card = deck.get_deck().pop(random.randint(0, len(deck.get_deck()) - 1))
            self.hand.append(card)

    def show_hand(self):
        print(self.__str__())

    def action(self, deck, pile):
        while True:
            response = int(input("Choose action: 1. Put card ; 2. Draw card "))
            if response == 1:
                if not self.put_card(pile):
                    continue
                break
            elif response == 2:
                self.draw_card(deck)
                break

    def put_card(self, pile : Pile):
        card_wanted = None
        while True:
            rank, suit = input(f"Choose card. Copy and paste the card number and symbol from above: ").split(" ")
            for card in self.hand:
                if card.rank == rank and card.suit == suit:
                    if card.rank in ['A', 'Joker'] or card.suit == pile.get_pile().suit or card.rank == pile.get_pile().rank:
                        if card.rank == 'A':
                            suit = input(f"Choose suit to change ").split(" ")
                            pile.set_suit(suit)
                        elif card.rank == '4':
                            self.stay_a_round()
                        elif card.rank in ['2', '3', 'Joker']:
                            self.give_cards(card)
                        card_wanted = card
                        self.hand.remove(card)
                        break
                    else:
                        continue
            if card_wanted:
                pile.update_pile(card)
                return True
            else:
                print("You can't put that card")
                return False

    def give_cards(self, card):
        pass

    def stay_a_round(self, ):
        pass

    def multiple_cards(self, ):
        pass

    def add_cards_to_give(self, ):
        pass

    def macao(self,):
        pass

    def win_condition(self, ):
        pass


    


#trefla, inima, romb, frunza
suits = ["\u2663", "\u2665", "\u2666", "\u2660"]
ranks = list(map(str, range(2, 11))) + ['J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, 'Joker': [5, 10]}

def main():
    deck = Deck()
    no_players = 2
    players = []
    for i in range(no_players):
        player = Player()
        players.append(player) 

    for ind, player in enumerate(players):
        print(f'\nPlayer {ind+1}')
        player.draw_cards_beginning(deck)
        player.show_hand()

    pile = Pile()
    pile.get_initial_card(deck.get_deck())
    pile.show_pile()

    while True:
        for ind, player in enumerate(players):
            print(f'\nPlayer {ind+1}')
            player.show_hand()
            player.action(deck, pile)
            player.show_hand()
            pile.show_pile()


if __name__ == "__main__":
    main()


