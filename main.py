import tkinter as tk
import tkinter.ttk as ttk
import sys


def on_close():
    sys.exit()


class GUIStart:
    def __init__(self, tk_parent):
        # if the user hits the X button, call on_close which will exit the application entirely
        tk_parent.protocol("WM_DELETE_WINDOW", on_close)

        # generate all widgets on a frame before adding them to the grid
        self.frm_container = ttk.Frame(tk_parent)
        self.lbl_welcome = ttk.Label(self.frm_container, text="Welcome!", font=("Arial", 18))
        self.msg_intro = tk.Message(self.frm_container,
                                    text="You've stumbled into Dracula's castle, and you need to find a way "
                                         "out - or kill him!", justify="center", font=("Arial", 12))

        self.msg_tip = tk.Message(self.frm_container,
                                  text="Tip: you can use the W-A-S-D keys on your keyboard to move.",
                                  justify="center", font=("Arial", 12))

        self.lbl_name = ttk.Label(self.frm_container, text="Please enter your name:", font=("Arial", 12))
        self.ent_name = ttk.Entry(self.frm_container)
        self.btn_quit = ttk.Button(self.frm_container, text="Quit", command=sys.exit)
        self.btn_start = ttk.Button(self.frm_container, text="Start")

        # insert widgets into the grid, span columns to center them relative to the buttons
        self.lbl_welcome.grid(row=0, columnspan=2)
        self.msg_intro.grid(row=1, columnspan=2)
        self.msg_tip.grid(row=2, columnspan=2)
        self.lbl_name.grid(row=3, columnspan=2)
        self.ent_name.grid(row=4, columnspan=2, sticky="nesw")
        self.btn_quit.grid(row=5, column=0, sticky="nesw")
        self.btn_start.grid(row=5, column=1, sticky="nesw")

        # pack the frame containing all widgets with some padding
        self.frm_container.pack(padx=20, pady=20)


class GUIMain:
    def __init__(self, tk_parent):
        # hide the root window and spawn a new window for the start screen
        tk_parent.withdraw()
        start_window = tk.Toplevel()
        self.start_screen = GUIStart(start_window)


if __name__ == "__main__":
    root = tk.Tk()
    window = GUIMain(root)
    root.mainloop()
