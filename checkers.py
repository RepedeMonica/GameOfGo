"""This module connects the start menu with the window for the game"""

import tkinter as tk
import sys
from startMenu import choose_board_size
from game import GameOfGo

def main(computer=False, selected_size=None):
    """The entry point of the game"""
    if selected_size is None:
        choose_board_size(computer)
    else:
        root = tk.Tk()
        GameOfGo(root, computer, selected_size)
        root.mainloop()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: checkers.py <computer/human>")
        sys.exit(1)
    main(computer= ("computer"== sys.argv[1]))


