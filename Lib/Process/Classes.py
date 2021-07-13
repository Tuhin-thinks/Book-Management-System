import os.path

from global_imports import *
import Lib.Utils.get_extensions


class InvalidRemoveIndex(Exception):
    def __str__(self):
        return "Invalid index to remove an item"


class Selection:
    """
    class to create selection of books from home window
    """
    extensions_file_path = "Utils/ExtensionsFile.txt"

    def __init__(self, book_name=None):
        self.valid_extensions = []
        self.selected = []
        if book_name:
            self.add_to_selection(book_name)

    def load_valid_extensions(self):
        if not os.path.exists(self.extensions_file_path):
            print(f"{Fore.LIGHTGREEN_EX + Back.LIGHTWHITE_EX}Scraping valid extensions [Please wait...]"
                  f" This will be done once since app installation {Style.RESET_ALL}")
            Lib.Utils.get_extensions.main()
        with open(self.extensions_file_path, 'r') as extensions_file:
            for line in extensions_file.read().strip('\n ').split('\n'):
                if line.strip('\n'):
                    self.valid_extensions.append(line)

    def verify_extension(self, filename:str):
        extension = os.path.splitext(filename)[-1]
        if extension in self.valid_extensions:
            return True
        return False

    def add_to_selection(self, book_names):
        if type(book_names) == str and self.verify_extension(book_names):
            self.selected.append(book_names)
        elif type(book_names) == list:
            for book in book_names:
                if self.verify_extension(book):
                    self.selected.append(book)

    def clear_selection(self):
        self.selected.clear()

    def remove_from_selection(self, index_: int):
        if index_ + 1 > len(self.selected):
            raise InvalidRemoveIndex(f"Expected index_ value to be between 0 and {len(self.selected)-1}")
        else:
            return self.selected.pop(index_)

    def __iter__(self):
        return iter(self.selected)

    def __str__(self):
        selections = []
        for item in self.selected:
            selections.append(item)
        return "\n".join(selections)
