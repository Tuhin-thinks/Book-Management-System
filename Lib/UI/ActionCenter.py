from global_imports import *
from . import action_center
import Lib


class ActionCenter(QtWidgets.QMainWindow):
    close_signal = QtCore.pyqtSignal()

    def __init__(self, selection: 'Lib.Classes.Selection', selection_path: str):
        super(ActionCenter, self).__init__()

        self.selected = selection.selected
        self.selection_path = selection_path

        self.ui = action_center.Ui_MainWindow()
        self.ui.setupUi(self)

        option = namedtuple("option", ["text", "active_status"])
        options = (
            option("Batch Selection", 1),
            option("Analyze Selected", 0),
            option("Remove Selected", 0)
        )
        self.create_buttons(options)

    def create_buttons(self, options):
        for op in options:
            button = Lib.customPushButton.add_custom_button(self.ui, self.ui.scrollAreaWidgetContents)
            button.setText(op.text)
            button.setEnabled(bool(op.active_status))

    def generate_description_text(self):
        length = f"Total {len(self.selection.selected)} books selected."
        selection_path = f"Common Selection Path: {os.path.dirname(self.selection_path)}"
        hint_text = "Hint: Select option from right panel to perform on the selections"

        return "\n".join([length, selection_path, '\n', hint_text])

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_signal.emit()
