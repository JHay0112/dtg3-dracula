import tkinter as tk
import gui

if __name__ == "__main__":
    root = tk.Tk()
    # TODO dynamic resizing?
    root.resizable(width=False, height=False)
    window = gui.GUIMain(root)
    root.mainloop()
