# Expression Classes
class NumberExpr:
    def __init__(self, value):
        self.value = value

class StringExpr:
    def __init__(self, value):
        self.value = value

class VariableExpr:
    def __init__(self, name):
        self.name = name

class BinaryopExpr:
    BINDING_POWER = {
        "+": (10, 11),
        "-": (10, 11),

        "*": (20, 21),
        "/": (20, 21),

        "==": (5, 6),
        "!=": (5, 6),

        "<": (7, 8),
        ">": (7, 8),
    }
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class CallExpr:
    def __init__ (self, name, parameters):
        self.name = name
        self.parameters = parameters