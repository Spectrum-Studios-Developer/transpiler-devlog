'''
    Code Rules:
        - Classes: PascalCase
        - Functions: snake_case
        - Global Storage: snake_case
        - Local Storage: camelCase
        - Indentation: 4 spaces
'''

import tokenizer
import parser

import os
import sys

input_path = os.path.join(os.getcwd(), sys.argv[1] if len(sys.argv) > 1 else "input.plang")
build_path = os.path.join(os.getcwd(), "build", "out.py")

class FileUtils:
    def init():
        os.makedirs(os.path.dirname(build_path), exist_ok=True)
        with open(build_path, "w") as f:
            f.write("exit_code = 0\n")

    @staticmethod
    def append_to_file(content):
        with open(build_path, "a") as f:
            f.write(content)

class Generator:
    def __init__(self):
        self.out = []
        self.indent = 0

    def emit(self, line):
        self.out.append(("    " * self.indent) + line)

    def indent_push(self):
        self.indent += 1
    
    def indent_pop(self):
        self.indent -= 1

    def build(self):
        FileUtils.append_to_file(''.join(self.out))

if __name__ == "__main__":
    FileUtils.init()
    generator = Generator()

    depth_index = 0
    tokens = tokenizer.getTokens(input_path)

    parser_module = parser.Parser(tokens)
    program = parser_module.parse_program()

    for stmt in program:
        node = parser.Stmt(stmt, generator)
        node.push()
    
    generator.build()


