import sys

from generator.py import libraries
import parser.expressions as expressions
import parser.statements as statements
from main import FileUtils

std = libraries.Std()

class CodeGenerator:
    def __init__(self, node, generator):
        self.generator = generator
        self.node = node
    
    @staticmethod
    def build_start_of_file():
        FileUtils.append_to_file("import sys\n")
        FileUtils.append_to_file("\n# START LIBRARIES\n")

        std.build()

        FileUtils.append_to_file("# END LIBRARIES\n")
        FileUtils.append_to_file("\ndef __program__():\n")
        FileUtils.append_to_file("    global exit_code\n")
        FileUtils.append_to_file("    # Start of the user's program\n")

    @staticmethod
    def build_end_of_file():
        FileUtils.append_to_file("\nexit_code = 0\n")
        FileUtils.append_to_file("__program__() # Execute the program\n")
        FileUtils.append_to_file("Std.exit(exit_code)\n")

        

    @staticmethod
    def get_expr_value(expr):
        if isinstance(expr, expressions.StringExpr):
            return f'"{expr.value}"'
        elif isinstance(expr, expressions.NumberExpr):
            return expr.value
        elif isinstance(expr, expressions.VariableExpr):
            return expr.name
        elif isinstance(expr, expressions.BoolExpr):
            return "True" if expr.value else "False"
        elif isinstance(expr, expressions.BinaryopExpr):
            left = CodeGenerator.get_expr_value(expr.left)
            right = CodeGenerator.get_expr_value(expr.right)
            return f"({left} {expr.operator} {right})"
        elif isinstance(expr, expressions.CallExpr):
            params = ', '.join([CodeGenerator.get_expr_value(param) for param in expr.parameters])
            return expr.name + "(" + params + ")"
        else:
            print(f"Error: Unsupported expression type '{type(expr).__name__}'")
            sys.exit(1)

    def push(self):
        if isinstance(self.node, statements.Let):
            name = self.node.name
            expr = self.node.value
            value = CodeGenerator.get_expr_value(expr)
            self.generator.emit(f"{name} = {value}\n")

        elif isinstance(self.node, statements.DefFunc):
            name = self.node.name
            params = ', '.join(self.node.parameters)
            self.generator.emit(f"def {name}({params}):\n")
            self.generator.indent_push()

            for stmt in self.node.body:
                node = CodeGenerator(stmt, self.generator)
                node.push()

            self.generator.indent_pop()
        
        elif isinstance(self.node, statements.Exit):
            expr = self.node.exprType
            value = CodeGenerator.get_expr_value(expr)
            self.generator.emit(f"exit_code = {value}\n")
            self.generator.emit("Std.exit(exit_code)\n")
        
        elif isinstance(self.node, statements.Return):
            value = CodeGenerator.get_expr_value(self.node.value)
            self.generator.emit(f"return {value}\n")

        elif isinstance(self.node, statements.Call):
            name = self.node.name
            params = ', '.join([CodeGenerator.get_expr_value(param) for param in self.node.parameters])
            self.generator.emit(f"{name}({params})\n")

        elif isinstance(self.node, statements.Log):
            value = CodeGenerator.get_expr_value(self.node.value)
            self.generator.emit(f"print({value})\n")

        elif isinstance(self.node, statements.If):
            condition = CodeGenerator.get_expr_value(self.node.condition)
            self.generator.emit(f"if {condition}:\n")
            self.generator.indent_push()

            for stmt in self.node.then_branch:
                node = CodeGenerator(stmt, self.generator)
                node.push()

            self.generator.indent_pop()
            if self.node.else_branch:
                self.generator.emit("else:\n")
                self.generator.indent_push()
                for stmt in self.node.else_branch:
                    node = CodeGenerator(stmt, self.generator)
                    node.push()
                self.generator.indent_pop()

        elif isinstance(self.node, statements.dbgstmt):
            print(self.node.cmd)
            if self.node.cmd == "exitcode":
                std.exitdbg = True

        elif isinstance(self.node, statements.While):
            condition = CodeGenerator.get_expr_value(self.node.condition)
            self.generator.emit(f"while {condition}:\n")
            self.generator.indent_push()

            for stmt in self.node.body:
                node = CodeGenerator(stmt, self.generator)
                node.push()

            self.generator.indent_pop()
        
        elif isinstance(self.node, statements.Inc):
            variable = self.node.variable
            value = CodeGenerator.get_expr_value(self.node.value)
            self.generator.emit(f"{variable} += {value}\n")