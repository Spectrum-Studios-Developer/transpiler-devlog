import main

# Stmt Classes
class Exit:
    def __init__(self, exprType):
        self.exprType = exprType

# Expression Classes
class NumberExpr:
    def __init__(self, value):
        self.value = value

class StringExpr:
    def __init__(self, value):
        self.value = value

# Statemnt Handler
class Stmt:
    def __init__(self, node, generator):
        self.generator = generator
        self.node = node

    def push(self):
        if isinstance(self.node, Exit):
            if self.node.exprType is None:
                self.generator.emit('print(f"Exited with code {repr(exit_code)}")\n')
                return

            expr = self.node.exprType

            if isinstance(expr, StringExpr):
                value = f'"{expr.value}"'
            elif isinstance(expr, NumberExpr):
                value = expr.value
            else:
                raise Exception("Unsupported expression type")

            self.generator.emit(f"exit_code = {value}\n")
            self.generator.emit("print(f'Exited with code {exit_code}')\n")

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
        

        
    # Parsing Functions  
    def parse_program(self):
        statements = []

        while self.peek() is not None:
            statements.append(self.parse_statement())

        return statements
    
    def parse_statement(self):
        token = self.peek()

        if token == "exit":
            return self.parse_exit()

        raise SyntaxError(f"Unknown statement: {token}")

    def parse_expression(self):
        token = self.peek()

        if token.isdigit():
            self.advance()
            return NumberExpr(token)
        
        if token == '"':
            self.consume('"')
            value = ""
            while self.peek() != '"':
                value += self.advance()
            self.consume('"')
            return StringExpr(value)
        
        raise SyntaxError(f"Unknown expression: {token}")
    
        # Parsing individual statements
    def parse_exit(self):
        self.consume("exit")
        self.consume("(")

        value = self.parse_expression()

        self.consume(")")
        self.consume(";")

        return Exit(value)