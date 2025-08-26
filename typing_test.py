import time
import random
import curses   # module for this purpose of coding
from curses import wrapper   # and this is gonna wrap all our code and run it in the context of curses module

# to run this code, we need to run it from the cmd by running in the directory python thenameoftheprogram.py

# Before that, you have to install the module curses with the command in cmd: pip install windows-curses

def start_screen(stdscr):  #starting screen function
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing test !")
    stdscr.addstr("\nPress any key to begin ")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):  #function to cover the display of the current text on the target, and change the color as well
    stdscr.addstr(target)

    stdscr.addstr(1, 0, f"WPM: {wpm}")


    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != target[i]:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)  # 0,i means start normally and go one step forward in

        #order to put the character typed at the same place of the ones We are checking the target text

def load_text():
    with open("typing_test_file.txt", 'r', encoding="utf-8") as file:
        lines = file.readlines()
        return random.choice(lines).strip()

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    key = ''
    start_time = time.time()

    stdscr.nodelay(True)   # for the wpm to decrease when we are not typing anything, this may cause crash so whe have to create exectpion
    #keep stealing those 4 next lines causes we are going to use them mulitple times


    while True:

        time_elapsed = max(time.time() - start_time, 1)  # 1 is to avoid the division by 0 error, since the time elpased
        #can be very short

        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)    #assuming here the average word has 5 char, picked from a website

        stdscr.clear()
        """  this has been taken from here to put it in the display function
        stdscr.addstr(target_text)
        for char in current_text:
            stdscr.addstr(char,curses.color_pair(1))
        """

        display_text(stdscr, target_text, current_text, wpm)

        stdscr.refresh()

        # stdscr.clear(), addstr() and refresh() are important, cause if we don't clean the screen,
        # when we start typing, it's gonna repeat the text cause we are not cleaning after new line

        #convert a list to a string using .join()
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break
        try:

            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:    # ASCII representation of ESC is 27, so whenever ESC is pressed, let's break
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):  #checking if key = backspace
            if len(current_text) > 0:
                current_text.pop()

        elif len(current_text) < len(target_text):  # for the code not to crash due to target and current index not matching
            current_text.append(key)






def main(stdscr):
    # initializing colors in the main function
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    """
    stdscr.clear()
    stdscr.addstr(1, 5, "Hello Word!", curses.color_pair(1))
    stdscr.addstr(1, 5, "Hello Word!", curses.color_pair(1))
# displaying 2 times will make they overlay on each other, that's what we are gonna use to deploy our programm
    stdscr.refresh()
    """

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You've completed the test! Press any key to continue or ESC to quit: ")
        key = stdscr.getkey()

        if ord(key) == 27:
            break




    #key = stdscr.getkey()  # this can help to get the key the user typed in
   # print(key)



wrapper(main)

