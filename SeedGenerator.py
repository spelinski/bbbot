import itertools
from Formation import Formation
import json

def sort_cards(three_cards):
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

numbers = [1,2,3,4,5,6,7,8,9,10]
suites = ["color1","color2","color3","color4","color5","color6"]
deck = list(itertools.product(numbers,suites))
my_side_combinations = list(itertools.combinations(deck,3))
other_side_combinations = list(itertools.combinations(deck,3))
times_through_outer_loop = 0
overall_dict = { "valid_formations": {}}
for three_card_list_my_side in my_side_combinations:
    three_card_list_my_side = sort_cards(three_card_list_my_side)
    this_formation_dict = { "times_won" : 0,
                            "times_lost" : 0,
                            "win_chance" : 0}
    my_side_formation = Formation(three_card_list_my_side)
    for three_card_list_other_side in other_side_combinations:
        other_side_formation = Formation(three_card_list_other_side)
        if my_side_formation.is_greater_strength_than(other_side_formation):
            this_formation_dict["times_won"] += 1
            this_formation_dict["win_chance"] = float(this_formation_dict["times_won"]) / float(this_formation_dict["times_won"]+this_formation_dict["times_lost"])
        elif other_side_formation.is_greater_strength_than(my_side_formation):
            this_formation_dict["times_lost"] += 1
            this_formation_dict["win_chance"] = float(this_formation_dict["times_won"]) / float(this_formation_dict["times_won"]+this_formation_dict["times_lost"])
    overall_dict["valid_formations"][str(three_card_list_my_side)] = this_formation_dict
    times_through_outer_loop += 1
    if times_through_outer_loop % 100 == 0:
        print (times_through_outer_loop)
with open('seed.txt','w') as outfile:
    json.dump(overall_dict, outfile)
