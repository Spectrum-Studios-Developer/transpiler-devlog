'''
    Code Rules:
        - Classes: PascalCase
        - Functions: snake_case
        - Global Storage: snake_case
        - Local Storage: camelCase
        - Indentation: 4 spaces
'''

import tokenizer
import parser.parser as parser
import parser.libraries as libraries

import os
import sys

input_path = os.path.join(os.getcwd(), sys.argv[1] if len(sys.argv) > 1 else "input.plang")
build_path = os.path.join(os.getcwd(), "build", "out.py")

class FileUtils:
    def init():
        os.makedirs(os.path.dirname(build_path), exist_ok=True)
        with open(build_path, "w") as f:
            f.write("")

    @staticmethod
    def append_to_file(content):
        with open(build_path, "a") as f:
            f.write(content)

class Generator:
    def __init__(self):
        self.out = []
        self.indent = 1

    def emit(self, line):
        self.out.append(("    " * self.indent) + line)

    def indent_push(self):
        self.indent += 1
    
    def indent_pop(self):
        self.indent -= 1

    def build(self):
        FileUtils.append_to_file("import sys\n\n# START LIBRARIES\n")
        libraries.Std.build()
        FileUtils.append_to_file("#END LIBRARIES\n\ndef __program__():\n")
        FileUtils.append_to_file("    global exit_code\n\n    # Start of the user's program\n")
        FileUtils.append_to_file(''.join(self.out))
        FileUtils.append_to_file("\nexit_code = 0\n")
        FileUtils.append_to_file("__program__() # Execute the program\n")
        FileUtils.append_to_file("Std.exit(exit_code)\n")

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