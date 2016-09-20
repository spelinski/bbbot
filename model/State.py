from model.Flags import Flags


class State(object):
    NAME = 'BBBot'

    def __init__(self):
        self.reply = ''
        self.seat = ''
        self.colors = ()
        self.hand = []
        self.deck = []
        self.flags = Flags()
        self.flag_statuses = ['unclaimed'] * Flags.NUM_FLAGS
        self.opponents_last_play = {}
        self.init_deck()

    def update_flag_cards(self, flag, seat, cards):
        self.flags.add_cards(flag, seat, cards)
        self.remove_cards_from_deck(cards)

    def get_full_flags(self):
        return [flag + 1 for flag in range(Flags.NUM_FLAGS) if len(self.flags.sides[self.seat][flag]) == 3]

    def init_deck(self):
        colors = ["color1","color2","color3","color4","color5","color6"]
        for color in colors:
            for i in range(1,11):
                self.deck.append((i,color))

    def remove_cards_from_deck(self, cards):
        for card in cards:
            for deck_card in self.deck:
                if card == deck_card:
                    self.deck.remove(deck_card)
                    break
