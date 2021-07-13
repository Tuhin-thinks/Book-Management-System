from global_imports import *


class FileShowModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(FileShowModel, self).__init__()
        self._data = data
    
    def data(self, index: QtCore.QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
    
    def rowCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return len(self._data)
    
    def columnCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return len(self._data[0])
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ('Book Name', 'File Path', 'Book Size')[section]
        else:
            return "{}".format(section)
