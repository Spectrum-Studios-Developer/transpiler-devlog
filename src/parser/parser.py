from turtle import left

import main
from . import expressions
from . import statements

# Statemnt Handler
class Stmt:
    def __init__(self, node, generator):
        self.generator = generator
        self.node = node

    @staticmethod
    def get_expr_value(expr):
        if isinstance(expr, expressions.StringExpr):
            return f'"{expr.value}"'
        elif isinstance(expr, expressions.NumberExpr):
            return expr.value
        elif isinstance(expr, expressions.VariableExpr):
            return expr.name
        elif isinstance(expr, expressions.BinaryopExpr):
            left = Stmt.get_expr_value(expr.left)
            right = Stmt.get_expr_value(expr.right)
            return f"({left} {expr.operator} {right})"
        elif isinstance(expr, expressions.CallExpr):
            params = ', '.join([Stmt.get_expr_value(param) for param in expr.parameters])
            return expr.name + "(" + params + ")"
        else:
            raise Exception("Unsupported expression type")

    def push(self): # This is where we handle the code generation for each statement
        # Declarative Statements
        if isinstance(self.node, statements.Let):
            name = self.node.name
            expr = self.node.value

            value = Stmt.get_expr_value(expr)

            self.generator.emit(f"{name} = {value}\n")

        if isinstance(self.node, statements.DefFunc):
            name = self.node.name
            params = ', '.join(self.node.parameters)
            self.generator.emit(f"def {name}({params}):\n")
            self.generator.indent_push()

            for stmt in self.node.body:
                node = Stmt(stmt, self.generator)
                node.push()

            self.generator.indent_pop()
        
        # Control Flow Statements
        if isinstance(self.node, statements.Exit):
            expr = self.node.exprType
            value = Stmt.get_expr_value(expr)

            self.generator.emit(f"exit_code = {value}\n")
            self.generator.emit("Std.exit(exit_code)\n")
        
        if isinstance(self.node, statements.Return):
            value = Stmt.get_expr_value(self.node.value)
            self.generator.emit(f"return {value}\n")

        if isinstance(self.node, statements.Call):
            name = self.node.name
            params = ', '.join([Stmt.get_expr_value(param) for param in self.node.parameters])
            self.generator.emit(f"{name}({params})\n")

        if isinstance(self.node, statements.Log):
            value = Stmt.get_expr_value(self.node.value)
            self.generator.emit(f"print({value})\n")
        if isinstance(self.node, statements.If):
            condition = Stmt.get_expr_value(self.node.condition)
            self.generator.emit(f"if {condition}:\n")
            self.generator.indent_push()

            for stmt in self.node.then_branch:
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
        elif token == "let":
            return self.parse_let()
        elif token == "func":
            return self.parse_func()
        elif token == "return":
            return self.parse_return()
        elif token == "call":
            return self.parse_call()
        elif token == "log":
            return self.parse_log()
        elif token == "if":
            return self.parse_if()

        raise SyntaxError(f"Unknown statement: {token}")

    # Parse Expr
    def parse_expr(self, min_bp=0):
        left = self.parse_primary()

        while True:
            op = self.peek()

            if op not in expressions.BinaryopExpr.BINDING_POWER:
                break

            lbp, rbp = expressions.BinaryopExpr.BINDING_POWER[op]

            if lbp < min_bp:
                break

            self.advance()
            right = self.parse_expr(rbp)

            left = expressions.BinaryopExpr(left, op, right)

        return left

    def parse_primary(self):
        token = self.peek()

        if token == "(":
            self.consume("(")
            expr = self.parse_expr()
            self.consume(")")
            return expr

        if token.isdigit():
            self.advance()
            return expressions.NumberExpr(token)
    
        if token.startswith('"') or token.startswith("'"):
            self.advance()
            return expressions.StringExpr(token[1:-1])
        
        if token.isidentifier():
            name = self.advance()

            if self.peek() == "(":
                self.consume("(")

                parameters = []

                if self.peek() != ")":
                    parameters.append(self.parse_expr())

                    while self.peek() == ",":
                        self.consume(",")
                        parameters.append(self.parse_expr())
                
                self.consume(")")
                return expressions.CallExpr(name, parameters)
            return expressions.VariableExpr(name)

        raise SyntaxError(f"Unknown expression: {token}")
    
    # Parsing individual statements
    def parse_exit(self):
        self.consume("exit")

        value = self.parse_expr()

        self.consume(";")

        return statements.Exit(value)
    
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

        return statements.DefFunc(name, parameters, body)
    
    def parse_let(self):
        self.consume("let")

        name = self.advance()

        self.consume("=")

        value = self.parse_expr()

        self.consume(";")

        return statements.Let(name, value)
    
    def parse_return(self):
        self.consume("return")

        value = self.parse_expr()

        self.consume(";")

        return statements.Return(value)
    
    def parse_call(self):
        self.consume("call")

        name = self.advance()

        parameters = []

        self.consume("(")

        if self.peek() != ")":
             parameters.append(self.parse_expr())

             while self.peek() == ",":
                self.consume(",")
                parameters.append(self.parse_expr())   
        self.consume(")")

        self.consume(";")

        return statements.Call(name, parameters)
    
    def parse_log(self):
        self.consume("log")
        value = self.parse_expr()
        self.consume(";")
        return statements.Log(value)
    
    def parse_if(self):
        self.consume("if")
        self.consume("(")
        condition = self.parse_expr()
        self.consume(")")
        self.consume("{")

        then_branch = []
        while self.peek() != "}":
            then_branch.append(self.parse_statement())
        self.consume("}")
        return statements.If(condition, then_branch)