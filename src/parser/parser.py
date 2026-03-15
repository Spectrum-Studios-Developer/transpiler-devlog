from . import expressions
from . import statements

class ParseError(Exception):
    def __init__(self, message, pos=None, token=None):
        self.pos = pos
        self.token = token
        super().__init__(message)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []

    def peek(self):
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def advance(self):
        token = self.peek()
        self.pos += 1
        return token

    def _context_snippet(self):
        start = max(0, self.pos - 2)
        end = min(len(self.tokens), self.pos + 3)
        snippet = self.tokens[start:end]
        marked = []
        for i, t in enumerate(snippet):
            marked.append(f">>>{t}<<<" if (start + i) == self.pos else t)
        return " ".join(marked)

    def _error(self, message, hint=None):
        token = self.peek()
        context = self._context_snippet()
        full = (
            f"\n[ParseError] at position {self.pos} (token: '{token}')\n"
            f"  Context : {context}\n"
            f"  Problem : {message}\n"
        )
        if hint:
            full += f"  Fix     : {hint}\n"
        self.errors.append(full)
        print(full)
        raise ParseError(full, pos=self.pos, token=token)

    def consume(self, expected):
        token = self.advance()
        if token != expected:
            self._error(
                f"Expected '{expected}', got '{token}'",
                hint=f"Insert '{expected}' before '{token}' at position {self.pos - 1}."
            )

    def parse_program(self):
        stmts = []
        while self.peek() is not None:
            try:
                stmts.append(self.parse_statement())
            except ParseError:
                self._sync()
        return stmts

    def _sync(self):
        sync_tokens = {"exit", "let", "func", "return", "call", "log", "if", "while", "inc", "update", "struct", "#"}
        while self.peek() is not None:
            if self.peek() == ";":
                self.advance()
                return
            if self.peek() in sync_tokens:
                return
            self.advance()

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
        elif token == "struct":
            return self.parse_struct()

        self._error(
            f"Unknown statement keyword '{token}'",
            hint=f"Valid statements: exit, let, func, return, call, log, if, while, inc, update, struct, #."
        )

    def parse_lvalue(self):
        name = self.advance()
        expr = expressions.VariableExpr(name)

        while True:
            if self.peek() == "[":
                self.consume("[")
                index = self.parse_expr()
                self.consume("]")
                expr = expressions.CallArrayExpr(expr, index)
            elif self.peek() == ".":
                self.consume(".")
                field = self.advance()
                expr = expressions.CallStructExpr(expr, field)
            else:
                break

        return expr

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
            self._error(
                "Unexpected end of input while parsing expression",
                hint="Check for unclosed parentheses, missing operands, or a trailing operator."
            )

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

        if token == "[":
            self.consume("[")
            elements = []
            if self.peek() != "]":
                elements.append(self.parse_expr())
                while self.peek() == ",":
                    self.consume(",")
                    elements.append(self.parse_expr())
            self.consume("]")
            return expressions.ArrayExpr(elements)

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

            if self.peek() == "[":
                self.consume("[")
                index = self.parse_expr()
                self.consume("]")
                return expressions.CallArrayExpr(expressions.VariableExpr(name), index)

            if self.peek() == ".":
                self.consume(".")
                field = self.advance()
                return expressions.CallStructExpr(expressions.VariableExpr(name), field)

            return expressions.VariableExpr(name)

        self._error(
            f"Unexpected token '{token}' in expression",
            hint="Expected a number, string, boolean, identifier, '(', or '[' to begin an expression."
        )

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
                self._error(
                    f"Unclosed '{{' in function '{name}'",
                    hint=f"Add a closing '}}' to end the body of function '{name}'."
                )
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
                self._error(
                    "Unclosed '{' in if statement",
                    hint="Add a closing '}' to end the if body."
                )
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
                    self._error(
                        "Unclosed '{' in else statement",
                        hint="Add a closing '}' to end the else body."
                    )
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
                self._error(
                    "Unclosed '{' in while statement",
                    hint="Add a closing '}' to end the while body."
                )
            body.append(self.parse_statement())

        self.consume("}")
        return statements.While(condition, body)

    def parse_inc(self):
        self.consume("inc")
        variable = self.parse_lvalue()
        self.consume(",")
        value = self.parse_expr()
        self.consume(";")
        return statements.Inc(variable, value)

    def parse_update(self):
        self.consume("update")
        variable = self.parse_lvalue()
        self.consume(",")
        value = self.parse_expr()
        self.consume(";")

        if isinstance(variable, expressions.CallStructExpr):
            struct_name = variable.struct.name
            field_name = variable.field
            return statements.StructFieldUpdate(struct_name, field_name, value)

        return statements.Update(variable, value)

    def parse_struct(self):
        self.consume("struct")
        name = self.advance()
        fields = []
        self.consume("{")

        while self.peek() != "}":
            if self.peek() is None:
                self._error(
                    f"Unclosed '{{' in struct definition '{name}'",
                    hint=f"Add a closing '}}' to end the struct '{name}'."
                )
            field = self.advance()
            self.consume(";")
            fields.append(field)

        self.consume("}")
        return statements.Struct(name, fields)