import curses  #this is used for styling of the terminal.
import random
from curses import wrapper  #this is to initialize curses in terminal and then restore back to previous state after program's over.
import time

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        if char == target[i]:
            color = curses.color_pair(1)
        else:
            color = curses.color_pair(2)
        # displaying on 0th row, ith column
        stdscr.addstr(0, i, char, color)

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()  #this is some big number(seconds after some date in past, and this keeps increasing)
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / 5) / (time_elapsed / 60))  #considering average word has 5 chars

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        # so this program displays correct wpm only if whole target text was written the same.
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        # so if key isn't pressed, this will not wait and below lines will not executed and this will go to start of loop, so that wpm keeps changing.
        try:
            key = stdscr.getkey()
        except:
            continue

        # if escape key pressed stop the loop.
        if ord(key) == 27:
            break
        # if backspace key (in any operating system) is pressed, delete last element in list.
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):  #stdscr is standard output screen
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(3, 0, "You completed the test! Press any key to take test again or press (esc) to exit.")
        key = stdscr.getkey()
        if ord(key) == 27:
            break


wrapper(main)