from global_imports import *


def OpenDir(parent, title, preferred_dir=None):
    """
    Opens directory and returns directory path or None (if nothing selected/ pop-up cancelled)
    :param parent:
    :param title:
    :param preferred_dir:
    :return:
    """
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.ShowDirsOnly
    dirName = QtWidgets.QFileDialog.getExistingDirectory(parent, title, directory=preferred_dir, options=options)
    if dirName:
        return dirName
    else:
        return None
