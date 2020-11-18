# name: entities.py
# author: Mitchell Ward
# purpose: contains classes for various game entities

# purpose: defines the player entity
class EntityPlayer:
    name = ""
    health = 100
    current_room = None

    def __init__(self, name):
        self.name = name

    # purpose: getter/setters
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_health(self):
        return self.health

    def set_health(self, health):
        self.health = health

    def get_current_room(self):
        return self.current_room

    def set_current_room(self, current_room):
        self.current_room = current_room


# purpose: defines the enemy entity
class EntityEnemy:
    name = ""
    health = 100

    def __init__(self, name, health):
        self.name = name
        self.health = health

    # purpose: getters/setters
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_health(self):
        return self.health

    def set_health(self, health):
        self.health = health


# purpose: defines an item that heals the player
class EntityHealItem:
    name = ""
    heal_amount = 0

    def __init__(self, name, heal_amount):
        self.name = name
        self.heal_amount = heal_amount

    # purpose: getters/setters
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_heal_amount(self):
        return self.heal_amount

    def set_heal_amount(self, amount):
        self.heal_amount = amount
