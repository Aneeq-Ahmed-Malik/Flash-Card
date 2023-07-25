from tkinter import *
import pandas
from random import choice

word = {}

# ---------------------------------- Giving Unknown Words ----------------------------------------#
try:
    open("./data/words_to_learn.csv")

except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv")
    data_list = data.to_dict("records")

else:
    data = pandas.read_csv("./data/words_to_learn.csv")
    data_list = data.to_dict("records")

# ---------------------------------- Next Card Generator ----------------------------------------#

def next_card():
    global timer, word

    word = choice(data_list)

    window.after_cancel(timer)

    canvas.itemconfig(card_img, image=front_card_img)
    canvas.itemconfig(to_guess, text=word["French"], fill="black")
    canvas.itemconfig(title, text="French", fill="black")

    timer = window.after(3000, flip_card, word)

# ---------------------------------- Removing Known Words ----------------------------------------#


def correct_guess():
    global word, data_list

    data_list.remove(word)
    seen_data = pandas.DataFrame(data_list)
    seen_data.to_csv("./data/words_to_learn.csv", index=False)

    next_card()
# ---------------------------------- Flipping Cards ----------------------------------------#


def flip_card(word):

    canvas.itemconfig(card_img, image=back_card_img)
    canvas.itemconfig(to_guess, fill="white", text=word["English"])
    canvas.itemconfig(title, fill="white", text="English")
    window.after_cancel(timer)

# ---------------------------------- UI ----------------------------------------#
BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

back_card_img = PhotoImage(file="./images/card_back.png")
front_card_img = PhotoImage(file="./images/card_front.png")
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_img = canvas.create_image(400, 263, image=front_card_img)

title = canvas.create_text(400, 150, font=("Arial", 40, "italic"))
to_guess = canvas.create_text(400, 263, font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=correct_guess)
right_button.grid(column=1, row=1)

timer = window.after(3000, flip_card)
next_card()

window.mainloop()
