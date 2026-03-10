import tokenizer
import os

fileName = input(" > ")

class FileUtils:
    file_path = os.path.join(os.getcwd(), "build", "out.py")
    @staticmethod
    def append_to_file(file, content):
        if not os.path.exists(FileUtils.file_path):
            os.makedirs(os.path.dirname(FileUtils.file_path), exist_ok=True)
            with open(FileUtils.file_path, "w") as f:
                f.write("")
        with open(FileUtils.file_path, "a") as f:
            f.write(content)

class Generator:
    tokenDefinitions = {
        "function": "def ",
        "return": "return ",
        "{": ":\n",
        "}": "",
        ";": "\n",
        "console.log": "print",
        "true": "True",
        "false": "False",
    }

    @staticmethod
    def generate():
        tokens = tokenizer.getTokens(fileName)
        depth_index = 0
        skip_next = 0
        for token in tokens:
            if skip_next > 0:
                skip_next -= 1
                continue

            if token == "console":
                print("Found console")
                print(tokens[tokens.index(token) + 1])
                print(tokens[tokens.index(token) + 2])
                if tokens[tokens.index(token) + 1] == "." and tokens[tokens.index(token) + 2] == "log":
                    FileUtils.append_to_file("out.py", Generator.tokenDefinitions["console.log"])
                    skip_next = 2
                    continue

            if token in Generator.tokenDefinitions: # if the token is specified in the token definitions:
                if token == "{":
                    depth_index += 1
                    FileUtils.append_to_file("out.py", Generator.tokenDefinitions[token] + "    " * depth_index)
                elif token == "}":
                    depth_index -= 1
                    FileUtils.append_to_file("out.py", Generator.tokenDefinitions[token])
                else:
                    FileUtils.append_to_file("out.py", Generator.tokenDefinitions[token])
            else:
                FileUtils.append_to_file("out.py", token)

if __name__ == "__main__":
    Generator.generate()