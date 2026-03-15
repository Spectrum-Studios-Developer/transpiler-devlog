from . import expressions
from . import statements
import sys

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
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
            print(f"Syntax Error: Expected '{expected}', got '{token}'")
            sys.exit(1)

    def parse_program(self):
        stmts = []
        while self.peek() is not None:
            stmts.append(self.parse_statement())
        return stmts
    



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
        elif token == "#":
            return self.parse_dbgstmt()
        elif token == "while":
            return self.parse_while()
        elif token == "inc":
            return self.parse_inc()
        elif token == "update":
            return self.parse_update()
        
        print(f"Syntax Error: Unknown statement '{token}'")
        sys.exit(1)






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

        if token is None:
            print("Syntax Error: Unexpected end of input")
            sys.exit(1)

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
        
        if token == "true":
            self.advance()
            return expressions.BoolExpr(True)
        if token == "false":
            self.advance()
            return expressions.BoolExpr(False)
        
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

        print(f"Syntax Error: Unexpected token '{token}'")
        sys.exit(1)
    
    def parse_exit(self):
        self.consume("exit")
        self.consume(",")
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
            if self.peek() is None:
                print(f"Syntax Error: Unclosed '{{' in function '{name}'")
                sys.exit(1)
            body.append(self.parse_statement())
        
        self.consume("}")
        return statements.DefFunc(name, parameters, body)
    
    def parse_let(self):
        self.consume("let")
        name = self.advance()
        self.consume(",")
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
            if self.peek() is None:
                print("Syntax Error: Unclosed '{' in if statement")
                sys.exit(1)
            then_branch.append(self.parse_statement())

        self.consume("}")
        if self.peek() == "else":
            self.consume("else")
            if self.peek() == "if":
                else_branch = [self.parse_if()]
                stmt = statements.If(condition, then_branch)
                stmt.else_branch = else_branch
                return stmt
            self.consume("{")
            else_branch = []
            while self.peek() != "}":
                if self.peek() is None:
                    print("Syntax Error: Unclosed '{' in else statement")
                    sys.exit(1)
                else_branch.append(self.parse_statement())
            self.consume("}")
            stmt = statements.If(condition, then_branch)
            stmt.else_branch = else_branch
            return stmt
        return statements.If(condition, then_branch)

    def parse_dbgstmt(self):
        self.consume("#")
        cmd = self.advance()
        self.consume(";")
        return statements.Dbgstmt(cmd)

    def parse_while(self):
        self.consume("while")
        self.consume("(")
        condition = self.parse_expr()
        self.consume(")")
        self.consume("{")

        body = []
        while self.peek() != "}":
            if self.peek() is None:
                print("Syntax Error: Unclosed '{' in while statement")
                sys.exit(1)
            body.append(self.parse_statement())

        self.consume("}")
        return statements.While(condition, body)

    def parse_inc(self):
        self.consume("inc")
        variable = self.advance()
        self.consume(",")
        value = self.parse_expr()
        self.consume(";")
        return statements.Inc(variable, value)
    
    def parse_update(self):
        self.consume("update")
        variable = self.advance()
        self.consume(",")
        value = self.parse_expr()
        self.consume(";")
        return statements.Update(variable, value)
    