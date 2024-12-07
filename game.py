"""This module implements the logic and the interface for the game"""

import tkinter as tk
import random

class GameOfGo:
    """Class to initialize and handle Game of Go"""
    def __init__(self, root, computer, board_size):
        """Initialize the components for the game"""
        self.root = root
        self.board_size = board_size

        self.computer = computer
        if computer:
            print("You play with computer")
        else:
            print("You play with another person")

        self.CANVAS_DIMENSION = 700
        self.TABLE_DIMENSION = 600
        self.CELL_DIMENSION = self.TABLE_DIMENSION // (self.board_size - 1)
        self.radius = self.CELL_DIMENSION // 2
        self.COLOR = "orange2"

        self.turn = "black"
        self.table = [["None" for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.previous_states = []
        self.black_score = 0
        self.white_score = 6.5
        self.previous_pass = -9
        self.check_number = -1

        self.root.geometry(f"{self.CANVAS_DIMENSION}x{self.CANVAS_DIMENSION}")
        self.root.title(f"Game of Go - {self.board_size}x{self.board_size}")

        self.canvas = tk.Canvas(
            self.root,
            width=self.CANVAS_DIMENSION,
            height=self.CANVAS_DIMENSION,
            bg=self.COLOR)
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
        menu.add_command(label="Exit", command=self.exit_game)
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
        main(self.computer, self.board_size)

    def exit_game(self):
        """Exit the game"""
        self.score()
        self.root.destroy()

    def pass_turn(self):
        """Pass the player's turn"""
        self.check_number = self.check_number + 1

        if self.previous_pass == -9:
            self.previous_pass = self.check_number
        else:
            if self.previous_pass + 1 == self.check_number:
                print(f"Game ended because there was 2 passes consecutively!")
                self.score()
                self.restart_game()
            else:
                self.previous_pass = self.check_number

        print(f"{self.turn.capitalize()} passed the turn!")
        self.turn = "white" if self.turn == "black" else "black"

    def make_move(self, event):
        """Place a piece if the desired place to move is empty"""
        x, y = event.x, event.y

        col = round((x - self.offset_x) / self.CELL_DIMENSION)
        row = round((y - self.offset_y) / self.CELL_DIMENSION)

        if 0 <= col < self.board_size and 0 <= row < self.board_size:
            if self.table[row][col] == "None":
                if not self.is_suicide(row, col):
                    if not self.is_ko(row, col):
                        self.check_number = self.check_number + 1

                        self.table[row][col] = self.turn
                        self.previous_states.append([row[:] for row in self.table])

                        self.check_captures()
                        self.draw_piece(row, col)
                        if self.computer:
                            self.ai_move()
                    else:
                        print(f"{self.turn.upper()}, you can't recreate a previous position!")
                else:
                    print(f"{self.turn.upper()} made a suicidal move! Please choose another one!")
            else:
                print(f"{self.turn.upper()}, a stone is already there!")
        else:
            print(f"{self.turn.upper()}, invalid move! Please choose another one!")

    def draw_piece(self, row, col):
        """Draw the piece on the desired position"""
        pos_x = self.offset_x + col * self.CELL_DIMENSION
        pos_y = self.offset_y + row * self.CELL_DIMENSION

        self.canvas.create_oval(
            pos_x - self.radius, pos_y - self.radius,
            pos_x + self.radius, pos_y + self.radius,
            fill=self.turn)

        self.turn = "black" if self.turn == "white" else "white"

    def check_captures(self, just_check=False):
        """Check if exists a group to be captured"""
        opponent = "black" if self.turn == "white" else "white"

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.table[row][col] == opponent:
                    group = self.find_group(row, col)
                    if not self.has_liberties(group):
                        if just_check:
                            self.fake_capture(group)
                        else:
                            self.capture(group)

    def has_liberties(self, group):
        """Check if a group has liberties"""
        for row, col in group:
            for r, c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                pos_x = row + r
                pos_y = col + c
                if (0 <= pos_x < self.board_size
                        and 0 <= pos_y < self.board_size):
                    if self.table[pos_x][pos_y] == "None":
                        return True
        return False

    def find_group(self, row, col):
        """Find the group of a stone"""
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
        #  print(f"The group is: {group}")
        return group

    def capture(self, group):
        """Delete the captured group from the board"""
        for row, col in group:
            self.table[row][col] = "None"

            x_pos = self.offset_x + col * self.CELL_DIMENSION
            y_pos = self.offset_y + row * self.CELL_DIMENSION

            self.canvas.create_oval(
                x_pos - self.radius, y_pos - self.radius,
                x_pos + self.radius, y_pos + self.radius,
                fill=self.COLOR, outline=self.COLOR)

            self.canvas.create_line(
                x_pos,
                max(y_pos - self.radius, self.offset_y),
                x_pos,
                min(y_pos + self.radius + 1, self.TABLE_DIMENSION + self.offset_y))
            self.canvas.create_line(
                max(x_pos - self.radius, self.offset_x),
                y_pos,
                min(x_pos + self.radius + 1, self.TABLE_DIMENSION + self.offset_x),
                y_pos)

            if self.turn == "black":
                self.black_score += 1
            else:
                self.white_score += 1

    def fake_capture(self, group):
        """Fake delete the captured group from the board, just to check ko"""
        for row, col in group:
            self.table[row][col] = "None"

    def is_ko(self, row, col):
        """Check if this move wants to recreate an earlier board position"""
        current_table = [row[:] for row in self.table]

        self.table[row][col] = self.turn
        self.check_captures(just_check=True)
        if self.table in self.previous_states:
            #  print(f"IS ko")
            self.table = current_table
            return True
        else:
            # print(f"Is not ko")
            self.table = current_table
            return False

    def is_suicide(self, row, col):
        """
        Check for suicidal move
        Meaning check if the group resulted has liberties or captures
        """
        self.table[row][col] = self.turn
        group = self.find_group(row, col)

        if self.has_liberties(group):
            self.table[row][col] = "None"
            #print("Has liberties")
            return False

        self.table[row][col] = self.turn
        opponent = "white" if self.turn == "black" else "black"
        for r, c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            pos_x = row + r
            pos_y = col + c
            if (0 <= pos_x < self.board_size and
                    0 <= pos_y < self.board_size and
                    self.table[pos_x][pos_y] == opponent):
                found_group = self.find_group(pos_x, pos_y)
                if not self.has_liberties(found_group):
                    self.table[row][col] = "None"
                    return False

        self.table[row][col] = "None"
        return True

    def score(self):
        """Implement 'stone scoring' and chinese method """
        visited = set()

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.table[row][col] == "black":
                    self.black_score += 1
                elif self.table[row][col] == "white":
                    self.white_score += 1

                elif (row, col) not in visited:
                    group_size, color = self.find_territory_color(row, col, visited)
                    print(f"Group size: {group_size}, color: {color}")
                    if color == "black":
                        self.black_score += group_size
                    elif color == "white":
                        self.white_score += group_size

        winner = "black" if self.black_score > self.white_score \
            else "white"

        print(f"{winner.capitalize()} won the Game of Go!")
        print(f"WHITE SCORE: {self.white_score}")
        print(f"BLACK SCORE: {self.black_score}")

    def find_territory_color(self, row, col, visited):
        """Check if the unoccupied territory belong to white, black or both"""
        possible_neighbours = [(row, col)]
        no_none_neighbours = set()
        none_neighbours = set()

        while possible_neighbours:
            current_row, current_col = possible_neighbours.pop()
            if (current_row, current_col) not in visited:
                visited.add((current_row, current_col))

                if self.table[current_row][current_col] == "None":
                    none_neighbours.add((current_row, current_col))
                    for r, c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        pos_x = current_row + r
                        pos_y = current_col + c
                        if (0 <= pos_x < self.board_size and
                                0 <= pos_y < self.board_size):
                            if self.table[pos_x][pos_y] == "None":
                                possible_neighbours.append((pos_x, pos_y))
                            else:
                                no_none_neighbours.add(self.table[pos_x][pos_y])
        if len(no_none_neighbours) == 1:
            return len(none_neighbours), no_none_neighbours.pop()
        return len(none_neighbours), "None"

    def ai_move(self):
        """Decision for white stones by AI - random"""
        possible_moves = self.find_possible_moves()
        if not possible_moves:
            self.pass_turn()
        else:
            self.check_number = self.check_number + 1
            row, col = random.choice(possible_moves)

            self.table[row][col] = self.turn
            self.previous_states.append([row[:] for row in self.table])

            self.check_captures()
            self.draw_piece(row, col)

    def find_possible_moves(self):
        """Find all possible moves for AI to make"""
        possible_moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.table[row][col] == "None":
                    if (not self.is_ko(row, col) and
                            not self.is_suicide(row, col)):
                        possible_moves.append((row, col))
        return possible_moves
