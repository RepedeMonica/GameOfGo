import tkinter as tk

def choose_board_size():
    """Display the start menu in which the user chooses the board size"""
    def submitted():
        """Handle the chosen table dimension by the player"""
        selected_size = int(possible_dimensions.get())
        print(f"Selected size is {selected_size}")
        root.destroy()
        from checkers import main
        main(selected_size)

    root = tk.Tk()
    root.geometry("600x600")
    root.title("Welcome to Game of Go!")

    canvas = tk.Canvas(root, width=600, height=600, bg="tan")
    canvas.pack(fill="both", expand=True)

    frame = tk.Frame(canvas, bg="tan")
    frame.pack(expand=True)

    indications = tk.Label(
        frame, text="Please choose the size of the board:",
        font=("Chiller",28), bg="tan")
    indications.pack()

    second_frame = tk.Frame(frame, bg="tan")
    second_frame.pack()

    possible_dimensions = tk.Spinbox(
        second_frame, values=["9", "13", "17", "19"],
        font=("Chiller",28), width=3, bg="tan")
    possible_dimensions.pack(side=tk.LEFT, padx=5)

    button = tk.Button(
        second_frame, text="Submit", font=("Chiller",20),
        command=submitted, bg="tan")
    button.pack(side=tk.RIGHT)

    root.mainloop()
