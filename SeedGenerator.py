import itertools
from Formation import Formation
import json

numbers = [1,2,3,4,5,6,7,8,9,10]
suites = ["color1","color2","color3","color4","color5","color6"]
deck = list(itertools.product(numbers,suites))
my_side_permutations = list(itertools.permutations(deck,3))
other_side_combinations = list(itertools.combinations(deck,3))
times_through_outer_loop = 0
list_of_json_strings = list()
for index_my_side,three_card_list_my_side in enumerate(my_side_permutations):
    this_formation_dict = { "formation" : three_card_list_my_side,
                                "times_won" : 0,
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
        this_formation_json = json.dumps(this_formation_dict)
    list_of_json_strings.append(this_formation_json)
    times_through_outer_loop += 1
    if times_through_outer_loop % 100 == 0:
        print (times_through_outer_loop)
with open('seed.txt','w') as outfile:
    for json_string in list_of_json_strings:
        json.dump(json_string, outfile)
