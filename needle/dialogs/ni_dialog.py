from dialogs.no_input_ui import Ui_no_input_dialog
from PySide6 import QtWidgets


class No_Input(QtWidgets.QDialog, Ui_no_input_dialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_no_input_dialog()
        self.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    form = No_Input()
    form.open()
    app.exec()
