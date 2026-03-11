import main

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

class CallExpr:
    def __init__ (self, name, parameters):
        self.name = name
        self.parameters = parameters

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
        elif isinstance(expr, CallExpr):
            params = ', '.join([Stmt.get_expr_value(param) for param in expr.parameters])
            return expr.name + "(" + params + ")"
        else:
            raise Exception("Unsupported expression type")

    def push(self): # This is where we handle the code generation for each statement
        # Declarative Statements
        if isinstance(self.node, Let):
            name = self.node.name
            expr = self.node.value

            value = Stmt.get_expr_value(expr)

            self.generator.emit(f"{name} = {value}\n")

        if isinstance(self.node, DefFunc):
            name = self.node.name
            params = ', '.join(self.node.parameters)
            self.generator.emit(f"def {name}({params}):\n")
            self.generator.indent_push()

            for stmt in self.node.body:
                node = Stmt(stmt, self.generator)
                node.push()

            self.generator.indent_pop()
        
        # Control Flow Statements
        if isinstance(self.node, Exit):
            expr = self.node.exprType
            value = Stmt.get_expr_value(expr)

            self.generator.emit(f"exit_code = {value}\n")
            self.generator.emit("print(f'Exited with code {repr(exit_code)}')\n")
        
        if isinstance(self.node, Return):
            value = Stmt.get_expr_value(self.node.value)
            self.generator.emit(f"return {value}\n")

        if isinstance(self.node, Call):
            name = self.node.name
            params = ', '.join([Stmt.get_expr_value(param) for param in self.node.parameters])
            self.generator.emit(f"{name}({params})\n")

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
        if token == "return":
            return self.parse_return()
        if token == "call":
            return self.parse_call()

        raise SyntaxError(f"Unknown statement: {token}")

    # Parse Expr
    def parse_expression(self):
        token = self.peek()

        if token == "(":
            self.consume("(")
            expr = self.parse_expression()
            self.consume(")")
            print("Compiler Warning: Grouped expressions are ignored; consider removing parentheses?")
            return expr

        if token.isdigit():
            self.advance()
            return NumberExpr(token)
    
        if token.startswith('"') or token.startswith("'"):
            self.advance()
            return StringExpr(token[1:-1])
        
        if token.isidentifier():
            name = self.advance()

            if self.peek() == "(":
                self.consume("(")

                parameters = []

                if self.peek() != ")":
                    parameters.append(self.parse_expression())

                    while self.peek() == ",":
                        self.consume(",")
                        parameters.append(self.parse_expression())
                
                self.consume(")")
                return CallExpr(name, parameters)
            return VariableExpr(name)

        raise SyntaxError(f"Unknown expression: {token}")
    
    # Parsing individual statements
    def parse_exit(self):
        self.consume("exit")

        value = self.parse_expression()

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

        return DefFunc(name, parameters, body)
    
    def parse_let(self):
        self.consume("let")

        name = self.advance()

        self.consume("=")

        value = self.parse_expression()

        self.consume(";")

        return Let(name, value)
    
    def parse_return(self):
        self.consume("return")

        value = self.parse_expression()

        self.consume(";")

        return Return(value)
    
    def parse_call(self):
        self.consume("call")

        name = self.advance()

        parameters = []

        self.consume("(")

        if self.peek() != ")":
             parameters.append(self.parse_expression())

             while self.peek() == ",":
                self.consume(",")
                parameters.append(self.parse_expression())   
        self.consume(")")

        self.consume(";")

        return Call(name, parameters)