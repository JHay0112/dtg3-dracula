class EntityPlayer:
    name = ""
    health = 100
    inventory = []
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

    def get_inventory(self):
        return self.inventory

    def get_current_room(self):
        return self.current_room

    def set_current_room(self, current_room):
        self.current_room = current_room
