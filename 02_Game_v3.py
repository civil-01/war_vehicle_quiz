import csv
import random
from tkinter import *
from functools import partial # to prevent unwanted windows
from PIL import ImageTk, Image


def get_vehicles():
    # retrieve vehicles from csv anf put them in a list
    file = open("war_vehicles/war_vehicles_v2.csv", "r")
    all_vehicles = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_vehicles.pop(0)

    return all_vehicles

def get_round_vehicles():

    all_vehicles = get_vehicles()
    round_vehicles = []

    # Loop until we have four vehicles with different scores,
    while len(round_vehicles) < 4:
        potential_vehicles = random.choice(all_vehicles)

        # Get the score and check it's not a duplicate
        if potential_vehicles not in round_vehicles:
            round_vehicles.append(potential_vehicles)

    return round_vehicles

def round_ans(val):
    """
    Rounds numbers to nearest integer
    :param val: number to be rounded.
    :return: Rounded number (an integer)
    """
    var_rounded = (val * 2 + 2) // 2
    raw_unrounded = "{:.0f}".format(var_rounded)
    return int(raw_unrounded)





class StartGame:
    """
    Initial Game interface (Asks users how many round they would like to play)
    """

    def __init__(self):
        """
        Gets number of round from user
        """
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # string for labels
        intro_string = ("In each round you will be given a vehicle name, then given a selection of four images,"
                        " which you then need to click on the image that matches the name. Your goal is"
                        "to beat the target score and win the round (and keep your points). ")

        choose_string = "How many rounds do you want to play"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["War Vehicle Quiz", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"]
        ]

        # create labels and add them to the reference list...

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2],
                               wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # extract choice label so that it can be changed to an
        # error message if necessary.
        self.choose_label = start_label_ref[2]

        # frame so that entry box and button can be in the same row.
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#4B5320", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        # Retrieve rounds to be converted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come to home)
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - please choose a whole number more than zero"
        has_errors = "no"

        # checks that amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # invoke play class (and take across number of rounds)
                game(rounds_wanted)
                # hide root window (ie hide rounds choice window)
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


class game:
    """
    Interface for planing the War vehicle Quiz
    """


    def __init__(self, how_many):


        self.correct_answer = StringVar()

        # rounds played - start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.rounds_won = IntVar()

        self.round_vehicle_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box, bg="#dad7cd")
        self.game_frame.grid(padx=10, pady=10)



        # body font for most labels
        body_font = ("Arial", "12")

        # list for label details (text | font | background | row)
        play_labels_list = [
            ["War Vehicles Quiz", ("Arial", "16", "bold"), "#dad7cd", 0],
            ["Vehicle name goes here", body_font, "#D5E8D4", 2],
            ["choose an image and then press next", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)

        # set score and rounds frame
        self.score_rounds_frame = Frame(self.game_frame, bg="#dad7cd")
        self.score_rounds_frame.grid(row=1)

        # list and label for rounds and score
        # (text | font | background | row | column)
        score_round_labels_list = [
            ["Score: #", body_font, "#a3b18a", 1, 1],
            ["Round # of #", body_font, "#a3b18a", 1, 0]
        ]
        score_round_labels_ref = []
        for item in score_round_labels_list:
            self.make_label = Label(self.score_rounds_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], column=item[4], padx=5, pady=5)

            score_round_labels_ref.append(self.make_label)

        # retrieve labels so they can be configured later
        self.heading_label = play_labels_ref[1]
        self.target_score = score_round_labels_ref[0]
        self.target_round = score_round_labels_ref[1]
        self.results_label = play_labels_ref[2]


        # set up vehicle buttons
        self.vehicle_frame = Frame(self.game_frame, bg="#dad7cd")
        self.vehicle_frame.grid(row=3)

        self.vehicle_button_ref = []
        self.vehicle_button_list = []

        # create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.vehicle_button = Button(self.vehicle_frame, font=("arial", 12),
                                         text="test image",
                                         command=partial(self.round_results, item))
            self.vehicle_button.grid(row=item // 2,
                                     column=item % 2,
                                     padx=5, pady=5)
            self.vehicle_button_ref.append(self.vehicle_button)

        # frame to hold help and stats buttons
        self.help_next_stats_frame = Frame(self.game_frame, bg="#dad7cd")
        self.help_next_stats_frame.grid(row=6)

        # list for buttons (frame | text | bg | command | width | row | column)
        control_button_list = [
            [self.help_next_stats_frame, "Help", "#588157", "", 5, 0, 0],
            [self.help_next_stats_frame, "Next Round", "#4B5320", self.new_round, 10, 0, 1],
            [self.help_next_stats_frame, "Stats", "#344e41", "", 5, 0, 2],
            [self.game_frame, "End", "#990000", self.close_play, 23, 7, None],
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", 16, "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=3, pady=5)

            control_ref_list.append(make_control_button)

        self.next_button = control_ref_list[1]
        self.end_game_button = control_ref_list[3]

        self.new_round()

    def new_round(self):


        """
        Chooses four vehicle images, configures
        buttons with chosen vehicles
        """


        # retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()



        #  get round vehicles
        self.round_vehicle_list = get_round_vehicles()

        # update heading, "hide" results label
        self.target_round.config(text=f"Round {rounds_played + 1} of {rounds_wanted}")
        # self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")
        # sets the correct answer
        print("round vehicle list", self.round_vehicle_list)

        self.correct_answer.set(self.round_vehicle_list[2][0])

        random.shuffle(self.round_vehicle_list)


        correct_answer = self.correct_answer.get()
        print("correct answer:", correct_answer)

        print("test", self.correct_answer)

        print("heading label", self.heading_label)

        self.heading_label.config(text=f"Choose the image that is a\n{correct_answer}", justify='center')






        # file Path
        file_paths = []

        for count, item in enumerate(self.vehicle_button_ref):
            file = self.round_vehicle_list[count][1]
            filepath = f"war_vehicles/{file}.jpg"
            file_paths.append(filepath)
            item.config(text=filepath)

            # print("round vehicles", self.round_vehicle_list)
            # print("File Paths: ", file_paths)

            image = Image.open(filepath).resize((200, 144))

            img = ImageTk.PhotoImage(image)

            item.config(image=img, state=NORMAL)
            # garbage collection
            item.image=img


        self.next_button.config(state=DISABLED)


    def round_results(self, user_choice):

        """
        Retrieves which button was pushed (index 0 - 3), retrieves
        score and updates results and adds results to stats list.
        """

        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        # get user answer and vehicle based on buttons press...
        answer = (self.round_vehicle_list[user_choice][0])



        # alternate way to get button name. good for if buttons have been scrambled
        vehicle_name = self.vehicle_button_ref[user_choice].cget('text')

        print("vehicle name", vehicle_name)

        print(answer)

        # retrieve the correct answer
        correct_answer = self.correct_answer.get()



        # print statements based on if the answer is correct
        if answer == correct_answer:
            self.results_label.config(text="Congrats you got it correct!")

            rounds_won = self.rounds_won.get()
            rounds_won += 1
            self.rounds_won.set(rounds_won)
            self.target_score.config(text=f"score: {rounds_won}")

        else:
            self.results_label.config(text=f"Wrong! you chose {answer}")


        # enable next round button
        self.next_button.config(state=NORMAL)

        # check to see if game is over
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:


            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.vehicle_button_ref:
            item.config(state=DISABLED)




    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("War Vehicle Quiz")
    StartGame()
    root.mainloop()
