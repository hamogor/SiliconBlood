class ComCreature:
    def __init__(self, name_instance, hp=10, death_function=None):
        self.name_instance = name_instance
        self.max_hp = hp
        self.hp = hp
        self.death_function = death_function

    def take_damage(self, damage):
        self.hp -= damage
        print(self.name_instance + " takes " + str(damage) + " damage")

        if self.hp <= 0:
            if self.death_function:
                self.death_function(self.owner)
