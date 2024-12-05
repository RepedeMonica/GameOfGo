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
        self.previous_states = []
        self.black_score = 0
        self.white_score = 0

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

        if 0 <= col < self.board_size and 0 <= row < self.board_size:
            if self.table[row][col] == "None":
                #not implemented yet: check if it was a previous state -> ko
                if not self.check_suicide(row, col):
                    self.table[row][col] = self.turn
                    self.check_captures()
                    self.check_ko()
                    self.draw_piece(row, col)
                else:
                    print(f"{self.turn.capitalize()} made a suicidal move! Please choose another one!")

    def draw_piece(self, row, col):
        """Draw the piece on the desired position"""
        cx = self.offset_x + col * self.CELL_DIMENSION
        cy = self.offset_y + row * self.CELL_DIMENSION
        radius = self.CELL_DIMENSION // 3
        self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill=self.turn)
        self.turn = "black" if self.turn == "white" else "white"

    def check_captures(self):
        """Check if exists a group to be captured"""
        opponent = "black" if self.turn == "white" else "white"

        for row in range(0, self.board_size):
            for col in range(0, self.board_size):
                if self.table[row][col] == opponent:
                    group = self.find_group(row, col)
                    if not self.has_liberties(group):
                        self.capture(group)

    def has_liberties(self, group):
        """Check if a group has liberties"""
        for row, col in group:
            for r, c in [(-1,0),(1,0),(0,-1),(0,1)]:
                pos_x =row + r
                pos_y =col + c
                if (0 <= pos_x < self.board_size
                        and 0 <= pos_y < self.board_size):
                    if self.table[pos_x][pos_y] == "None":
                        return True
        return False

    def find_group(self, row, col):
        """Find the group of a piece"""
        color = self.table[row][col]
        possible_group_elements = [(row, col)]
        group = set()

        while possible_group_elements:
            current_row, current_col = possible_group_elements.pop()
            if (current_row, current_col) not in group:
                group.add((current_row, current_col))

                for r, c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    pos_x = current_row + r
                    pos_y = current_col + c
                    if (0 <= pos_x < self.board_size
                            and 0 <= pos_y < self.board_size):
                        if (self.table[pos_x][pos_y] == color
                                and (pos_x, pos_y) not in group):
                            possible_group_elements.append((pos_x, pos_y))
        return group

    def capture(self, group):
        """Delete the captured group from the board"""
        for row, col in group:
            self.table[row][col] = "None"

            x_pos = self.offset_x + col * self.CELL_DIMENSION
            y_pos = self.offset_y + row * self.CELL_DIMENSION
            radius = self.CELL_DIMENSION // 3

            self.canvas.create_oval(
                x_pos - radius, y_pos - radius,
                x_pos + radius, y_pos + radius,
                fill="tan", outline="tan")
            self.canvas.create_line(
                x_pos , y_pos - radius,
                x_pos , y_pos + radius + 1)
            self.canvas.create_line(
                x_pos - radius, y_pos,
                x_pos + radius + 1, y_pos )

            if self.turn == "black":
                self.black_score += 1
            else:
                self.white_score += 1

    def check_ko(self):
        """Not implemented yet"""
        pass

    def check_suicide(self, row, col):
        """
        Check for suicidal move
        Meaning check if the group resulted has liberties or captures
        """
        self.table[row][col] = self.turn
        group = self.find_group(row, col)

        if self.has_liberties(group):
            self.table[row][col] = "None"
            return False

        for r, c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            pos_x = row + r
            pos_y = col + c
            if (0 <= pos_x < self.board_size and
                    0 <= pos_y < self.board_size):
                found_group = self.find_group(pos_x, pos_y)
                if not self.has_liberties(found_group):
                    self.table[row][col] = "None"
                    return False

        self.table[row][col] = "None"
        return True


