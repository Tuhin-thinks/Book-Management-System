from global_imports import *


class FindBooks(QtCore.QObject):
    status = QtCore.pyqtSignal(str)
    close = QtCore.pyqtSignal()
    books_found = QtCore.pyqtSignal(list)
    
    def __init__(self, path_location: str):
        super(FindBooks, self).__init__()
        self._ignore = []
        self.path_location = path_location
    
    def search(self):
        files = []
        if os.path.exists(self.path_location):
            for root, dirnames, filenames in os.walk(self.path_location):
                for file in filenames:
                    extension = os.path.splitext(file)
                    if extension in self._ignore:
                        self.status.emit(f"ignored {file}")
                        continue
                    file_path = os.path.join(root, file)

                    size_ = os.stat(file_path).st_size/1000
                    unit = "KB"
                    if size_ > 1024:
                        size_ /= 1024
                        unit = 'MB'

                    if size_ > 1024:
                        size_ /= 1024
                        unit = 'GB'

                    if size_ > 1024:
                        size_ /= 1024
                        unit = 'TB'

                    self.status.emit(file)
                    size_str_mod = f"{size_ :.02f} {unit}"
                    files.append([file, file_path, size_str_mod])
            self.status.emit(f"Total {len(files)} books found.")
        else:
            self.status.emit("Invalid path entered.")
        self.books_found.emit(files)
        self.close.emit()
    
    @property
    def ignore(self):
        return self._ignore
    
    @ignore.setter
    def ignore(self, to_ignore: List[str]):
        to_ignore.clear()
        for extensions in to_ignore:
            if extensions.startswith('.'):
                pass
            else:
                extensions = '.' + extensions
            self._ignore.append(extensions)
