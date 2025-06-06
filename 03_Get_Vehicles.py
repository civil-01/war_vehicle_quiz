import csv
import random
from tkinter.constants import NORMAL


def round_ans(val):
    """
    Rounds numbers to nearest integer
    :param val: number to be rounded.
    :return: Rounded number (an integer)
    """
    var_rounded = (val * 2 + 2) // 2
    raw_unrounded = "{:.0f}".format(var_rounded)
    return int(raw_unrounded)
# retrieve vehicles from csv anf put them in a list
file = open("war_vehicles/war_vehicles_v2.csv", "r")
all_vehicles = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row
all_vehicles.pop(0)



round_vehicles = []
vehicles_scores = []


# loop until we have four vehicles with different scores
while len(round_vehicles) < 4:
    potential_vehicles = random.choice(all_vehicles)

    # get the score and check it's not a duplicate
    if potential_vehicles[1] not in vehicles_scores:
        round_vehicles.append(potential_vehicles)

print("round vehicles", round_vehicles)






