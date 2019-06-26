from ecs.entity import Entity


class TestEntity:
    def test_getter_gets_set_values(self):
        e = Entity()
        expected = IntComponent(13)
        e.set(expected)

        actual = e.get(IntComponent)
        assert actual == expected

    def test_set_overwrites_previous_value(self):
        e = Entity()
        expected = IntComponent(13)

        e.set(IntComponent(1888))
        e.set(expected)

        actual = e.get(IntComponent)
        assert actual == expected

    def test_has_returns_true_is_component_exists(self):
        # Note: doesn't work for subclasses of the component
        e = Entity(IntComponent(77))
        assert e.has(IntComponent) is True
        assert e.has(StringComponent) is False


class IntComponent:
    def __init__(self, value):
        self.value = value


class StringComponent:
    def __init__(self, value):
        self.value = str(value)