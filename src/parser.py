import main

# Stmt Classes
class Exit:
    def __init__(self, exprType):
        self.exprType = exprType

class Func:
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

class Let:
    def __init__(self, name, value):
        self.name = name
        self.value = value

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

# Statemnt Handler
class Stmt:
    def __init__(self, node, generator):
        self.generator = generator
        self.node = node

    @staticmethod
    def get_expr_value(expr):
        if isinstance(expr, StringExpr):
            return f'"{expr.value}"'
        elif isinstance(expr, NumberExpr):
            return expr.value
        elif isinstance(expr, VariableExpr):
            return expr.name
        else:
            raise Exception("Unsupported expression type")

    def push(self):
        if isinstance(self.node, Exit):
            if self.node.exprType is None:
                self.generator.emit('print(f"Exited with code {repr(exit_code)}")\n')
                return

            expr = self.node.exprType
            value = Stmt.get_expr_value(expr)

            self.generator.emit(f"exit_code = {value}\n")
            self.generator.emit("print(f'Exited with code {repr(exit_code)}')\n")
        
        if isinstance(self.node, Let):
            name = self.node.name
            expr = self.node.value

            value = Stmt.get_expr_value(expr)

            self.generator.emit(f"{name} = {value}\n")

        if isinstance(self.node, Func):
            name = self.node.name
            params = ', '.join(self.node.parameters)
            self.generator.emit(f"def {name}({params}):\n")
            self.generator.indent_push()

            for stmt in self.node.body:
                node = Stmt(stmt, self.generator)
                node.push()

            self.generator.indent_pop()

# Main parser class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    # Helper Functions
    def peek(self):
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def advance(self):
        token = self.peek()
        self.pos += 1
        return token

    def consume(self, expected):
        token = self.advance()
        if token != expected:
            raise SyntaxError(f"Expected {expected}, got {token}")

    # High Level Parsing Functions
    def parse_program(self):
        statements = []

        while self.peek() is not None:
            statements.append(self.parse_statement())

        return statements
    
    def parse_statement(self):
        token = self.peek()

        if token == "exit":
            return self.parse_exit()
        
        if token == "let":
            return self.parse_let()

        if token == "func":
            return self.parse_func()

        raise SyntaxError(f"Unknown statement: {token}")

    # Parse Expr
    def parse_expression(self):
        token = self.peek()

        if token.isdigit():
            self.advance()
            return NumberExpr(token)
    
        if token.startswith('"') or token.startswith("'"):
            self.advance()
            return StringExpr(token[1:-1])
        
        if token.isidentifier():
            name = self.advance()
            return VariableExpr(name)

        raise SyntaxError(f"Unknown expression: {token}")
    
    # Parsing individual statements
    def parse_exit(self):
        self.consume("exit")
        self.consume("(")

        value = self.parse_expression()

        self.consume(")")
        self.consume(";")

        return Exit(value)
    
    def parse_func(self):
        self.consume("func")

        name = self.advance()

        parameters = []

        self.consume("(")

        if self.peek() != ")":
             parameters.append(self.advance())

             while self.peek() == ",":
                self.consume(",")
                parameters.append(self.advance())   
        self.consume(")")
        
        self.consume("{")

        body = []

        while self.peek() != "}":
            body.append(self.parse_statement())
        
        self.consume("}")

        return Func(name, parameters, body)
    
    def parse_let(self):
        self.consume("let")

        name = self.advance()

        self.consume("=")

        value = self.parse_expression()

        self.consume(";")

        return Let(name, value)