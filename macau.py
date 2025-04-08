from random import randint


class Card:
    def __init__(self, rank, suit) -> None:
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return f"{self.rank} {self.suit}"


class Deck:
    def __init__(self) -> None:
        self.deck = []
        self.make_deck()

    def __str__(self) -> str:
        return printing_method(self.deck, "\n")

    def make_deck(self):
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit))
        self.deck.append(Card("Joker", "Red"))
        self.deck.append(Card("Joker", "Black"))
        return self

    def get_deck(self):
        return self.deck


class Pile:
    def __init__(self) -> None:
        self.pile = None
        self.pile_changed_suit = None

    def __str__(self):
        return f"\nPile\n{self.pile}"

    def show_pile(self):
        print(self.__str__())
        if self.pile_changed_suit:
            print(f"Changed suit to: {self.pile_changed_suit}")
        # self.pile_changed_suit = None

    def get_initial_card(self, deck_obj):
        deck = deck_obj.get_deck()
        card = deck.pop(randint(0, len(deck) - 1))
        self.update_pile(card)

    def update_pile(self, card):
        self.pile = card

    def unset_suit(self):
        self.pile_changed_suit = None

    def get_pile_suit(self):
        if self.pile_changed_suit:
            return self.pile_changed_suit
        return self.pile.suit

    def get_pile(self):
        return self.pile

    def set_suit(self, suit):
        self.pile_changed_suit = suit


class Player:
    def __init__(self) -> None:
        self.hand = []

    def __str__(self) -> str:
        return printing_method(self.hand, "\t")

    def draw_card(self, deck_obj: Deck):
        deck = deck_obj.get_deck()
        self.hand.append(deck.pop(randint(0, len(deck) - 1)))
        return None

    def draw_cards_obliged(self, deck, to_draw):
        for _ in range(to_draw):
            self.draw_card(deck)

    def draw_cards_beginning(self, deck_obj: Deck):
        for _ in range(5):
            deck = deck_obj.get_deck()
            card = deck.pop(randint(0, len(deck) - 1))
            self.hand.append(card)

    def show_hand(self):
        print(self.__str__())

    def check_if_can_put_card(self, pile_obj: Pile):
        pile = pile_obj.get_pile()
        for card in self.hand:
            if (
                card.rank == pile.rank
                or card.suit == pile_obj.get_pile_suit()
                or card.rank in ["A", "Joker"]
            ):
                return True
        return False

    def check_if_can_give_cards(self, pile_obj: Pile):
        pile = pile_obj.get_pile()
        for card in self.hand:
            if (
                card.rank in ["2", "3"]
                and (card.rank == pile.rank or card.suit == pile_obj.get_pile_suit())
            ) or card.rank == "Joker":
                return True

    def action2(self, deck: Deck, pile, to_draw=None):
        if to_draw:
            if self.check_if_can_give_cards(pile):
                response = self.action(deck, pile, to_draw)
            else:
                print(f"You can't give any cards. You will draw {to_draw} cards")
                self.draw_cards_obliged(deck, to_draw)
                response = 0
                return response
        elif not self.check_if_can_put_card(pile):
            print("You can't put any card. Automatically drawing a card")
            response = self.draw_card(deck)
            return response
        else:
            response = self.action(deck, pile)
            return response

    def action(self, deck, pile, to_draw=None):
        while True:
            if to_draw:
                # at the moment you can't give more than 1 card that gives cards
                response = self.put_card(pile, to_draw)
                if not response:
                    continue
                return response
            inp = input("Choose action: 1. Put card ; 2. Draw card ; 3. Put cards: ")
            try:
                inp = int(inp)
            except:
                print("Invalid input. Please choose 1, 2 or 3!")
                continue
            if inp == 1:
                response = self.put_card(pile, to_draw)
                if not response:
                    continue
                return response
            elif inp == 2:
                response = self.draw_card(deck)
                return response
            elif inp == 3:
                card_from_list_can_not_be_put = False
                card_list = input(
                    "Choose cards to put (ex. 5 trefla, 5 inima, etc): "
                ).split(", ")
                for card in card_list:
                    print(f"Checking if {card} can be put")
                    response = self.put_card(
                        pile, to_draw, chosen_above=True, card=card
                    )
                    if not response:
                        card_from_list_can_not_be_put = True
                        break
                if card_from_list_can_not_be_put:
                    continue
                return response

    # def put_cards(self, pile, response, to_draw):
    #     card_list = input('Choose cards to put (ex. 5 trefla, 5 inima, etc): ').split(", ")
    #     for card in card_list:
    #         self.put_card(pile, response, to_draw, chosen_above = True, card=card)

    def put_card(self, pile_obj: Pile, to_draw=None, chosen_above=False, card=None):
        card_wanted = None
        pile = pile_obj.get_pile()
        while True:
            if not chosen_above:
                rank, suit = input(f"Choose card (ex. 5 trefla): ").split(" ")
            else:
                rank, suit = card.split(" ")
            suit = colour_dict[suit]
            # going through the hand to see if card chosen is in hand
            for card in self.hand:
                if card.rank == rank and card.suit == suit:
                    # found the card
                    # checking if there are cards to draw
                    if to_draw:
                        print(f"The other player wants you to draw {to_draw} cards")
                        if (
                            card.rank in ["2", "3"]
                            and (card.rank == pile.rank or card.suit == pile.suit)
                            or card.rank == "Joker"
                        ):
                            # succesfully found the card, and it can be put
                            card_wanted = card
                            self.hand.remove(card)
                            # updating cards to draw
                            response = to_draw + self.give_cards(card)
                        else:
                            print("You need to give cards")
                            continue
                    # no cards to draw
                    elif (
                        # checking if suit was changed
                        card.suit == pile_obj.get_pile_suit()
                        or card.rank == pile.rank
                        or card.rank in ["A", "Joker"]
                    ):
                        # found the card, and it can be put
                        # unsetting the suit change
                        pile_obj.unset_suit()
                        # checking exceptional cases
                        if card.rank == "A":
                            suit = input(f"Choose suit to change to (ex. trefla): ")
                            suit = colour_dict[suit]
                            pile_obj.set_suit(suit)
                            response = None
                        # response will be used both as a checker and as a value
                        elif card.rank == "4":
                            response = "stay_a_round"
                        elif card.rank in ["2", "3", "Joker"]:
                            response: int = self.give_cards(card)
                        else:
                            response = None
                        # setting the found card variable
                        card_wanted = card
                        self.hand.remove(card)
                        break
                # checking next card
                else:
                    continue
            # card was found
            if card_wanted:
                if response is None:
                    response = True
                pile_obj.update_pile(card_wanted)
                return response
            # card was not found
            else:
                print("You can't put that card")
                return False

    def give_cards(self, card) -> int:
        if card.rank == "Joker":
            if card.suit == "red":
                cards_to_give = 10
            else:
                cards_to_give = 5
        else:
            cards_to_give = int(card.rank)
        return cards_to_give


def read_players() -> list[Player]:
    no_players = 2
    players = []
    for _ in range(no_players):
        player = Player()
        players.append(player)
    return players


def printing_method(lis, spacing):
    s = ""
    for card in lis:
        s += f"{card}{spacing}"
    return s


# trefla, inima, romb, frunza
suits = ["\u2663", "\u2665", "\u2666", "\u2660"]
ranks = list(map(str, range(2, 11))) + ["J", "Q", "K", "A"]
values = {"2": 2, "3": 3, "Joker": [5, 10]}

colour_dict = {
    "trefla": "\u2663",
    "inima": "\u2665",
    "romb": "\u2666",
    "frunza": "\u2660",
    "Red": "red",
    "Black": "black",
    # "red": ["\u2665", "\u2666"],
    # "black": ["\u2663", "\u2660"],
}


def main():
    deck = Deck()
    players = read_players()
    for ind, player in enumerate(players):
        print(f"\nPlayer {ind+1}")
        player.draw_cards_beginning(deck)
        player.show_hand()

    pile = Pile()
    pile.get_initial_card(deck)
    pile.show_pile()

    response = None
    to_draw = None
    while True:
        for ind, player in enumerate(players):
            print(f"\nPlayer {ind+1}")
            if response != "stay_a_round":
                if type(response) == int:
                    if response == 0:
                        to_draw = None
                    else:
                        to_draw = response
                player.show_hand()
                response = player.action2(deck, pile, to_draw)
                player.show_hand()
                pile.show_pile()
            else:
                print("You need to stay a round.")
                response = None


if __name__ == "__main__":
    main()
