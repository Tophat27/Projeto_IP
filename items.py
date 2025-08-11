# items.py
# Defines item classes and their effects.

class Item:
    def __init__(self, name):
        self.name = name

    def use(self, player):
        pass

class Boots(Item):
    def __init__(self):
        super().__init__("Boots")

    def use(self, player):
        player.hp = min(player.max_hp, player.hp + 20)  # +20 HP, capped at max

class Umbrella(Item):
    def __init__(self):
        super().__init__("Umbrella")

    def use(self, player):
        player.damage += 5  # +5 Damage