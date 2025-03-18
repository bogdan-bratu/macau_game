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
        self.deck.append(Card('Joker', 'Red'))
        self.deck.append(Card('Joker', 'Black'))
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
        self.hand.append(deck.get_deck().pop(random.randint(0, len(deck.get_deck()) - 1)))
    
    def draw_cards_obliged(self, deck, to_draw):
        for _ in range(to_draw):
            self.draw_card(deck)

    def draw_cards_beginning(self, deck):
        for _ in range(5):
            card = deck.get_deck().pop(random.randint(0, len(deck.get_deck()) - 1))
            self.hand.append(card)

    def show_hand(self):
        print(self.__str__())

    def check_if_can_put_card(self, pile):
        for card in self.hand:
            if card.rank == pile.get_pile().rank or card.suit == pile.get_pile().suit or card.rank in ['A', 'Joker']:
                return True
        return False
    
    def check_if_can_give_cards(self, pile):
        for card in self.hand:
            if card.rank in ['2', '3', 'Joker'] and (card.rank == pile.rank or card.suit == pile.suit):
                return True
    
    def action2(self, deck, pile, to_draw=None):
        if to_draw:
            if self.check_if_can_give_cards():
                self.action(deck, pile, to_draw)
            else:
                print('You can\'t give any cards. You will draw {to_draw} cards')
                self.draw_cards_obliged(deck, to_draw)
        elif not self.check_if_can_put_card(pile):
            print('You can\'t put any card. Automatically drawing a card')
            self.draw_card(deck)
        else:
            self.action(deck, pile)

    def action(self, deck, pile, to_draw=None):
        response = None
        while True:
            if to_draw:
                response = self.put_card(pile, response, to_draw)
                if not response:
                    continue
                return response
            inp = input("Choose action: 1. Put card ; 2. Draw card: ")
            try:
                inp = int(inp)
            except:
                print("Invalid input")
                continue
            if inp == 1:
                return_val = self.put_card(pile, response, to_draw)
                if return_val == False:
                    continue
                return return_val
            elif inp == 2:
                self.draw_card(deck)
                return response

    def put_card(self, pile : Pile, response, to_draw=None):
        card_wanted = None
        while True:    
            rank, suit = input(f"Choose card (ex. 5 trefla): ").split(" ")
            suit = colour_dict[suit]
            #going through the hand to see if card chosen is in hand
            for card in self.hand:
                if card.rank == rank and card.suit == suit:
                    #found the card
                    #checking if there are cards to draw
                    if to_draw:
                        print(f'The other player wants you to draw {to_draw} cards')
                        if card.rank in ['2', '3', 'Joker'] and (card.rank == pile.rank or card.suit == pile.suit):
                            #succesfully found the card, and it can be put
                            card_wanted = card
                            self.hand.remove(card)
                            #updating cards to draw
                            response = to_draw + card.rank
                            return response
                        else:
                            print('You need to give cards')
                            continue
                    #no cards to draw
                    elif card.suit == pile.get_pile().suit or card.rank == pile.get_pile().rank or card.rank in ['A', 'Joker']:
                        #found the card, and it can be put
                        #checking exceptional cases
                        if card.rank == 'A':
                            suit = input(f"Choose suit to change to: ")
                            try:
                                suit = colour_dict[suit]
                            #joker
                            except KeyError:
                                pass
                            pile.set_suit(suit)
                        elif card.rank == '4':
                            response = 'stay_a_round'
                        elif card.rank in ['2', '3', 'Joker']:
                            response = self.give_cards(card)
                        card_wanted = card
                        self.hand.remove(card)
                        break
                #checking next card
                else:
                    continue
            #card was found
            if card_wanted:
                pile.update_pile(card_wanted)
                return True
            #card was not found
            else:
                print("You can't put that card")
                return False

    def give_cards(self, card):
        if card.rank == 'Joker':
            if card.suit == 'Red':
                cards_to_give = 10
            else:
                cards_to_give = 5
        else:
            cards_to_give = int(card.rank)
        return cards_to_give


    def stay_a_round(self, ):
        response = 'stay_a_round'
        return response

    def multiple_cards(self, ):
        pass

    def add_cards_to_give(self, ):
        pass

    def macao(self,):
        pass

    def win_condition(self, ):
        pass


colour_dict = {
    'trefla': '\u2663',
    'inima': '\u2665',
    'romb': '\u2666',
    'frunza': '\u2660'
}

def read_players():
    no_players = 2
    players = []
    for _ in range(no_players):
        player = Player()
        players.append(player) 
    return players


#trefla, inima, romb, frunza
suits = ["\u2663", "\u2665", "\u2666", "\u2660"]
ranks = list(map(str, range(2, 11))) + ['J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, 'Joker': [5, 10]}

def main():
    deck = Deck()
    players = read_players()

    for ind, player in enumerate(players):
        print(f'\nPlayer {ind+1}')
        player.draw_cards_beginning(deck)
        player.show_hand()

    pile = Pile()
    pile.get_initial_card(deck.get_deck())
    pile.show_pile()

    response = None
    to_draw = None
    while True:
        for ind, player in enumerate(players):
            if response != 'stay_a_round':
                if type(response) == int:
                    to_draw = response
                response = None
                print(f'\nPlayer {ind+1}')
                player.show_hand()
                response = player.action2(deck, pile, to_draw)
                player.show_hand()
                pile.show_pile()
            else:
                response = None
                


if __name__ == "__main__":
    main()


