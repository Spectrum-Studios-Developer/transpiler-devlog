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
    
class BoolExpr:
    def __init__(self, value):
        self.value = value

class ArrayExpr:
    def __init__(self, elements):
        self.elements = elements

class StructExpr:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields

class BinaryopExpr:
    BINDING_POWER = {
        "||": (1, 2),
        "&&": (3, 4),

        "==": (5, 6),
        "!=": (5, 6),

        "<": (7, 8),
        ">": (7, 8),

        "+": (10, 11),
        "-": (10, 11),

        "*": (20, 21),
        "/": (20, 21),
    }

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class CallArrayExpr:
    def __init__(self, array, index):
        self.array = array
        self.index = index

class CallExpr:
    def __init__ (self, name, parameters):
        self.name = name
        self.parameters = parameters
    
class CallStructExpr:
    def __init__(self, struct, field):
        self.struct = struct
        self.field = field