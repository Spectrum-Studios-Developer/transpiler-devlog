import main

class Std:
    @staticmethod
    def build():
        # Exit
        main.FileUtils.append_to_file("class Std:\n")
        main.FileUtils.append_to_file("    @staticmethod\n")
        main.FileUtils.append_to_file("    def exit(value):\n")
        main.FileUtils.append_to_file("          print(f'Exited with code {repr(value)}')\n")
        main.FileUtils.append_to_file("          sys.exit(value)\n")
