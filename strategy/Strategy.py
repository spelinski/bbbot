from random import shuffle
import itertools
from model.Flags import Flags
from model.Card import Card


class Strategy(object):

    def __init__(self, seeded_json):
        self.seeded_json = seeded_json

    def decide(self, state):
        self.__seeded_strategy(state)

    def __seeded_strategy(self, state): 
        if self.__able_to_play_a_card(state):
            flags = self.__unclaimed_minus_full_flags(state)
            playFlag,playCard = self.__get_card_and_flag_for_play(flags, state)
            state.reply = self.__reply_text(playFlag, playCard)
        else:
            self.__no_moves(state)

    def __get_card_and_flag_for_play(self, flags, state):
        flag_to_play = 1
        max_win_prob = 0
        card_to_play = (0,"color1")
        for flag in flags:
            if state.seat == "north":
                already_on_flag = state.flags.north[flag-1]
            else :
                already_on_flag = state.flags.south[flag-1]

            if len(already_on_flag) < 2:
                my_combos = list(itertools.combinations(state.deck,(2-len(already_on_flag))))

            for card_in_hand in state.hand:
                if len(already_on_flag) == 2:
                    my_combos = list(itertools.combinations([tuple(card_in_hand)],1))
                for combo in my_combos:
                    cards_already_owned = 0
                    if len(already_on_flag) < 2:
                        tempList = [tuple(card_in_hand)]
                        for temp_card in combo:
                            tempList.append(temp_card)
                        combo = tuple(tempList)

                    probability_to_get_combo = 0
                    
                    for combo_card in combo:
                        for hand_card in state.hand:
                            if combo_card == hand_card:
                                cards_already_owned += 1

                    for on_flag_card in already_on_flag:
                        combo = list(combo)
                        combo.append(on_flag_card)
                        combo = tuple(combo)
                        cards_already_owned += 1
                    if self.seeded_json["valid_formations"][str(combo)]["win_chance"] > max_win_prob:
                        flag_to_play = flag
                        max_win_prob = self.seeded_json["valid_formations"][str(combo)]["win_chance"]
                        card_to_play = combo[0]
        return flag_to_play,card_to_play


    def __no_moves(self, state):
        state.reply = 'no moves'

    def __able_to_play_a_card(self, state):
        return len(state.hand) > 0 and len(self.__unclaimed_flags(state)) > 0 and len(self.__full_flags(state)) < Flags.NUM_FLAGS

    def __unclaimed_flags(self, state):
        return [i for i, status in enumerate(state.flag_statuses, start=1) if status == "unclaimed"]

    def __full_flags(self, state):
        return state.get_full_flags()

    def __reply_text(self, flag, card):
        return 'play {} {}'.format(flag, Card().card_to_text(card))

    def __get_first(self, list):
        return list[0]

    def __unclaimed_minus_full_flags(self, state):
        return [flag for flag in self.__unclaimed_flags(state) if flag not in self.__full_flags(state)]