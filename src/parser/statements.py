# Stmt Classes
class Exit:
    def __init__(self, exprType):
        self.exprType = exprType

class DefFunc:
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

class Let:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
class Return:
    def __init__(self, value):
        self.value = value

class Call:
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

class Log:
    def __init__(self, value):
        self.value = value

class If:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class dbgstmt:
    def __init__(self, cmd):
        self.cmd = cmd

class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Inc:
    def __init__(self, variable, value=1):
        self.variable = variable
        self.value = value