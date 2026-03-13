import sys

import parser.expressions as expressions
import parser.statements as statements
import main

section_data = []

class CodeGenerator:
    def __init__(self, node, generator):
        self.generator = generator
        self.node = node
    
    @staticmethod
    def build_data():
        main.FileUtils.append_to_file("section .data\n\n")

    @staticmethod
    def build_text():
        main.FileUtils.append_to_file("\nsection .text\n")
        main.FileUtils.append_to_file("\nglobal main\n")
        # put extern functions here
        # functions
        main.FileUtils.append_to_file("\nmain:\n")

        

    @staticmethod
    def get_expr_value(expr, generator):
        if isinstance(expr, expressions.StringExpr):
            label = f'str_{generator.label_id}'
            generator.label_id += 1
            
            generator.emit(f'{label} db "{expr.value}", 0\n', type="data")
            generator.emit(f'lea rax, [{label}]\n', type="text")
        elif isinstance(expr, expressions.NumberExpr):
            generator.emit(f"mov rax, {expr.value}", type="text")
        elif isinstance(expr, expressions.VariableExpr):
            generator.emit(f"mov rax, [{expr.name}]\n", type="text")
        elif isinstance(expr, expressions.BinaryopExpr):
            CodeGenerator.get_expr_value(expr.left, generator)
            generator.emit("push rax\n", type="text")

            CodeGenerator.get_expr_value(expr.right, generator)
            generator.emit("pop rbx\n", type="text")


            if expr.operator == "+":
                generator.emit("add rax, rbx\n", type="text")
            elif expr.operator == "-":
                generator.emit("sub rbx, rax\n", type="text")
                generator.emit("mov rax, rbx\n", type="text")
            elif expr.operator == "*":
                generator.emit("imul rax, rbx\n", type="text")
            elif expr.operator == "/":
                generator.emit("mov rdx, 0", type="text")
                generator.emit("mov rcx, rax\n", type="text")
                generator.emit("mov rax, rbx\n", type="text")
                generator.emit("idiv rcx\n", type="text")

        elif isinstance(expr, expressions.CallExpr):
            regs = ["rdx", "rcx", "r8", "r9"]

            for i, param in enumerate(expr.parameters):
                CodeGenerator.get_expr_value(param, generator)
                
                if i < 4:
                    generator.emit(f"mov {regs[i]}, rax\n", type="text")
                else:
                    generator.emit("push rax\n", type="text")
                
            generator.emit(f"call {expr.name}\n", type="text")

        else:
            print(f"Error: Unsupported expression type '{type(expr).__name__}'")
            sys.exit(1)

    def push(self, generator):
        if isinstance(self.node, statements.Let):
            name = self.node.name
            expr = self.node.value
            CodeGenerator.get_expr_value(expr, generator)

            self.generator.emit(f"mov [{name}], rax\n", type="text") 
            self.generator.emit(f"{name} dq 0", type="data")

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
            value = CodeGenerator.get_expr_value(expr, generator)
            self.generator.emit(f"exit_code = {value}\n")
            self.generator.emit("Std.exit(exit_code)\n")
        
        elif isinstance(self.node, statements.Return):
            value = CodeGenerator.get_expr_value(self.node.value, generator)
            self.generator.emit(f"ret\n", type="text")

        elif isinstance(self.node, statements.Call):
            call = expressions.CallExpr(self.node.name, self.node.parameters)
            CodeGenerator.get_expr_value(call, self.generator)

        elif isinstance(self.node, statements.Log):
            value = CodeGenerator.get_expr_value(self.node.value, generator)
            self.generator.emit(f"print({value})\n", type="text")

        elif isinstance(self.node, statements.If):
            condition = CodeGenerator.get_expr_value(self.node.condition, generator)
            self.generator.emit(f"if {condition}:\n")
            self.generator.indent_push()

            for stmt in self.node.then_branch:
                node = CodeGenerator(stmt, self.generator)
                node.push()

            self.generator.indent_pop()