import os.path
import sys

from global_imports import *
import Lib


class HomeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(HomeWindow, self).__init__()
        
        self.ui = Lib.home.Ui_MainWindow()
        self.ui.setupUi(self)

        self.thread_pool = []
        self.ui.tableView_books.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        
        header = ['Book Name', 'File Path', 'Size (KB)']
        self.ui.pushButton_search.clicked.connect(self.openFile)
    
    def openFile(self):
        searchPath = self.ui.lineEdit_searchhPath.text()
        book_dir = os.path.expanduser("~/Downloads/Books") if not searchPath else searchPath
        folderName = Lib.FileOpener.OpenDir(self, "Select Book Directory", book_dir)
        if folderName:
            Lib.showStatus(self, f"Opening {folderName}")
            self.ui.lineEdit_searchhPath.setText(folderName)
            self.searchBooks(folderName)
    
    def searchBooks(self, path:str):
        if not hasattr(self, 'search_thread'):
            self.search_thread = QtCore.QThread()
            self.thread_pool.append(self.search_thread)
        self.search_obj = Lib.ThreadObjects.FindBooks(path)
        self.search_obj.ignore = [".jpeg", '.png', '.jpg', '.html', '.txt', '.db', '.py', '.js', '.css']
        self.search_obj.status.connect(partial(Lib.showStatus, self))
        self.search_obj.close.connect(self.Disconnect_searchThread)
        self.search_obj.books_found.connect(self.setDataToTable)
        self.search_obj.moveToThread(self.search_thread)
        self.search_thread.started.connect(self.search_obj.search)
        self.search_thread.start()

    def Disconnect_searchThread(self):
        while True:
            try:
                self.search_thread.quit()
            except:
                pass
            try:
                self.search_thread.disconnect()
            except TypeError:
                break
    
    def setDataToTable(self, books: typing.List[typing.List] = ...):
        model = Lib.FileShowModel(books)
        self.ui.tableView_books.setModel(model)
        self.ui.tableView_books.adjustSize()
        self.update()
    
    def resizeColumns(self):
        table_width = self.ui.tableView_books.width()
        self.ui.tableView_books.setColumnWidth(0, table_width * 45 // 100)
        self.ui.tableView_books.setColumnWidth(1, table_width * 50 // 100)
        self.ui.tableView_books.setColumnWidth(2, table_width * 5 // 100)
        self.horizontal_header.setStretchLastSection(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = HomeWindow()
    w.show()
    sys.exit(app.exec())
