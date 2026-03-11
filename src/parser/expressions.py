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
    BINARY_OPERATORS = {"+", "-", "*", "/", "=="}
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class CallExpr:
    def __init__ (self, name, parameters):
        self.name = name
        self.parameters = parameters