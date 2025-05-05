from macau import *


deck = Deck()

players = read_players(test = True)
for ind, player in enumerate(players):
    print(f"\nPlayer {ind+1}")
    player.draw_cards_beginning(deck)
    player.show_hand()

pile = Pile(test=True)
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