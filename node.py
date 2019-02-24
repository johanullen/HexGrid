
class Node:
    def __init__(self, value, *, data=None):
        if isinstance(value, Node):
            self.value = value.value
        else:
            self.value = value
        self.data = data

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.value == other.value
        else:
            return self.value == other

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        if isinstance(other, Node):
            return self.value > other.value
        else:
            return self.value > other

    def __ge__(self, other):
        return self == other or self > other

    def __lt__(self, other):
        return not self >= other

    def __le__(self, other):
        return not self > other

    def __neg__(self):
        return Node(-self.value, data=self.data)

    def __add__(self, other):
        if isinstance(other, Node):
            return Node(self.value + other.value, data=self.data)
        else:
            return Node(self.value + other, data=self.data)

    def __sub__(self, other):
        return self + (-other)

    def __iadd__(self, other):
        if isinstance(other, Node):
            self.value += other.value
        else:
            self.value += other
        return self

    def __isub__(self, other):
        self += -other
        return self

    def __index__(self):
        return self.value

    def __hash__(self):
        return self.value

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return self.__str__()