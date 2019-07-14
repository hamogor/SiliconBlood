import pysnooper
class Container:
    instance = None

    def __init__(self):
        Container.instance = self
        self.systems = []
        self.entities = []

    def add_system(self, system):
        self.systems.append(system)

    def add_entity(self, entity):
        self.entities.append(entity)

    def update(self):
        for s in self.systems:
            s.update(self.entities)
