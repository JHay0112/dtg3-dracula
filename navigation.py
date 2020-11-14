import random
import entities


# defines everything in a room and the other places it can go
class Room:
    def __init__(self, name):
        # instance variables
        self.name = name
        # list of EntityHealItem objects
        self.items = []
        # list of EntityEnemy objects
        self.enemies = []
        # list of Room objects in order of N-E-S-W.
        self.valid_moves = []

    def get_name(self):
        return self.name

    def get_valid_moves(self):
        return self.valid_moves

    def set_valid_moves(self, valid_moves):
        self.valid_moves = valid_moves

    def get_items(self):
        return self.items

    def add_item(self, item):
        self.items.append(item)

    def get_enemies(self):
        return self.enemies

    def add_enemy(self, enemy):
        self.enemies.append(enemy)


class RoomManager:
    # class variables
    # number of healing items and enemies to add to the map
    NUM_ITEMS = 3
    NUM_ENEMIES = 2

    # every room in the map
    Rooms = {
        "room_entrance": Room("Entrance Hall"),
        "room_mainhall": Room("Main Hall"),
        "room_backhall": Room("Back Hall"),
        "room_passage": Room("Passage"),
        "room_scullery": Room("Scullery"),
        "room_cellar": Room("Cellar"),
        "room_kitchen": Room("Kitchen"),
        "room_pantry": Room("Pantry"),
        "room_sunroom": Room("Sun Room"),
        "room_westhall": Room("West Hall"),
        "room_toilet": Room("Toilet"),
        "room_westtower": Room("West Tower"),
        "room_drawingroom": Room("Drawing Room"),
        "room_library": Room("Library"),
        "room_bedroom": Room("Bedroom"),
        "room_dressingroom": Room("Dressing Room"),
        "room_bathroom": Room("Bathroom"),
        "room_eastcorridor": Room("East Corridor"),
        "room_lounge": Room("Lounge"),
        "room_easttower": Room("East Tower")
    }

    def __init__(self):
        # start initializing the room states - valid moves are in order N-E-S-W, none = no moves
        self.Rooms["room_entrance"].set_valid_moves([
            self.Rooms["room_mainhall"],
            None,
            None,
            None
        ])
        self.Rooms["room_mainhall"].set_valid_moves([
            self.Rooms["room_backhall"],
            self.Rooms["room_eastcorridor"],
            self.Rooms["room_entrance"],
            self.Rooms["room_westhall"]
        ])
        self.Rooms["room_backhall"].set_valid_moves([
            self.Rooms["room_sunroom"],
            self.Rooms["room_passage"],
            self.Rooms["room_mainhall"],
            None
        ])
        self.Rooms["room_passage"].set_valid_moves([
            self.Rooms["room_kitchen"],
            self.Rooms["room_scullery"],
            None,
            self.Rooms["room_backhall"]
        ])
        self.Rooms["room_scullery"].set_valid_moves([
            None,
            None,
            self.Rooms["room_cellar"],
            self.Rooms["room_passage"]
        ])
        self.Rooms["room_cellar"].set_valid_moves([
            self.Rooms["room_scullery"],
            None,
            None,
            None
        ])
        self.Rooms["room_kitchen"].set_valid_moves([
            None,
            self.Rooms["room_pantry"],
            self.Rooms["room_passage"],
            None
        ])
        self.Rooms["room_pantry"].set_valid_moves([
            None,
            None,
            None,
            self.Rooms["room_kitchen"]
        ])
        self.Rooms["room_sunroom"].set_valid_moves([
            None,
            None,
            self.Rooms["room_backhall"],
            None
        ])
        self.Rooms["room_westhall"].set_valid_moves([
            self.Rooms["room_toilet"],
            self.Rooms["room_mainhall"],
            None,
            self.Rooms["room_westtower"]
        ])
        self.Rooms["room_toilet"].set_valid_moves([
            None,
            None,
            self.Rooms["room_westhall"],
            None
        ])
        self.Rooms["room_westtower"].set_valid_moves([
            self.Rooms["room_bedroom"],
            self.Rooms["room_westhall"],
            self.Rooms["room_drawingroom"],
            None
        ])
        self.Rooms["room_drawingroom"].set_valid_moves([
            self.Rooms["room_westtower"],
            self.Rooms["room_library"],
            None,
            None
        ])
        self.Rooms["room_library"].set_valid_moves([
            None,
            None,
            None,
            self.Rooms["room_drawingroom"]
        ])
        self.Rooms["room_bedroom"].set_valid_moves([
            self.Rooms["room_dressingroom"],
            None,
            self.Rooms["room_westtower"],
            None
        ])
        self.Rooms["room_dressingroom"].set_valid_moves([
            None,
            self.Rooms["room_bathroom"],
            self.Rooms["room_bedroom"],
            None
        ])
        self.Rooms["room_bathroom"].set_valid_moves([
            None,
            None,
            None,
            self.Rooms["room_dressingroom"]
        ])
        self.Rooms["room_eastcorridor"].set_valid_moves([
            None,
            None,
            self.Rooms["room_lounge"],
            self.Rooms["room_mainhall"]
        ])
        self.Rooms["room_lounge"].set_valid_moves([
            self.Rooms["room_eastcorridor"],
            self.Rooms["room_easttower"],
            None,
            None
        ])
        self.Rooms["room_easttower"].set_valid_moves([
            None,
            None,
            None,
            self.Rooms["room_lounge"]
        ])

        # add healing items to the map
        for i in range(0, self.NUM_ITEMS):
            # select a random room, and add a +10 HP health pack
            room = random.choice(list(self.Rooms.values()))
            room_items = room.get_items()
            # skip if there's already an item here
            if len(room_items) != 0:
                continue
            room.add_item(entities.EntityHealItem("Health Pack", 10))

        # add enemies
        for i in range(0, self.NUM_ENEMIES):
            # select a random room, and add an enemy
            room = random.choice(list(self.Rooms.values()))
            room_enemies = room.get_enemies()
            # skip if there's already an item here
            if len(room_enemies) != 0:
                continue
            room.add_enemy(entities.EntityEnemy("Vampire"))

    def get_rooms(self):
        return self.Rooms
