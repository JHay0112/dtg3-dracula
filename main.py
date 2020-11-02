# ttk has theming support for widgets, and looks closer to system-default
import tkinter as tk
import tkinter.ttk as ttk
import entities
import navigation
import sys


# callback for window exit (X button)
def on_close():
    sys.exit()


class GUIGame:
    player = None
    room_manager = None
    rooms = None

    def __init__(self, tk_parent, name):
        self.name = name

        # un-hide the window
        tk_parent.deiconify()

        self.player = entities.EntityPlayer(name)
        self.room_manager = navigation.RoomManager()
        self.rooms = self.room_manager.get_rooms()

        self.player.set_current_room(self.rooms["room_entrance"])
        print(f"{self.player.get_name()} is in {self.player.get_current_room().get_name()}")

        frm_container = ttk.Frame(tk_parent)
        btn_north = ttk.Button(frm_container, text="North", command=lambda: self.move("N"))
        btn_north.pack()
        btn_east = ttk.Button(frm_container, text="East", command=lambda: self.move("E"))
        btn_east.pack()
        btn_south = ttk.Button(frm_container, text="South", command=lambda: self.move("S"))
        btn_south.pack()
        btn_west = ttk.Button(frm_container, text="West", command=lambda: self.move("W"))
        btn_west.pack()
        frm_container.pack()

    def move(self, direction):
        if direction == "N":
            valid_moves = self.player.get_current_room().get_valid_moves()
            if valid_moves[0] is None:
                print("Can't go that way.")
            else:
                self.player.set_current_room(valid_moves[0])
                print(f"{self.player.get_name()} is in {self.player.get_current_room().get_name()}")
        if direction == "E":
            valid_moves = self.player.get_current_room().get_valid_moves()
            if valid_moves[1] is None:
                print("Can't go that way.")
            else:
                self.player.set_current_room(valid_moves[1])
                print(f"{self.player.get_name()} is in {self.player.get_current_room().get_name()}")
        if direction == "S":
            valid_moves = self.player.get_current_room().get_valid_moves()
            if valid_moves[2] is None:
                print("Can't go that way.")
            else:
                self.player.set_current_room(valid_moves[2])
                print(f"{self.player.get_name()} is in {self.player.get_current_room().get_name()}")
        if direction == "W":
            valid_moves = self.player.get_current_room().get_valid_moves()
            if valid_moves[3] is None:
                print("Can't go that way.")
            else:
                self.player.set_current_room(valid_moves[3])
                print(f"{self.player.get_name()} is in {self.player.get_current_room().get_name()}")


class GUIMain:
    def __init__(self, tk_parent):
        # hide the root window and spawn a new window for the start screen
        tk_parent.withdraw()
        tk_start_window = tk.Toplevel()

        # if the user hits the X button, call on_close which will exit the application entirely
        tk_start_window.protocol("WM_DELETE_WINDOW", on_close)
        tk_parent.protocol("WM_DELETE_WINDOW", on_close)

        # user's name
        var_name = tk.StringVar()

        # generate all widgets on a frame before adding them to the grid
        frm_container = ttk.Frame(tk_start_window)
        lbl_welcome = ttk.Label(frm_container, text="Welcome!", font=("Arial", 18))
        msg_intro = tk.Message(frm_container,
                               text="You've stumbled into Dracula's castle, and you need to find a way "
                                    "out - or kill him!", justify="center", font=("Arial", 12))

        msg_tip = tk.Message(frm_container,
                             text="Tip: you can use the W-A-S-D keys on your keyboard to move.",
                             justify="center", font=("Arial", 12))

        lbl_name = ttk.Label(frm_container, text="Please enter your name:", font=("Arial", 12))
        ent_name = ttk.Entry(frm_container, textvariable=var_name)
        btn_quit = ttk.Button(frm_container, text="Quit", command=sys.exit)
        btn_start = ttk.Button(frm_container, text="Start",
                               command=lambda: self.start_game(var_name.get(), tk_start_window, tk_parent))

        # insert widgets into the grid, span columns to center them relative to the buttons
        lbl_welcome.grid(row=0, columnspan=2)
        msg_intro.grid(row=1, columnspan=2)
        msg_tip.grid(row=2, columnspan=2)
        lbl_name.grid(row=3, columnspan=2)
        ent_name.grid(row=4, columnspan=2, sticky="nesw")
        btn_quit.grid(row=5, column=0, sticky="nesw")
        btn_start.grid(row=5, column=1, sticky="nesw")

        # pack the frame containing all widgets with some padding
        frm_container.pack(padx=20, pady=20)

    def start_game(self, name, tk_start_window, tk_parent):
        # hide the start window
        tk_start_window.withdraw()
        # create the main game window
        game_window = GUIGame(tk_parent, name)


if __name__ == "__main__":
    root = tk.Tk()
    window = GUIMain(root)
    root.mainloop()
