"""
Hangman
Creator: Kian Moloney

This game is hangman. The game was created using a class. Your job is to guess
what the shown country is by pressing interactive buttons that are shown on
screen. If you guess incorrectly a total of 7 times, the game ends. There are
a total of 41 countries that you have to guess from. Use either the drop-down
menu or the x-button to exit the game.
"""

from tkinter import *
from tkinter import messagebox
from functools import partial
from string import ascii_uppercase
import random

WORDLIST = ["FINLAND", "SWEDEN", "NORWAY", "DENMARK", "CHINA", "JAPAN",
            "INDIA", "TURKEY", "GERMANY", "RUSSIA", "POLAND", "SPAIN",
            "FRANCE", "PORTUGAL", "EGYPT", "ARGENTINA", "AMERICA", "CANADA",
            "GREECE", "ITALY", "SERBIA", "ESTONIA", "MEXICO", "UKRAINE",
            "HUNGARY", "ICELAND", "LUXEMBOURG", "MADAGASCAR", "INDONESIA",
            "AUSTRALIA", "ISRAEL", "CHILE", "IRELAND", "CROATIA", "ALBANIA",
            "NIGERIA", "MAROCCO", "SOMALIA", "BELGIUM", "LATVIA", "MALAYSIA"]


class Hangman:
    def __init__(self):
        """
        Constructor that creates all the parts of the GUI and all the
        attributes for the functions, the use of which are explained later.
        """

        # Create the menu.
        self.__window = Tk()
        self.__window.title("Hangman - Guess the Country")

        # Import the photos now that there is a main window.
        self.__photos = [
                        PhotoImage(file="0.png"), PhotoImage(file="1.png"),
                        PhotoImage(file="2.png"), PhotoImage(file="3.png"),
                        PhotoImage(file="4.png"), PhotoImage(file="5.png"),
                        PhotoImage(file="6.png"), PhotoImage(file="7.png")
                        ]

        self.__wrong_guesses = 0

        # Create a top menu and cascade a submenu to it containing two buttons.
        top_menu = Menu(self.__window)
        self.__window.configure(menu=top_menu)
        sub_menu = Menu(top_menu, tearoff=False)
        top_menu.add_cascade(menu=sub_menu, label="Menu")
        sub_menu.add_command(label="New game", command=self.new_game)
        sub_menu.add_command(label="Quit", command=self.quit_program)

        # Create a Label for the hangman photos and set the default photo.
        self.__hangman_label = Label(self.__window)
        self.__hangman_label.grid(row=0, column=12, columnspan=6, rowspan=7,
                                  sticky=E, padx=(0, 5))
        self.__hangman_label.configure(image=self.__photos[0])

        # Create a Label for the word to be guessed.
        self.__word_label = Label(self.__window)
        self.__word_label.grid(row=12, column=8, columnspan=3, sticky=E+W,
                               padx=(10, 0))

        # An attribute to help to check if the user won. It is called spaced
        # word, because the selected country is presented to the user with
        # spaces between the letters.
        self.__spaced_word = ""

        # Make a list where the keyboard buttons can be placed.
        self.__buttons = []

        i = 0

        # To create the buttons, we first have to go through the letters,
        # so 'range(26)' for the amount of letters.
        for index in range(26):
            # Pick out a letter and make a button for it. The partial is used
            # to make sure an argument can be passed to the guess handler.
            letter = ascii_uppercase[index]
            self.__buttons.append(Button(self.__window, text=letter, font=
                                         "Euphemia 10",
                                         command=partial(self.guess, letter,
                                                         index)))

            # Place the letters using the i variable.
            self.__buttons[index].grid(row=1+i//5, column=i % 5, sticky=E+W)
            i += 1

        # Create a 'new game' button beside the Z button.
        self.__new_game = Button(self.__window, text="New Game",
                                 font="Euphemia", command=self.new_game).grid(
                                                          row=6, column=2,
                                                          columnspan=4,
                                                          sticky=W)

        self.new_game()

        # Greet the user and tell them how to play.
        self.__welcome_message = messagebox.showinfo("Hangman",
                                                     "Welcome to Hangman!\n"
                                                     "Your job is to guess "
                                                     "the country.\nYou can "
                                                     "answer incorrectly 7 "
                                                     "times so make it count!")
        self.__window.mainloop()

    def new_game(self):
        """
        Start a new game, so in other words reset the buttons, get a new word,
        replace the old with the new one (unless it's the first game),
        and reset the wrong guesses.
        """

        # Reset the amount of wrong guesses.
        self.__wrong_guesses = 0

        # Reset the image and buttons.
        self.__hangman_label.configure(image=self.__photos[0])
        for index in range(25):
            self.__buttons[index].configure(state=NORMAL)

        # Select a word out of the 41 countries.
        random_index = random.randint(0, 40)
        selected_word = WORDLIST[random_index]

        # Create spaces between the letters of the word and replace the letters
        # with underscores.
        self.__word_label.configure(text=" ".join("_" * len(selected_word)),
                                    font="Euphemia 14")

        # Configure the spaced word for the guess method, so that it can make
        # it into a list, and use it to check if the user won.
        self.__spaced_word = " ".join(selected_word)

    def quit_program(self):
        """
        Simple exit function, incase the user wants to exit using the 'Quit'
        button.
        """

        # Show a messagebox and destroy the window.
        messagebox.showinfo("Hangman - Guess the Country",
                            "Thanks for playing!")
        self.__window.destroy()

    def guess(self, letter, index):
        """
        When a button is pressed, this method is called. This methods job
        consists of disabling the button, and if guessed correctly, checking
        if won and replacing underscores with letters. Also it changes the
        picture of Hangman accordingly.

        :param letter: str, the letter of the button that was pressed.
        :param index: int, the index of the abovesaid button in the list,
        where the buttons exist.
        """

        # Since the button was pressed, disable it.
        self.__buttons[index].configure(state=DISABLED)

        # Get the already guessed letters and make a list out of them.
        guessed_letters = list(self.__word_label.cget("text"))

        # Also make a list of the letters of the country, so that we can
        # check the count.
        letters_of_the_country = list(self.__spaced_word)

        # If a letter is found, go through the letters of the country and
        # check how many there are.
        if self.__spaced_word.count(letter) > 0:
            for i in range(len(letters_of_the_country)):
                if letters_of_the_country[i] == letter:

                    # Add the correctly guessed letters to the list,
                    # and make tem appear.
                    guessed_letters[i] = letter

                self.__word_label.configure(text="".join(guessed_letters),
                                            font="Euphemia 14")

            # Check if won:
            if self.__word_label.cget("text") == self.__spaced_word:
                # Call a new game and pop up a messagebox.
                messagebox.showinfo("Hangman",
                                    "YOU WON!")
                self.new_game()
        else:
            self.__wrong_guesses += 1

            # Change the hangman picture according to the amount of guesses.
            self.__hangman_label.configure(image=
                                           self.__photos[self.__wrong_guesses])

            # If the user guessed 7 times already, it's game over.
            if self.__wrong_guesses == 7:
                messagebox.showwarning("Hangman",
                                       "Game Over")

                self.new_game()


def main():
    Hangman()


if __name__ == '__main__':
    main()
    
