# ttk has theming support for widgets, and look closer to system-default
import tkinter as tk
import tkinter.ttk as ttk
import sys


# callback for window exit (X button)
def on_close():
    sys.exit()


class EntityPlayer:
    name = ""
    health = 100

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_health(self):
        return self.health

    def set_health(self, health):
        self.health = health


class GUIGame:
    # user's name
    name = ""

    def __init__(self, tk_parent, name):
        print(name)


class GUIMain:
    # tk window objects
    _start_window = tk.Toplevel()
    _tk_root = None

    def __init__(self, tk_parent):
        self._tk_root = tk_parent
        # hide the root window and spawn a new window for the start screen
        self._tk_root.withdraw()

        # if the user hits the X button, call on_close which will exit the application entirely
        self._start_window.protocol("WM_DELETE_WINDOW", on_close)
        self._tk_root.protocol("WM_DELETE_WINDOW", on_close)

        # user's name
        var_name = tk.StringVar()

        # generate all widgets on a frame before adding them to the grid
        frm_container = ttk.Frame(self._start_window)
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
                               command=lambda: self.start_game(var_name.get()))

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

    def start_game(self, name):
        # hide the start window
        self._start_window.withdraw()
        # create the main game window
        game_window = GUIGame(self._tk_root, name)


if __name__ == "__main__":
    root = tk.Tk()
    window = GUIMain(root)
    root.mainloop()
