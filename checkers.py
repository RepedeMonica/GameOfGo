from startMenu import choose_board_size
from game import GameOfGo
import tkinter as tk

def main(selected_size=None):
    """The entry point of the game"""
    if selected_size is None:
        choose_board_size()
    else:
        root = tk.Tk()
        GameOfGo(root, selected_size)
        root.mainloop()

if __name__ == '__main__':
    main()


