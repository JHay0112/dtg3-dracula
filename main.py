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
    # window root object
    tk_parent = None

    # frames
    frm_container = None
    frm_inventory = None
    frm_map = None
    frm_log = None

    # canvases
    cnv_inventory = None
    cnv_map = None
    cnv_log = None

    # game objects
    player = None
    room_manager = None
    rooms = None

    def __init__(self, tk_parent, name):
        self.name = name
        self.tk_parent = tk_parent

        # un-hide the window
        self.tk_parent.deiconify()

        self.player = entities.EntityPlayer(name)
        self.room_manager = navigation.RoomManager()
        self.rooms = self.room_manager.get_rooms()

        self.player.set_current_room(self.rooms["room_entrance"])
        print(f"{self.player.get_name()} is in {self.player.get_current_room().get_name()}")

        self.frm_container = tk.Frame(self.tk_parent)
        self.frm_inventory = tk.Frame(self.frm_container, highlightbackground="black", highlightthickness=1)
        self.frm_map = tk.Frame(self.frm_container, highlightbackground="black", highlightthickness=1)
        self.frm_log = tk.Frame(self.frm_container, highlightbackground="black", highlightthickness=1)

        lbl_inventory = ttk.Label(self.frm_container, text="Inventory", font=("Arial", 18))
        lbl_map = ttk.Label(self.frm_container, text="Map", font=("Arial", 18))
        lbl_log = ttk.Label(self.frm_container, text="Log", font=("Arial", 18))

        self.cnv_inventory = tk.Canvas(self.frm_inventory, width=100, height=300)
        self.cnv_map = tk.Canvas(self.frm_map, width=300, height=300)
        self.cnv_log = tk.Canvas(self.frm_log, width=100, height=300)

        lbl_inventory.grid(row=0, column=0)
        lbl_map.grid(row=0, column=1)
        lbl_log.grid(row=0, column=2)

        self.cnv_inventory.grid(row=0, column=0)
        self.cnv_map.grid(row=0, column=0)
        self.cnv_log.grid(row=0, column=0)

        self.frm_container.grid(row=0, column=0)
        self.frm_inventory.grid(row=1, column=0)
        self.frm_map.grid(row=1, column=1)
        self.frm_log.grid(row=1, column=2)

        # bind keyboard keys to movement
        self.tk_parent.bind("w", lambda event, direction="N": self.move(direction))
        self.tk_parent.bind("d", lambda event, direction="E": self.move(direction))
        self.tk_parent.bind("s", lambda event, direction="S": self.move(direction))
        self.tk_parent.bind("a", lambda event, direction="W": self.move(direction))

        # render the map
        self.render(self.cnv_map)

    def render(self, canvas):
        # clear the screen
        canvas.delete(tk.ALL)

        valid_moves = self.player.get_current_room().get_valid_moves()

        # render the current room
        canvas.create_rectangle(50, 50, 250, 250, fill="white", outline="black")
        # north hallway
        if valid_moves[0] is not None:
            canvas.create_rectangle(125, 0, 175, 50, fill="white", outline="black")
        # east hallway
        if valid_moves[1] is not None:
            canvas.create_rectangle(250, 125, 310, 175, fill="white", outline="black")
        # south hallway
        if valid_moves[2] is not None:
            canvas.create_rectangle(125, 250, 175, 310, fill="white", outline="black")
        # west hallway
        if valid_moves[3] is not None:
            canvas.create_rectangle(0, 125, 50, 175, fill="white", outline="black")

    def move(self, direction):
        if direction == "N":
            valid_moves = self.player.get_current_room().get_valid_moves()
            if valid_moves[0] is None:
                print("Can't go that way.")
            else:
                self.player.set_current_room(valid_moves[0])
                print(f"{self.player.get_name()} is in {self.player.get_current_room().get_name()}")
        elif direction == "E":
            valid_moves = self.player.get_current_room().get_valid_moves()
            if valid_moves[1] is None:
                print("Can't go that way.")
            else:
                self.player.set_current_room(valid_moves[1])
                print(f"{self.player.get_name()} is in {self.player.get_current_room().get_name()}")
        elif direction == "S":
            valid_moves = self.player.get_current_room().get_valid_moves()
            if valid_moves[2] is None:
                print("Can't go that way.")
            else:
                self.player.set_current_room(valid_moves[2])
                print(f"{self.player.get_name()} is in {self.player.get_current_room().get_name()}")
        elif direction == "W":
            valid_moves = self.player.get_current_room().get_valid_moves()
            if valid_moves[3] is None:
                print("Can't go that way.")
            else:
                self.player.set_current_room(valid_moves[3])
                print(f"{self.player.get_name()} is in {self.player.get_current_room().get_name()}")

        self.render(self.cnv_map)


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
    root.geometry("600x400")
    root.resizable(width=False, height=False)
    window = GUIMain(root)
    root.mainloop()
