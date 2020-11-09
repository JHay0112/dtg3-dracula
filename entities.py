class EntityPlayer:
    name = ""
    health = 100
    current_room = None

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

    def get_current_room(self):
        return self.current_room

    def set_current_room(self, current_room):
        self.current_room = current_room


class EntityHealItem:
    name = ""
    heal_amount = 0

    def __init__(self, name, heal_amount):
        self.name = name
        self.heal_amount = heal_amount

    def get_name(self):
        return self.name

    def get_heal_amount(self):
        return self.heal_amount
