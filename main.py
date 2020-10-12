import tkinter as tk
import tkinter.ttk as ttk


class GUIStart:
    def __init__(self, tk_parent):
        self.lbl_welcome = ttk.Label(tk_parent, text="Welcome!")
        self.lbl_welcome.config(font=("Arial", 24))
        self.lbl_welcome.grid(row=0)

        self.lbl_intro = ttk.Label(tk_parent, text="You've stumbled into Dracula's castle, and you need to find a way "
                                                   "out - or kill him!")
        self.lbl_intro.config(font=("Arial", 12))
        self.lbl_intro.grid(row=1)


class GUIMain:
    def __init__(self, tk_parent):
        self.start_screen = GUIStart(tk_parent)


if __name__ == "__main__":
    root = tk.Tk()
    window = GUIMain(root)
    root.mainloop()
