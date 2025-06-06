# importing only those functions
# which are needed
from tkinter import *
from PIL import ImageTk, Image
from tkinter.ttk import *


# creating tkinter window
root = Tk()

# Creating a photoimage object to use image
img = ImageTk.PhotoImage(file = "C:/users/matichj1179/OneDrive - Massey High School/2025/comue/war_vehicle_quiz/war_vehicles/a7v.jpg")

Button = Button(image=img)
Button.grid(padx=5, pady=5)

mainloop()