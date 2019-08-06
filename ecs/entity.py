class Entity:
    all_entities = []

    def __init__(self, *components):
        self.components = {}

        Entity.all_entities.append(self)

        for component in components:
            self.set(component)

    def set(self, component):
        key = type(component)
        self.components[key] = component

    def get(self, component):
        try:
            return self.components[component]
        except KeyError:
            pass

    def has(self, component):
        try:
            return self.get(component) is not None
        except KeyError:
            pass
