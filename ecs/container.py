class Container:
    instance = None

    def __init__(self):
        Container.instance = self
        self.systems = []
        self.entities = []
        self.index = 0

    def add_system(self, system):
        self.systems.append(system)

    def add_entity(self, entity):
        self.entities.append(entity)
        self.index += 1
        entity.index = self.index


    def update(self):
        for system in self.systems:
            system.update(self.entities)
