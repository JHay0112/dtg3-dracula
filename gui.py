# name: gui.py
# author: Mitchell Ward
# purpose: contains GUI classes and functionality

# ttk has theming support for widgets, and looks closer to system-default
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from playsound import playsound
import os
import entities
import navigation
import sys
import random


# purpose: callback for window exit (X button)
def on_close_exit():
    sys.exit()


# purpose: dummy callback to "disable" the X button on battle window
def on_close_ignore():
    pass


# purpose: handles the battle window and battle system itself
class GUIBattle:
    # constants
    # player attacks
    DAMAGE_STRIKE_MIN = 1
    DAMAGE_STRIKE_MAX = 10
    DAMAGE_SMASH_MIN = 1
    DAMAGE_SMASH_MAX = 20
    # enemy attack
    DAMAGE_TAKEN_MIN = 1
    DAMAGE_TAKEN_MAX = 10
    # enemy attack if player blocks
    DAMAGE_TAKEN_BLOCK_MIN = 0
    DAMAGE_TAKEN_BLOCK_MAX = 3

    def __init__(self, tk_parent, game_object, enemy):
        self.tk_parent = tk_parent
        self.tk_parent.protocol("WM_DELETE_WINDOW", on_close_ignore)

        # main game object
        self.game_object = game_object

        self.player = game_object.player
        self.enemy = enemy

        # create and set stringvars so health labels can be updated elsewhere
        self.var_player_health = tk.StringVar()
        self.var_enemy_health = tk.StringVar()
        self.var_player_health.set(str(self.player.get_health()))
        self.var_enemy_health.set(str(self.enemy.get_health()))

        # generate all widgets on a frame before adding them to the grid
        frm_container = ttk.Frame(self.tk_parent)
        lbl_battle = ttk.Label(frm_container, text="Battle", font=("Arial", 18))
        if self.enemy.get_name() == "Dracula":
            msg_intro = tk.Message(frm_container, text=f"You've discovered Dracula's hiding place! Kill him to escape!",
                                   justify="center", font=("Arial", 12))
        else:
            msg_intro = tk.Message(frm_container, text=f"You've stumbled upon a {self.enemy.get_name()}",
                                   justify="center", font=("Arial", 12))

        lbl_enemy = ttk.Label(frm_container, text=self.enemy.get_name(), font=("Arial", 16))
        lbl_enemy_health = ttk.Label(frm_container, textvariable=self.var_enemy_health, font=("Arial", 12))

        lbl_player = ttk.Label(frm_container, text=self.player.get_name(), font=("Arial", 16))
        lbl_player_health = ttk.Label(frm_container, textvariable=self.var_player_health, font=("Arial", 12))

        btn_strike = ttk.Button(frm_container, text="Strike", command=lambda action="strike": self.battle(action))
        btn_smash = ttk.Button(frm_container, text="Smash", command=lambda action="smash": self.battle(action))
        btn_block = ttk.Button(frm_container, text="Block", command=lambda action="block": self.battle(action))

        # insert widgets into the grid, span columns to center them relative to the buttons
        lbl_battle.grid(row=0, columnspan=2)
        msg_intro.grid(row=1, columnspan=2)
        lbl_enemy.grid(row=2, columnspan=2)
        lbl_enemy_health.grid(row=3, columnspan=2)
        lbl_player.grid(row=4, columnspan=2)
        lbl_player_health.grid(row=5, columnspan=2)

        btn_strike.grid(row=6, column=0, sticky="nesw")
        btn_smash.grid(row=6, column=1, sticky="nesw")
        btn_block.grid(row=7, column=0, sticky="nesw", columnspan=2)

        # pack the frame containing all widgets with some padding
        frm_container.pack(padx=20, pady=20)

    # purpose: handles battle action inputs
    def battle(self, action):
        if action == "block":
            damage_taken = random.randint(self.DAMAGE_TAKEN_BLOCK_MIN, self.DAMAGE_TAKEN_BLOCK_MAX)
            # play a random sound from the given action's sound directory
            playsound("sounds\\block\\" + random.choice(os.listdir("sounds\\block\\")))
            self.apply_damage(damage_taken, 0)
        elif action == "strike":
            damage_given = random.randint(self.DAMAGE_STRIKE_MIN, self.DAMAGE_STRIKE_MAX)
            damage_taken = random.randint(self.DAMAGE_TAKEN_MIN, self.DAMAGE_TAKEN_MAX)
            playsound("sounds\\strike\\" + random.choice(os.listdir("sounds\\strike\\")))
            self.apply_damage(damage_taken, damage_given)
        elif action == "smash":
            damage_given = random.randint(self.DAMAGE_SMASH_MIN, self.DAMAGE_SMASH_MAX)
            damage_taken = random.randint(self.DAMAGE_TAKEN_MIN, self.DAMAGE_TAKEN_MAX)
            playsound("sounds\\smash\\" + random.choice(os.listdir("sounds\\smash\\")))
            self.apply_damage(damage_taken, damage_given)

    # purpose: applies damage calculated in battle function, and checks for player or enemy death
    def apply_damage(self, damage_taken, damage_given):
        enemy_health = self.enemy.get_health() - damage_given
        player_health = self.player.get_health() - damage_taken

        # apply dealt damage to enemy
        self.enemy.set_health(enemy_health)
        self.var_enemy_health.set(str(enemy_health))

        # apply taken damage to player
        self.player.set_health(player_health)
        self.var_player_health.set(str(player_health))

        # update the health in the main game window
        self.game_object.render_stats(self.game_object.cnv_stats)

        if player_health <= 0:
            self.tk_parent.destroy()
            messagebox.showerror("You died!", "You died in combat! Press the button to exit.")
            sys.exit()
        elif enemy_health <= 0:
            if self.enemy.get_name() == "Dracula":
                self.tk_parent.destroy()
                messagebox.showinfo(
                    "You won!",
                    "You killed Dracula! Congratulations on beating the game. Press the button to exit."
                )
                sys.exit()
            else:
                self.tk_parent.destroy()
                messagebox.showinfo("You won!", "You beat the enemy in combat! Press the button to continue.")


# purpose: handles main gameplay loop, rendering, etc
class GUIGame:
    def __init__(self, tk_parent, name):
        # window root object
        self.tk_parent = tk_parent
        # player's name
        self.name = name

        # un-hide the window
        self.tk_parent.deiconify()

        # game object setup
        self.player = entities.EntityPlayer(name)
        self.room_manager = navigation.RoomManager()
        self.rooms = self.room_manager.get_rooms()

        # window setup - populate frames
        self.frm_container = tk.Frame(self.tk_parent)
        self.frm_stats = tk.Frame(self.frm_container, highlightbackground="black", highlightthickness=1)
        self.frm_map = tk.Frame(self.frm_container, highlightbackground="black", highlightthickness=1)
        self.frm_controls = tk.Frame(self.frm_container)
        self.frm_log = tk.Frame(self.frm_container, highlightbackground="black", highlightthickness=1)

        # section titles
        lbl_stats = ttk.Label(self.frm_container, text="Stats", font=("Arial", 22))
        lbl_map = ttk.Label(self.frm_container, text="Map", font=("Arial", 22))
        lbl_log = ttk.Label(self.frm_container, text="Log", font=("Arial", 22))

        # control buttons
        btn_north = ttk.Button(self.frm_controls, text="↑", command=lambda direction="N": self.move(direction))
        btn_east = ttk.Button(self.frm_controls, text="→", command=lambda direction="E": self.move(direction))
        btn_south = ttk.Button(self.frm_controls, text="↓", command=lambda direction="S": self.move(direction))
        btn_west = ttk.Button(self.frm_controls, text="←", command=lambda direction="W": self.move(direction))

        # populate canvases - TODO dynamic resizing?
        self.cnv_stats = tk.Canvas(self.frm_stats, width=200, height=300)
        self.cnv_map = tk.Canvas(self.frm_map, width=300, height=300, bg="black")

        # log textbox
        self.txt_log = tk.Text(self.frm_log)
        self.txt_log.configure(state="disabled")
        self.txt_log.grid(row=0, column=0)

        # start populating grids - labels on container, canvases on respective frames
        lbl_stats.grid(row=0, column=0)
        lbl_map.grid(row=0, column=1)
        lbl_log.grid(row=4, column=0, columnspan=2)

        btn_north.grid(row=0, column=2)
        btn_west.grid(row=1, column=0)
        btn_east.grid(row=1, column=3)
        btn_south.grid(row=1, column=2)

        self.cnv_stats.grid(row=0, column=0)
        self.cnv_map.grid(row=0, column=0)

        # lastly populate the frames on the window's grid
        self.frm_container.grid(row=0, column=0)
        self.frm_stats.grid(row=1, column=0)
        self.frm_map.grid(row=1, column=1)
        self.frm_controls.grid(row=3, column=0, columnspan=2)
        self.frm_log.grid(row=5, column=0, columnspan=2)

        # set the starting room
        self.player.set_current_room(self.rooms["room_entrance"])
        self.insert_log_text(f"{self.player.get_name()} is in {self.player.get_current_room().get_name()}\n")

        # bind keyboard keys to movement
        self.tk_parent.bind("w", lambda event, direction="N": self.move(direction))
        self.tk_parent.bind("d", lambda event, direction="E": self.move(direction))
        self.tk_parent.bind("s", lambda event, direction="S": self.move(direction))
        self.tk_parent.bind("a", lambda event, direction="W": self.move(direction))

        # render the screen
        self.render()

    # purpose: meta-function that calls the other rendering steps
    def render(self):
        self.render_map(self.cnv_map)
        self.render_stats(self.cnv_stats)

    # purpose: renders the stats display
    def render_stats(self, canvas):
        # clear the canvas
        canvas.delete(tk.ALL)

        canvas.create_text(100, 20, text="Name", font=("Arial", 18))
        canvas.create_text(100, 45, text=str(self.player.get_name()), font=("Arial", 16))
        canvas.create_text(100, 70, text="Health", font=("Arial", 18))
        canvas.create_text(100, 95, text=str(self.player.get_health()), font=("Arial", 16))

    # purpose: renders the map with canvas rects
    def render_map(self, canvas):
        # clear the canvas
        canvas.delete(tk.ALL)

        valid_moves = self.player.get_current_room().get_valid_moves()

        # render the current room - TODO dynamic resizing?
        canvas.create_rectangle(50, 50, 250, 250, fill="white", outline="black")
        canvas.create_text(150, 150, text=self.player.get_current_room().get_name(), font=("Arial", 18))
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

    # purpose: adds text to the log window
    def insert_log_text(self, text):
        self.txt_log.configure(state="normal")
        self.txt_log.insert(tk.END, text)
        self.txt_log.see(tk.END)
        self.txt_log.configure(state="disabled")

    # purpose: checks the player's current room for enemies and initiates a battle if present
    def check_enemies(self):
        room_enemies = self.player.get_current_room().get_enemies()
        if len(room_enemies) != 0:
            self.insert_log_text(f"\n{self.player.get_name()} encountered a {room_enemies[0].get_name()}!\n")
            battle_window = tk.Toplevel()
            # only allow user to interact with battle window
            battle_window.grab_set()
            # force focus on the window to start the grab set
            battle_window.focus()
            # pass up the current object so battle window can update stats
            battle = GUIBattle(battle_window, self, room_enemies[0])
            room_enemies.remove(room_enemies[0])

    # purpose: checks the player's current room for healing items and applies them if present
    def check_healing_items(self):
        room_items = self.player.get_current_room().get_items()
        if len(room_items) != 0:
            for i in room_items:
                # add healing item amount to player's health
                current_health = self.player.get_health()
                self.player.set_health(current_health + i.get_heal_amount())
                self.insert_log_text(f"\n{self.player.get_name()} found a {i.get_name()}! +{i.get_heal_amount()}HP!\n")
                # remove the item
                room_items.remove(i)

    # purpose: handles player movement, checks to make sure a move is valid and executes it
    def move(self, direction):
        # updates the player's location to the room in the specified direction
        if direction == "N":
            # fetch the list of rooms adjacent to the current one
            valid_moves = self.player.get_current_room().get_valid_moves()
            if valid_moves[0] is None:
                self.insert_log_text("\nCan't go that way.\n")
            else:
                # update the player's current room if the move is valid
                self.player.set_current_room(valid_moves[0])
                self.insert_log_text(f"\n{self.player.get_name()} is in {self.player.get_current_room().get_name()}\n")
                # check for any healing items in the room
                self.check_healing_items()
                # check for enemies
                self.check_enemies()

        elif direction == "E":
            valid_moves = self.player.get_current_room().get_valid_moves()
            if valid_moves[1] is None:
                self.insert_log_text("\nCan't go that way.\n")
            else:
                self.player.set_current_room(valid_moves[1])
                self.insert_log_text(f"\n{self.player.get_name()} is in {self.player.get_current_room().get_name()}\n")
                self.check_healing_items()
                self.check_enemies()

        elif direction == "S":
            valid_moves = self.player.get_current_room().get_valid_moves()
            if valid_moves[2] is None:
                self.insert_log_text("\nCan't go that way.\n")
            else:
                self.player.set_current_room(valid_moves[2])
                self.insert_log_text(f"\n{self.player.get_name()} is in {self.player.get_current_room().get_name()}\n")
                self.check_healing_items()
                self.check_enemies()

        elif direction == "W":
            valid_moves = self.player.get_current_room().get_valid_moves()
            if valid_moves[3] is None:
                self.insert_log_text("\nCan't go that way.\n")
            else:
                self.player.set_current_room(valid_moves[3])
                self.insert_log_text(f"\n{self.player.get_name()} is in {self.player.get_current_room().get_name()}\n")
                self.check_healing_items()
                self.check_enemies()

        self.render()


# purpose: initial GUI object, primarily handles the start screen and instantiating the main gameplay GUI
class GUIMain:
    def __init__(self, tk_parent):
        # hide the root window and spawn a new window for the start screen
        tk_parent.withdraw()
        tk_start_window = tk.Toplevel()

        # if the user hits the X button, call on_close which will exit the application entirely
        tk_start_window.protocol("WM_DELETE_WINDOW", on_close_exit)
        tk_parent.protocol("WM_DELETE_WINDOW", on_close_exit)

        # user's name
        var_name = tk.StringVar()
        # user's age
        var_age = tk.StringVar()

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

        lbl_age = ttk.Label(frm_container, text="Please enter your age:", font=("Arial", 12))
        ent_age = ttk.Entry(frm_container, textvariable=var_age)

        btn_quit = ttk.Button(frm_container, text="Quit", command=sys.exit)
        btn_start = ttk.Button(frm_container, text="Start",
                               command=lambda: self.start_game(var_name.get(), var_age.get(),
                                                               tk_start_window, tk_parent))

        # insert widgets into the grid, span columns to center them relative to the buttons
        lbl_welcome.grid(row=0, columnspan=2)
        msg_intro.grid(row=1, columnspan=2)
        msg_tip.grid(row=2, columnspan=2)
        lbl_name.grid(row=3, columnspan=2)
        ent_name.grid(row=4, columnspan=2, sticky="nesw")
        lbl_age.grid(row=5, columnspan=2)
        ent_age.grid(row=6, columnspan=2, sticky="nesw")
        btn_quit.grid(row=7, column=0, sticky="nesw")
        btn_start.grid(row=7, column=1, sticky="nesw")

        # pack the frame containing all widgets with some padding
        frm_container.pack(padx=20, pady=20)

    # purpose: instantiates the main gameplay GUI
    def start_game(self, name, age, tk_start_window, tk_parent):
        # check name validity
        if name == "" or name.startswith(" "):
            messagebox.showerror("Error", "Name must not be empty, and must not start with a space.")
            pass
        else:
            # check age
            try:
                age_int = int(age)
                if age_int < 13:
                    messagebox.showerror("Error", "You must be over 13 to play this game.")
                    sys.exit()
                # hide the start window
                tk_start_window.withdraw()
                # create the main game window
                game_window = GUIGame(tk_parent, name)
            except ValueError:
                messagebox.showerror("Error", "Age must be a number.")
                pass
