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
            ["War Vehicle Quiz", ("Courier New", "16", "bold"), None],
            [intro_string, ("Courier New", "12"), None],
            [choose_string, ("Courier New", "12", "bold"), "#009900"]
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

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Courier New", 20, "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # create play button
        self.play_button = Button(self.entry_area_frame, font=("Courier New", 16, "bold"),
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
        self.choose_label.config(fg="#009900", font=("Courier New", "12", "bold"))
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
                                     font=("Courier New", "10", "bold"))
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
        body_font = ("Courier New", "12")

        # list for label details (text | font | background | row)
        play_labels_list = [
            ["War Vehicles Quiz", ("Courier New", "16", "bold"), "#dad7cd", 0],
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
            ["Score: 0", body_font, "#a3b18a", 1, 1],
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
            self.vehicle_button = Button(self.vehicle_frame, font=("Courier New", 12),
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
            [self.help_next_stats_frame, "Help", "#588157", self.to_help, 5, 0, 0],
            [self.help_next_stats_frame, "Next Round", "#4B5320", self.new_round, 10, 0, 1],
            [self.help_next_stats_frame, "Stats", "#344e41", self.to_stats, 5, 0, 2],
            [self.game_frame, "End", "#990000", self.close_play, 23, 7, None],
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Courier New", 16, "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=3, pady=5)

            control_ref_list.append(make_control_button)

        self.help_button = control_ref_list[0]
        self.next_button = control_ref_list[1]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        self.stats_button.config(state=DISABLED)

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
        self.correct_answer.set(self.round_vehicle_list[2][0])

        random.shuffle(self.round_vehicle_list)

        correct_answer = self.correct_answer.get()


        self.heading_label.config(text=f"Choose the image that is a\n{correct_answer}", justify='center')

        self.results_label.config(bg="#D5E8D4", text="Choose an image and then press next." )


        # file Path
        file_paths = []

        for count, item in enumerate(self.vehicle_button_ref):
            file = self.round_vehicle_list[count][1]
            filepath = f"war_vehicles/{file}.jpg"
            file_paths.append(filepath)
            item.config(text=filepath)

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

        self.stats_button.config(state=NORMAL)

        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        # get user answer and vehicle based on buttons press...
        answer = (self.round_vehicle_list[user_choice][0])


        # retrieve the correct answer
        correct_answer = self.correct_answer.get()

        # print statements based on if the answer is correct
        if answer == correct_answer:
            self.results_label.config(bg="#D5E8D4",text="Congrats you got it correct!")

            rounds_won = self.rounds_won.get()
            rounds_won += 1
            self.rounds_won.set(rounds_won)
            self.target_score.config(text=f"score: {rounds_won} out of {rounds_played}")

        else:
            self.results_label.config(bg="#FF6767", text=f"Wrong! you chose {answer}")
            rounds_won = self.rounds_won.get()
            self.target_score.config(text=f"score: {rounds_won} out of {rounds_played}")


        # enable next round button
        self.next_button.config(state=NORMAL)

        # check to see if game is over
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.vehicle_button_ref:
            item.config(state=DISABLED)

    def to_help(self):
        """
        Displays help for playing game
        :return:
        """
        Displayhelp(self)


    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_stats(self):
        """
        Retrieves everything we need to display the game / round statistics
        """


         #  IMPORTANT: retrieve number of rounds
         # won as number (rather than self container)
        rounds_won = self.rounds_won.get()
        rounds_played = self.rounds_played.get()

        stats_bundle = [rounds_won, rounds_played]

        Stats(self, stats_bundle)





class Stats:

    def __init__(self, partner, all_stats_info):


        # Extract information from master list
        rounds_won = all_stats_info[0]
        user_scores = all_stats_info[0]
        high_scores = all_stats_info[0]
        rounds_played = all_stats_info[1]


        # setup dialogue box amd background colour

        self.stats_box = Toplevel()

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        # if users press cross at the top, closes stats
        #  and releases stats box
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300,
                                 height=200)
        self.stats_frame.grid()

        # math to populate stats dialog

        success_rate = rounds_won / rounds_played * 100
        total_score = user_scores
        max_possible = rounds_played



        # strings for stats labels..

        success_string = (f"Success Rate: {rounds_won} / {rounds_played}"
                          f" ({success_rate:.0f}%)")
        total_score_string = f"Total Score: {total_score}"
        max_possible_string = f"Maximum possible score: {max_possible}"


        # custom comment text and formatting
        if total_score == max_possible:
            comment_string = ("Amazing! You got the highest "
                              "possible score!")
            comment_colour = "#D5E8D4"

        elif total_score == 0:
            comment_string = ("Oops - Youve lost every round! "
                              "you might want to look at the hints!")
            comment_colour = "#F8CECC"
        else:
            comment_colour = "#F0F0F0"
            comment_string = ""

        heading_font = ("Courier New", "16", "bold")
        normal_font = ("Courier New", "14")
        comment_font = ("Courier New", "13")

        # label list (text | font | 'Sticky')
        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [success_string, normal_font, "W"],
            [total_score_string, normal_font, "W"],
            [max_possible_string, normal_font, "W"],
            [comment_string, comment_font, "W"]
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left",
                                     padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        # configure comment label background (for all won / all lost)
        stats_comment_label = stats_label_ref_list[4]
        stats_comment_label.config(bg="#FFFFFF")

        self.dismiss_button = Button(self.stats_frame,
                                     font=("Courier New", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=5, padx=10, pady=10)

    def close_stats(self, partner):
        """
        Closes stats dialogue box (and enable stats button)
        """
        # put stats button back to normal
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()







class Displayhelp:

    def __init__(self, partner):
        # setup dialogue box amd background colour
        background = "#dad7cd"
        self.help_box = Toplevel()
        self.help_box.resizable(False, False)

        # disable help button
        partner.help_button.config(state=DISABLED)

        # if users press cross at the top, closes help
        #  and releases help box
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        text="Help",
                                        font=("Courier New", "14", "bold"))
        self.help_heading_label.grid(row=0)

        self.help_text_label = Label(self.help_frame,
                                     text="So basically at the top of the screen its gonna have what round you're on and your score."
                                          " Below that it's gonna tell you the name of what vehicle you need to choose."
                                          " Now underneath that is the fun part, the images, you find the image of the vehicle you were asked for and click on it."
                                          " you will then be told if you got it right or wrong. If you did well and got it correct then your score will increase by 1."
                                          " Now after everytime you click an image you will need to then click the next round button which is below the images."
                                          " When you have played all your rounds, you can click stats and flex on your friends about your highscore.", wraplength=350,
                                     font=("Courier New", "11", "bold"), justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Courier New", "12", "bold"),
                                     text="Close", bg="#588157",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # list and loop to set the background colour on
        # everything except buttons
        recolour_list = [self.help_frame, self.help_heading_label,
                         self.help_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_help(self, partner):
        """
        Closes help dialogue box (and enable help button)
        """
        # put help button back to normal
        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()




# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("War Vehicle Quiz")
    StartGame()
    root.mainloop()
