from random import shuffle
import itertools
from model.Flags import Flags
from model.Card import Card
import threading
import json


class Strategy(object):

    def __init__(self):
        with open('seed.txt') as json_data:
            self.seeded_json = json.load(json_data)

    '''def start_json_thread(self):
        thread = threading.Thread(target=self.__load_json_file)
        thread.daemon = True
        thread.start()

    def __load_json_file(self):
        with open('seed.txt') as json_data:
            seeded_data = json.load(json_data)
            self.seeded_json = seeded_data
            self.is_json_loaded = True'''

    def decide(self, state):
        self.__seeded_strategy(state)

    def __seeded_strategy(self, state): 
        flags = self.__unclaimed_minus_full_flags(state)
        playFlag,playCard = self.__get_card_and_flag_for_play(flags, state)
        state.reply = self.__reply_text(playFlag, playCard)

    def __get_opponent_best_win_prob(self,opponent_on_flag,state):
        max_win_prob = 0
        my_combos = list(itertools.combinations(state.deck,(3-len(opponent_on_flag))))

        for combo in my_combos:
            for on_flag_card in opponent_on_flag:
                combo = list(combo)
                combo.append(on_flag_card)
                combo = tuple(combo)
            combo = self.sort_cards(combo)
            win_prob = self.seeded_json["valid_formations"][str(combo)]["win_chance"]

            if win_prob > max_win_prob:
                max_win_prob = win_prob
        return max_win_prob


    def __get_card_and_flag_for_play(self, flags, state):
        flag_to_play = 1
        max_win_prob = 0
        card_to_play = (0,"color1")
        for flag in flags:
            if state.seat == "north":
                already_on_flag = state.flags.north[flag-1]
                already_on_flag_opponent = state.flags.south[flag-1]
            else :
                already_on_flag = state.flags.south[flag-1]
                already_on_flag_opponent = state.flags.north[flag-1]

            opponent_win_prob = self.__get_opponent_best_win_prob(already_on_flag_opponent,state)

            if len(already_on_flag) < 2:
                my_combos = list(itertools.combinations(state.deck,(2-len(already_on_flag))))

            for card_in_hand in state.hand:
                if len(already_on_flag) == 2:
                    my_combos = list(itertools.combinations([tuple(card_in_hand)],1))
                for combo in my_combos:
                    #cards_already_owned = 0
                    if len(already_on_flag) < 2:
                        tempList = [tuple(card_in_hand)]
                        for temp_card in combo:
                            tempList.append(temp_card)
                        combo = tuple(tempList)

                    #probability_to_get_combo = 0
                    
                    '''for combo_card in combo:
                        for hand_card in state.hand:
                            if combo_card == hand_card:
                                cards_already_owned += 1'''

                    for on_flag_card in already_on_flag:
                        combo = list(combo)
                        combo.append(on_flag_card)
                        combo = tuple(combo)
                        #cards_already_owned += 1
                    old_combo = combo
                    combo = self.sort_cards(combo)

                    '''if cards_already_owned == 3:
                        probability_to_get_combo = 1
                    elif cards_already_owned == 2:
                        probability_to_get_combo = 1.0 * 1.0 * (1.0/len(state.deck))
                    elif cards_already_owned == 1:
                        probability_to_get_combo = 1.0 * (1.0/len(state.deck)) * (1.0/(len(state.deck)-1))'''

                    win_prob = self.seeded_json["valid_formations"][str(combo)]["win_chance"]
                    #* probability_to_get_combo

                    if win_prob > opponent_win_prob:
                        return flag,old_combo[0]

                    if win_prob > max_win_prob:
                        flag_to_play = flag
                        max_win_prob = win_prob
                        card_to_play = old_combo[0]
        return flag_to_play,card_to_play

    def sort_cards(self,three_cards):
        index = 1
        while index < 3:
            if three_cards[index][0] < three_cards[index-1][0]:
                three_cards = list(three_cards)
                temp_card = three_cards[index]
                three_cards[index] = three_cards[index-1]
                three_cards[index-1] = temp_card
                three_cards = tuple(three_cards)
                index = 0
            if three_cards[index][0] == three_cards[index-1][0]:
                if three_cards[index][1] < three_cards[index-1][1]:
                    three_cards = list(three_cards)
                    temp_card = three_cards[index]
                    three_cards[index] = three_cards[index-1]
                    three_cards[index-1] = temp_card
                    three_cards = tuple(three_cards)
                    index = 0
            index += 1
        return three_cards


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