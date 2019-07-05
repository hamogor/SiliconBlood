class Container:
    instance = None

    def __init__(self):
        Container.instance = self
        self._systems = []
        self._entities = []

    def add_system(self, system):
        self._systems.append(system)

    def add_entity(self, entity):
        self._entities.append(entity)

    def update(self):
        for s in self._systems:
            s.update(self._entities)
