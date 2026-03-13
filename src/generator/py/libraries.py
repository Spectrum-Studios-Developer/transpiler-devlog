from main import FileUtils as file_utils

class Std:
    @staticmethod
    def build():
        # Exit
        file_utils.append_to_file("class Std:\n")
        file_utils.append_to_file("    @staticmethod\n")
        file_utils.append_to_file("    def exit(value):\n")
        file_utils.append_to_file("          print(f'Exited with code {repr(value)}')\n")
        file_utils.append_to_file("          sys.exit(value)\n")
