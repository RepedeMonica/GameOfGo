import tkinter as tk

class GameOfGo:
    """Class to initialize and handle Game of Go"""
    def __init__(self, root, board_size):
        """
        Initialize the game of go
        :param root: The root Tkinter window
        :param board_size: The size of the board
        """
        self.root = root
        self.board_size = board_size
        self.CANVAS_DIMENSION = 700
        self.TABLE_DIMENSION = 600
        self.CELL_DIMENSION = self.TABLE_DIMENSION // (self.board_size - 1)
        self.turn = "black"
        self.table = [["None" for _ in range(self.board_size)] for _ in range(self.board_size)]

        self.root.geometry(f"{self.CANVAS_DIMENSION}x{self.CANVAS_DIMENSION}")
        self.root.title(f"Game of Go - {self.board_size}x{self.board_size}")

        self.canvas = tk.Canvas(
            self.root,
            width=self.CANVAS_DIMENSION,
            height=self.CANVAS_DIMENSION,
            bg="tan")
        self.canvas.pack(fill="both", expand=True)

        self.offset_x = (self.CANVAS_DIMENSION - self.TABLE_DIMENSION) // 2
        self.offset_y = (self.CANVAS_DIMENSION - self.TABLE_DIMENSION) // 2

        self.add_menu()

        self.draw_grid()

        self.canvas.bind("<Button-1>", self.make_move)

    def add_menu(self):
        """Add a menu to: restart the game, pass a turn or exit the game"""
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        menu.add_command(label="New Game", command=self.restart_game)
        menu.add_command(label="Exit", command=self.root.destroy)
        menu.add_command(label="Pass", command=self.pass_turn)

    def draw_grid(self):
        """Draw the board"""
        for i in range(self.board_size):
            self.canvas.create_line(
                self.offset_x + self.CELL_DIMENSION * i,
                self.offset_y,
                self.offset_x + self.CELL_DIMENSION * i,
                self.offset_y + self.CELL_DIMENSION * (self.board_size - 1))
            self.canvas.create_line(
                self.offset_x,
                self.offset_y + self.CELL_DIMENSION * i,
                self.offset_x + self.CELL_DIMENSION * (self.board_size - 1),
                self.offset_y + self.CELL_DIMENSION * i)

    def restart_game(self):
        """Restart the game"""
        self.root.destroy()
        from checkers import main
        main(self.board_size)

    def pass_turn(self):
        """Pass the player's turn"""
        print(f"{self.turn.capitalize()} passed the turn!")
        self.turn = "white" if self.turn == "black" else "black"

    def make_move(self, event):
        """Place a piece if the desired place to move is empty"""
        x, y = event.x, event.y

        if not (self.offset_x <= x <= self.offset_x + self.TABLE_DIMENSION and
                self.offset_y <= y <= self.offset_y + self.TABLE_DIMENSION):
            print(f"{self.turn.capitalize()} invalid move! Please choose another one!")

        col = round((x - self.offset_x) / self.CELL_DIMENSION)
        row = round((y - self.offset_y) / self.CELL_DIMENSION)

        cx = self.offset_x + col * self.CELL_DIMENSION
        cy = self.offset_y + row * self.CELL_DIMENSION

        radius = self.CELL_DIMENSION // 3

        if 0 <= col < self.board_size and 0 <= row < self.board_size:
            if self.table[row][col] == "None":
                self.table[row][col] = self.turn
                if self.turn == "black":
                    self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill="black")
                    self.turn = "white"
                else:
                    self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill="white")
                    self.turn = "black"
                self.check_adjacent()

    def check_adjacent(self):
        """Not implemented yet"""
        print(self.table)
        print()
