import sys

import parser.expressions as expressions
import parser.statements as statements
import main

'''
THIS IS A WORK IN PROGRESS AND NOT ALL FEATURES MAY BE SUPPORTED OR FULLY FUNCTIONAL. EXPECT BUGS AND INCOMPLETE CODE GENERATION, 
ESPECIALLY FOR COMPLEX CONSTRUCTS. USE WITH CAUTION AND TEST THOROUGHLY. FEEL FREE TO CONTRIBUTE OR REPORT ISSUES TO HELP IMPROVE THE X86-64 BACKEND.
'''

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
        main.FileUtils.append_to_file("\nmain:\n")
        main.FileUtils.append_to_file("    push rbp\n")
        main.FileUtils.append_to_file("    mov rbp, rsp\n")

    @staticmethod
    def get_expr_value(expr, generator):
        if isinstance(expr, expressions.StringExpr):
            label = f"str{generator.label_id}"
            generator.label_id += 1
            generator.emit(f'    {label} db "{expr.value}", 0\n', type="data")
            generator.emit(f"    lea rax, [rel {label}]\n", type="text")

        elif isinstance(expr, expressions.NumberExpr):
            generator.emit(f"    mov rax, {expr.value}\n", type="text")

        elif isinstance(expr, expressions.VariableExpr):
            generator.emit(f"    mov rax, [rel {expr.name}]\n", type="text")

        elif isinstance(expr, expressions.BinaryopExpr):
            CodeGenerator.get_expr_value(expr.left, generator)
            generator.emit("    push rax\n", type="text")
            CodeGenerator.get_expr_value(expr.right, generator)
            generator.emit("    pop rbx\n", type="text")

            if expr.operator == "+":
                generator.emit("    add rax, rbx\n", type="text")
            elif expr.operator == "-":
                generator.emit("    sub rbx, rax\n", type="text")
                generator.emit("    mov rax, rbx\n", type="text")
            elif expr.operator == "*":
                generator.emit("    imul rax, rbx\n", type="text")
            elif expr.operator == "/":
                generator.emit("    xor rdx, rdx\n", type="text")
                generator.emit("    mov rcx, rax\n", type="text")
                generator.emit("    mov rax, rbx\n", type="text")
                generator.emit("    idiv rcx\n", type="text")

        elif isinstance(expr, expressions.CallExpr):
            WIN64_REGS = ["rcx", "rdx", "r8", "r9"]
            stack_args = []

            for i, param in enumerate(expr.parameters):
                CodeGenerator.get_expr_value(param, generator)
                if i < 4:
                    generator.emit(f"    mov {WIN64_REGS[i]}, rax\n", type="text")
                else:
                    stack_args.append(i)
                    generator.emit("    push rax\n", type="text")

            # 32-byte shadow space (Windows x64 ABI)
            generator.emit("    sub rsp, 32\n", type="text")
            generator.emit(f"    call {expr.name}\n", type="text")
            generator.emit("    add rsp, 32\n", type="text")

            if stack_args:
                generator.emit(f"    add rsp, {len(stack_args) * 8}\n", type="text")

        else:
            print(f"Error: Unsupported expression type '{type(expr).__name__}'")
            sys.exit(1)

    def push(self):
        generator = self.generator

        if isinstance(self.node, statements.Let):
            name = self.node.name
            expr = self.node.value
            CodeGenerator.get_expr_value(expr, generator)
            generator.emit(f"    mov [rel {name}], rax\n", type="text")
            generator.emit(f"    {name} dq 0\n", type="data")

        elif isinstance(self.node, statements.DefFunc):
            name = self.node.name
            generator.emit(f"\n{name}:\n", type="text")
            generator.emit("    push rbp\n", type="text")
            generator.emit("    mov rbp, rsp\n", type="text")

            WIN64_REGS = ["rcx", "rdx", "r8", "r9"]
            for i, param in enumerate(self.node.parameters):
                offset = (i + 2) * 8
                if i < 4:
                    generator.emit(f"    mov [rbp+{offset}], {WIN64_REGS[i]}\n", type="text")

            for stmt in self.node.body:
                CodeGenerator(stmt, generator).push()

            generator.emit("    pop rbp\n", type="text")
            generator.emit("    ret\n", type="text")

        elif isinstance(self.node, statements.Exit):
            CodeGenerator.get_expr_value(self.node.exprType, generator)
            generator.emit("    mov rcx, rax\n", type="text")
            generator.emit("    call ExitProcess\n", type="text")

        elif isinstance(self.node, statements.Return):
            CodeGenerator.get_expr_value(self.node.value, generator)
            generator.emit("    pop rbp\n", type="text")
            generator.emit("    ret\n", type="text")

        elif isinstance(self.node, statements.Call):
            call = expressions.CallExpr(self.node.name, self.node.parameters)
            CodeGenerator.get_expr_value(call, generator)

        elif isinstance(self.node, statements.Log):
            CodeGenerator.get_expr_value(self.node.value, generator)
            generator.emit("    mov rcx, rax\n", type="text")
            generator.emit("    call printf\n", type="text")

        elif isinstance(self.node, statements.If):
            else_label = f".else{generator.label_id}"
            end_label = f".endif{generator.label_id}"
            generator.label_id += 1

            CodeGenerator.get_expr_value(self.node.condition, generator)
            generator.emit("    cmp rax, 0\n", type="text")
            generator.emit(f"    je {else_label}\n", type="text")

            for stmt in self.node.then_branch:
                CodeGenerator(stmt, generator).push()

            if hasattr(self.node, "else_branch") and self.node.else_branch:
                generator.emit(f"    jmp {end_label}\n", type="text")
                generator.emit(f"{else_label}:\n", type="text")
                for stmt in self.node.else_branch:
                    CodeGenerator(stmt, generator).push()
                generator.emit(f"{end_label}:\n", type="text")
            else:
                generator.emit(f"{else_label}:\n", type="text")

        else:
            print(f"Error: Unsupported statement type '{type(self.node).__name__}'")
            sys.exit(1)