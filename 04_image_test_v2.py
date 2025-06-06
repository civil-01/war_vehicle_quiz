from tkinter import *
from PIL import ImageTk, Image

import csv
import random
from tkinter.constants import NORMAL


root = Tk()

def round_ans(val):
    """
    Rounds numbers to nearest integer
    :param val: number to be rounded.
    :return: Rounded number (an integer)
    """
    var_rounded = (val * 2 + 2) // 2
    raw_unrounded = "{:.0f}".format(var_rounded)
    return int(raw_unrounded)

# Retrieve vehicles from csv and put them in a list,
file = open("war_vehicles/war_vehicles_v2.csv", "r")
all_vehicles = list(csv.reader(file, delimiter=","))
file.close()

# Remove the first row,
all_vehicles.pop(0)

round_vehicles = []
vehicles_scores = []

# Loop until we have four vehicles with different scores,
while len(round_vehicles) < 4:
    potential_vehicles = random.choice(all_vehicles)

    # Get the score and check it's not a duplicate
    if potential_vehicles not in vehicles_scores:
        round_vehicles.append(potential_vehicles)

print("Round Vehicles: ", round_vehicles)

# file Path
file_paths = []

# Get image file names from list
for count, item in enumerate(round_vehicles):
    file = round_vehicles[count][1]
    filepath = f"war_vehicles/{file}.jpg"
    file_paths.append(filepath)

print("File Paths: ", file_paths)

image1 = Image.open(file_paths[0]).resize((200, 144))
image2 = Image.open(file_paths[1]).resize((200, 144))
image3 = Image.open(file_paths[2]).resize((200, 144))
image4 = Image.open(file_paths[3]).resize((200, 144))
img1 = ImageTk.PhotoImage(image1)
img2 = ImageTk.PhotoImage(image2)
img3 = ImageTk.PhotoImage(image3)
img4 = ImageTk.PhotoImage(image4)


image1 = Button(root)
image1.grid(row=0, column=0)

image2 = Button(root)
image2.grid(row=0, column=1)

image3 = Button(root)
image3.grid(row=1, column=0)

image4 = Button(root)
image4.grid(row=1, column=1)

image1.config(image=img1)
image2.config(image=img2)
image3.config(image=img3)
image4.config(image=img4)

mainloop()
