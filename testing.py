import csv
import random
from tkinter import *
from functools import partial  # to prevent unwanted windows


def __init__(self, how_many):
    # integers / string variables
    self.target_score = IntVar()

    # rounds played - start with zero
    self.rounds_played = IntVar()
    self.rounds_played.set(0)

    self.rounds_wanted = IntVar()
    self.rounds_wanted.set(how_many)

    self.rounds_won = IntVar()

    # colour list lists and score list
    self.round_colour_list = []
    self.all_scores_list = []
    self.all_high_score_list = []

    self.play_box = Toplevel()

    self.game_frame = Frame(self.play_box)
    self.game_frame.grid(padx=10, pady=10)

    # body font for most labels
    body_font = ("Arial", "12")

    # list for label details (text | font | background | row)
    play_labels_list = [
        ["Round # of #", ("Arial", "16", "bold"), None, 0],
        ["Score to beat: #", body_font, "#FFF2CC", 1],
        ["Choose a colour below. Good luck 🍀", body_font, "#D5E8D4", 2],
        ["You chose, result", body_font, "#D5E8D4", 4]
    ]

    play_labels_ref = []
    for item in play_labels_list:
        self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                bg=item[2], wraplength=300, justify="left")
        self.make_label.grid(row=item[3], pady=10, padx=10)

        play_labels_ref.append(self.make_label)

    # retrieve labels so they can be configured later
    self.heading_label = play_labels_ref[0]
    self.target_label = play_labels_ref[1]
    self.choose_label = play_labels_ref[2]
    self.results_label = play_labels_ref[3]

    # set up colour buttons
    self.colour_frame = Frame(self.game_frame)
    self.colour_frame.grid(row=3)

    self.colour_button_ref = []
    self.colour_button_list = []

    # create four buttons in a 2 x 2 grid
    for item in range(0, 4):
        self.colour_button = Button(self.colour_frame, font=("arial", 12),
                                    text="colour Name", width=15,
                                    command=partial(self.round_results, item))
        self.colour_button.grid(row=item // 2,
                                column=item % 2,
                                padx=5, pady=5)

        self.colour_button_ref.append(self.colour_button)

    # frame to hold hints and stats buttons
    self.hints_stats_frame = Frame(self.game_frame)
    self.hints_stats_frame.grid(row=6)

    # list for buttons (frame | text | bg | command | width | row | column)
    control_button_list = [
        [self.game_frame, "Next Round", "#0057D8", self.new_round, 21, 5, None],
        [self.hints_stats_frame, "Hints", "#FF8000", self.to_hints, 10, 0, 0],
        [self.hints_stats_frame, "Stats", "#333333", self.to_stats, 10, 0, 1],
        [self.game_frame, "End", "#990000", self.close_play, 21, 7, None],
    ]

    # create buttons and add to list
    control_ref_list = []
    for item in control_button_list:
        make_control_button = Button(item[0], text=item[1], bg=item[2],
                                     command=item[3], font=("Arial", 16, "bold"),
                                     fg="#FFFFFF", width=item[4])
        make_control_button.grid(row=item[5], column=item[6], padx=3, pady=5)

        control_ref_list.append(make_control_button)

    # retrieve next, stats and end button so that they can be configured
    self.next_button = control_ref_list[0]
    self.hints_button = control_ref_list[1]
    self.stats_button = control_ref_list[2]
    self.end_game_button = control_ref_list[3]

    self.stats_button.config(state=DISABLED)

    # Once interface has been created, invoke new
    # round function for first round
    self.new_round()


def round_results(self, user_choice):
        """
        Retrieves which butoon was pushed (index 0 - 3), retrieves
        score and the compares it with median, updates reults
        and adds results to stats list.
        """

        # enable stast button after atleast one round has been played
        self.stats_button.config(state=NORMAL)

        # get user score and colour based on buttons press..
        score = int(self.round_colour_list[user_choice][1])

        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_won = self.rounds_won.get()

        # alternate way to get button name. good for if buttons have been scrambled
        colour_name = self.colour_button_ref[user_choice].cget('text')

        # retrieve target score and compare with user score to find round result
        target = self.target_score.get()

        if score >= target:
            result_text = f"Success! {colour_name} earned you {score} points"
            result_bg = "#82B366"
            self.all_scores_list.append(score)

            rounds_won = self.rounds_won.get()
            rounds_won += 1
            self.rounds_won.set(rounds_won)

        else:
            result_text = f"Oops {colour_name} ({score}) is less than the target."
            result_bg = "#F8CECC"
            self.all_scores_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # printing area to generate test data for stats (delete when done)
        print("all scores", self.all_scores_list)
        print("highest scores:", self.all_high_score_list)

        # enable stats and next buttons, disable colour buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # check to see if game is over
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            # work out success rate
            success_rate = rounds_won / rounds_played * 100
            success_string = (f"Success Rate: "
                              f"{rounds_won} / {rounds_played} "
                              f"({success_rate:.0f}%)")

            self.heading_label.config(text="Game Over")
            self.target_label.config(text=success_string)
            self.choose_label.config(text="Please click the stats "
                                          "button for more info")
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.colour_button_ref:
            item.config(state=DISABLED)
