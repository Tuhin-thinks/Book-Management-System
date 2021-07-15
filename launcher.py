import os.path

import Lib
from global_imports import *


class HomeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(HomeWindow, self).__init__()

        self.search_thread = QtCore.QThread()
        self.search_obj = None
        self.actionCenterWindow = None
        self.ui = Lib.home.Ui_MainWindow()
        self.ui.setupUi(self)

        self.thread_pool = []
        self.selection = Lib.Classes.Selection()
        self.ui.tableView_books.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.ui.tableView_books.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ui.tableView_books.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.ui.tableView_books.installEventFilter(self)
        # header = ['Book Name', 'File Path', 'Size (KB)']
        self.ui.pushButton_search.clicked.connect(self.openFile)
        self.ui.actionOpen_Action_Center.triggered.connect(self.openActionCenter)

    def get_selected_rows(self):
        selection_model = self.ui.tableView_books.selectionModel()
        selected = []
        if selection_model:
            row_count = self.ui.tableView_books.model().rowCount()
            column_count = self.ui.tableView_books.model().columnCount()
            for row in range(row_count):
                column_data = []
                for column_index in range(column_count):
                    column_ = selection_model.selectedRows(column_index)
                    try:
                        column_data.append(column_[0].data(0))
                    except IndexError:  # IndexError may occur when there is no selection
                        return
                    break  # break to only get the book name (first column)
                selected.append(column_data[0])

        self.selection.add_to_selection(Lib.Classes.Selection(selected))

    def openActionCenter(self):
        self.get_selected_rows()
        if not self.selection:
            return
        self.actionCenterWindow = Lib.ActionCenter.ActionCenter(self.selection, self.ui.lineEdit_searchhPath.text())
        self.actionCenterWindow.close_signal.connect(self.close_action_window)
        self.actionCenterWindow.show()
        self.hide()

    def close_action_window(self):
        self.show()
        self.actionCenterWindow.close()

    def openFile(self):
        searchPath = self.ui.lineEdit_searchhPath.text()
        book_dir = os.path.expanduser("~/Downloads/") if not searchPath else searchPath
        folderName = Lib.FileOpener.OpenDir(self, "Select Book Directory", book_dir)
        if folderName:
            Lib.showStatus(self, f"Opening {folderName}")
            self.ui.lineEdit_searchhPath.setText(folderName)
            self.searchBooks(folderName)

    def searchBooks(self, path: str):
        if not hasattr(self, 'search_thread'):
            self.search_thread = QtCore.QThread()
            self.thread_pool.append(self.search_thread)
        self.search_obj = Lib.ThreadObjects.FindBooks(path)
        self.search_obj.ignore = [".jpeg", '.png', '.jpg', '.html', '.txt', '.db', '.py', '.js', '.css', '.pyc']
        self.search_obj.status.connect(partial(Lib.showStatus, self))
        self.search_obj.close.connect(self.Disconnect_searchThread)
        self.search_obj.books_found.connect(self.set_data_to_table)
        self.search_obj.moveToThread(self.search_thread)
        self.search_thread.started.connect(self.search_obj.search)
        self.search_thread.start()

    def Disconnect_searchThread(self):
        while True:
            try:
                self.search_thread.quit()
            except Exception:
                pass
            try:
                self.search_thread.disconnect()
            except TypeError:
                break

    def set_data_to_table(self, books: typing.List[typing.List] = ...):
        model = Lib.FileShowModel(books)
        self.ui.tableView_books.setModel(model)
        self.ui.tableView_books.adjustSize()
        self.update()

    def eventFilter(self, source: 'QtCore.QObject', event: 'QtCore.QEvent'):
        if source == self.ui.tableView_books and event.type() == QtCore.QEvent.Resize:
            table_width = self.ui.frame.width()
            self.ui.tableView_books.setColumnWidth(0, (table_width * 25 // 100))
            self.ui.tableView_books.setColumnWidth(1, (table_width * 50 // 100))
            self.ui.tableView_books.setColumnWidth(2, (table_width * 27 // 100))

        return super(HomeWindow, self).eventFilter(source, event)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    w = HomeWindow()
    w.show()
    sys.exit(app.exec())
