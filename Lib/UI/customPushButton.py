from global_imports import *


def add_custom_button(parent, root):
    """

    :param parent: self
    :param root: parent.scrollAreaWidgetContents
    :return: 'QtWidgets.QPushButton'
    """
    parent.pushButton_3 = QtWidgets.QPushButton(root)
    parent.pushButton_3.setObjectName(u"pushButton_3")
    parent.pushButton_3.setMinimumSize(QtCore.QSize(301, 71))
    parent.pushButton_3.setMaximumSize(QtCore.QSize(301, 71))
    font = QtGui.QFont()
    font.setFamily(u"Impact")
    font.setPointSize(11)
    parent.pushButton_3.setFont(font)
    parent.pushButton_3.setStyleSheet(u"QPushButton{\n"
                                      "	border: 1px solid white;\n"
                                      "	border-top: 3px solid black;\n"
                                      "	border-bottom: 3px solid black;\n"
                                      "	border-right: 2px solid grey;\n"
                                      "	border-left: 2px solid grey;\n"
                                      "	border-radius: 5px;\n"
                                      "}\n"
                                      "QPushButton::hover{\n"
                                      "	background-color:rgb(185, 185, 185);\n"
                                      "}\n"
                                      "QPushButton::pressed{\n"
                                      "	color: white;\n"
                                      "}")

    parent.verticalLayout.addWidget(parent.pushButton_3)
    return parent.pushButton_3
