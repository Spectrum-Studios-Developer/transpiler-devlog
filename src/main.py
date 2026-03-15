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
import generator.x8664.x8664 as x8664_generator

import os
import sys

build_version = None
build_extension = None
cwd = None
base_folder = None
input_path = None
build_path = None


class FileUtils:
    @staticmethod
    def init():
        m = sys.modules.get('__main__') or sys.modules.get('main')
        os.makedirs(os.path.dirname(m.build_path), exist_ok=True)
        with open(m.build_path, "w") as f:
            f.write("")

    @staticmethod
    def append_to_file(content):
        m = sys.modules.get('__main__') or sys.modules.get('main')
        with open(m.build_path, "a") as f:
            f.write(content)

class Generator:
    def __init__(self):
        self.out = []

        self.text = []
        self.data = []
        self.label_id = 0

        self.indent = 1

    def emit(self, line, type="out"):
        if type == "out":
            self.out.append(("    " * self.indent) + line)
        elif type == "text":
            self.text.append(("    " * self.indent) + line)
        elif type == "data":
            self.data.append(line)
    
    def new_label(self):
        self.label_id += 1
        return f"L{self.label_id}"

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
        elif version == "x86-64":
            x8664_generator.CodeGenerator.build_data()
            FileUtils.append_to_file(''.join(self.data))
            x8664_generator.CodeGenerator.build_text()
            FileUtils.append_to_file(''.join(self.text))
            print(f"Finished: File generated at {build_path}")
            print(f"---------------------------------------------------------")
        else:
            print(f"Error: Unsupported build version '{version}'")


def resolve_build_config():
    global build_version, build_extension, cwd, base_folder, input_path, build_path
    
    build_version = sys.argv[2] if len(sys.argv) > 2 else "python"
    if build_version not in ["python", "x86-64"]:
        print(f"Error: Unsupported build version '{build_version}'")
        sys.exit(1)

    if build_version == "x86-64":
        print("Warning: Building for x86-64 is currently in early stages and may not support all features or generate fully optimized code.")
        print("Do you wish to succeed anyway? (y/n)")
        if input().lower() != "y":
            sys.exit(0)

    build_extension = "py" if build_version == "python" else "asm"

    cwd = os.getcwd()
    base_folder = os.path.basename(cwd)
    input_path = os.path.join(cwd, sys.argv[1] if len(sys.argv) > 1 else "input.plang")
    build_path = os.path.join(cwd, "build", f"{base_folder}.{build_extension}")
    
    print(f"DEBUG build_path = {build_path}")
    print(f"DEBUG sys.modules['main'].build_path = {sys.modules['main'].build_path}")


def main():
    resolve_build_config()
    FileUtils.init()
    generator = Generator()

    index = 0
    tokens = tokenizer.getTokens(input_path)

    parser_module = parser.Parser(tokens)
    program = parser_module.parse_program()

    print(f"--------------------  PLANG COMPILER  -------------------")
    for stmt in program:
        if build_version == "python":
            node = py_generator.CodeGenerator(stmt, generator)
        elif build_version == "x86-64":
            node = x8664_generator.CodeGenerator(stmt, generator)
        else:
            print(f"Error: Unsupported build version '{build_version}'")
            sys.exit(1)
        node.push()
        index += 1
        print(f"[{index}/{len(program)}] Generated '{stmt.__class__.__name__}' statement")

    generator.build(build_version)


if __name__ == "__main__":
    main()


'''
1 else -> else if  - DONE
2 while - DONE
3 boolean literals (true false) - DONE
4 logical operators (&& ||)
5 arrays
6 scopes
''' 