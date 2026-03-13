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
import generator.py.py as py_generator

import os
import sys

cwd = os.getcwd()
base_folder = os.path.basename(cwd)
input_path = os.path.join(cwd, sys.argv[1] if len(sys.argv) > 1 else "input.plang")
build_path = os.path.join(cwd, "build", f"{base_folder}.py")

build_version = sys.argv[2] if len(sys.argv) > 2 else "python"

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

    def build(self, version):
        if version == "python":
            py_generator.CodeGenerator.build_start_of_file()
            FileUtils.append_to_file(''.join(self.out))
            py_generator.CodeGenerator.build_end_of_file()
            print(f"Finished: File generated at {build_path}")
            print(f"---------------------------------------------------------")
            return
        elif version == "x86-64":
            print("x86-64 generation not implemented yet")
            return
        else:
            print(f"Error: Unsupported build version '{version}'")
            return

if __name__ == "__main__":
    FileUtils.init()
    generator = Generator()

    depth_index = 0
    index = 0
    tokens = tokenizer.getTokens(input_path)

    parser_module = parser.Parser(tokens)
    program = parser_module.parse_program()

    print(f"--------------------  PLANG COMPILER  -------------------")
    for stmt in program:
        if build_version == "python":
            node = py_generator.CodeGenerator(stmt, generator)
        elif build_version == "x86-64":
            print("x86-64 generation not implemented yet")
            sys.exit(1)
        else:
            print(f"Error: Unsupported build version '{build_version}'")
            sys.exit(1)
        node.push()
        index += 1
        print(f"[{index}/{len(program)}] Generated {stmt.__class__.__name__} statement")
    
    generator.build(build_version)


'''
1 else
2 while
3 boolean literals (true false)
4 logical operators (&& ||)
5 arrays
6 scopes
'''