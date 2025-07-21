import csv
import random
from tkinter import *
from functools import partial



class StartGame:
    """
    Initial Game interface (Asks users how many round they would like to play)
    """

    def __init__(self,):
        """
        Gets number of round from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # create play button
        self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)



    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        # Retrive rounds to be converted
        rounds_wanted = 5
        self.to_play(rounds_wanted)

    def to_play(self, num_rounds):
        """
        Invokes Game GUI and take accross numebr of rounds to be played
        """
        Play(num_rounds)
        # Hide root window (ie: hide rounds choice window) 
        root.withdraw()

class Play:
    """
    Interface for playing the colour quest game
    """
    def __init__(self, how_many):
        self.rounds_won = IntVar()

        # random score test data
        self.all_scores_list = [19, 0, 20, 20, 16]
        self.all_high_score_list = [20, 16, 20, 20, 20]
        self.rounds_won.set(4)


        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Colour Quest", font=("Airal", "16", 'bold'),
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.stats_button =Button(self.game_frame, font=("arial", "14", "bold"),
                                  text="Stats", width=15, fg="#FFFFFF",
                                  bg="#FF8000", padx=10, pady=10, command=self.to_stats)
        self.stats_button.grid(row=1)

    def to_stats(self):
        """
        Retrieves everthing we need to display the game / round statistics
        """

        #  IMPORTANT: retrieve number of rounds
        # won as number (rather than self container)
        rounds_won = self.rounds_won.get()
        stats_bundle = [rounds_won]

        Stats(self, stats_bundle)

class Stats:

    def __init__(self, partner, all_stats_info):
        
        # Extract information from master list 
        rounds_won = all_stats_info[1]
        user_scores = all_stats_info[1]
        high_scores = all_stats_info[2]

        # sorts user scores to find high score..
        user_scores.sort()
        
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

        # math to populate stats dialouge
        rounds_played = len(user_scores)

        success_rate = rounds_won / rounds_played * 100
        total_score = sum(user_scores)
        max_possible = sum(high_scores)

        best_score = user_scores[-1]
        average_score = total_score / rounds_played

        # strings for stats labels..

        success_string = (f"Sucess Rate: {rounds_won} / {rounds_played}"
                          f" ({success_rate:.0f}%)")
        total_score_string = f"Total Score: {total_score}"
        max_possible_string = f"Maximum possible score: {max_possible}"
        best_score_string = f"Best Score: {best_score}"

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
            comment_string = "#F0F0F0"


        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("Arial", "13")

        # label list (text | font | 'Sticky')
        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [success_string, normal_font, "W"],
            [total_score_string, normal_font, "W"],
            [max_possible_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
            ["\nRound Stats", heading_font, ""],
            [best_score_string, normal_font, "W"],
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
        stats_comment_label.config(bg=comment_colour)
         
        
        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)



    def close_stats(self, partner):
        """
        Closes stats dialogue box (and enable stats button)
        """
        # put stats button back to normal
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()



# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()


  