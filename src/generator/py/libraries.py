from main import FileUtils as file_utils

class Std:
    def __init__(self, exitdbg=False):
        self.exitdbg = exitdbg

    def build(self):
        # Exit
        file_utils.append_to_file("class Std:\n")
        file_utils.append_to_file("    @staticmethod\n")
        file_utils.append_to_file("    def exit(value):\n")
        if self.exitdbg:
            file_utils.append_to_file("        print(f'Exited with code {repr(value)}')\n")
        file_utils.append_to_file("        sys.exit(value)\n")
