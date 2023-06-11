import sys
import os
import pathlib

from modules import *
from widgets import *
from Custom_Widgets.Widgets import *
from dialogs.ni_dialog import No_Input
from functions.tabulate import TableModel

widgets = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        loadJsonStyle(self, self.ui)

        # QSizeGrip(self.ui.size_grip)
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        widgets.btn_tabulate.clicked.connect(self.buttonClick)
        widgets.btn_arrange.clicked.connect(self.buttonClick)
        widgets.btn_compile.clicked.connect(self.buttonClick)
        widgets.btn_format.clicked.connect(self.buttonClick)

        self.numAddWidget = 1
        self.ui.titleContainer.addWidget(inputBlock())

        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)

        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)

        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)
        self.show()

        useCustomTheme = True
        themeFile = r"needle\themes\py_dracula_dark.qss"

        if useCustomTheme:
            UIFunctions.theme(self, themeFile, True)
            AppFunctions.setThemeHack(self)

        widgets.stackedWidget.setCurrentWidget(widgets.Tabulation)
        widgets.btn_tabulate.setStyleSheet(
            UIFunctions.selectMenu(widgets.btn_tabulate.styleSheet())
        )

    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()

        if btnName == "btn_tabulate":
            widgets.stackedWidget.setCurrentWidget(widgets.Tabulation)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_arrange":
            widgets.stackedWidget.setCurrentWidget(widgets.Segregation)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_compile":
            widgets.stackedWidget.setCurrentWidget(widgets.Compilation)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

        if btnName == "btn_format":
            widgets.stackedWidget.setCurrentWidget(widgets.Formatting)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU


class btn_proceed(QPushButton):
    def __init__(self) -> None:
        super(btn_proceed, self).__init__()
        self.make_settings()

    def make_settings(self):
        icon = QIcon()
        icon.addFile(
            ":/icons/icons/cil-arrow-circle-right.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.setIcon(icon)
        self.setText("  Proceed")
        self.setMinimumHeight(40)
        self.setMinimumWidth(100)
        self.setStyleSheet(
            """
    btn_proceed {
        background-color: rgb(100, 30, 156);
        border: 1.5px solid;
        border-color: rgb(100, 100, 100);
        border-radius: 15px;
    }

    btn_proceed:hover {
        background-color: rgb(111, 56, 167);
        border-color: rgb(180, 100, 180);
    }

    btn_proceed:disabled {
        background-color: rgb(50, 50, 50);
        border-color: rgb(150, 150, 150);
    }

    btn_proceed:pressed {
        background-color: #6272a4;
        border-color: #bd93f1;
    }
"""
        )


class btn_browse(QPushButton):
    def __init__(self) -> None:
        super(btn_browse, self).__init__()
        self.make_settings()

    def make_settings(self):
        icon = QIcon()
        icon.addFile(":/icons/icons/cil-browser.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setIcon(icon)
        self.setMinimumHeight(40)
        self.setMinimumWidth(40)
        self.setStyleSheet(
            """
    btn_browse {
        background-color: rgb(50, 50, 50);
        border: 1.5px solid;
        border-color: #6272a4;
        border-radius: 15px;
    }

    btn_browse:hover {
        background-color: rgb(50, 50, 50);
        border-color: rgb(180, 100, 180);
        border-radius: 15px;
    }

    btn_browse:pressed {
        background-color: #6272a4;
        border-color: #bd93f9;
        border-radius: 15px;
    }

"""
        )


class pathText(QLineEdit):
    def __init__(self):
        super(pathText, self).__init__()
        self.setPlaceholderText("Please browse your files here")
        self.setMinimumHeight(40)
        self.setStyleSheet(
            """
    pathText {
        border-radius:15px;
        border-color: #6272a4;                               
    }
    
    pathText:hover {
        border-radius: 15px;
        border-color: rgb(180, 100, 180);
    }
"""
        )


class inputBlock(QWidget):
    file_paths = []

    def __init__(self):
        super(inputBlock, self).__init__()
        self.add_inputbox()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.file_paths = [
            pathlib.Path(u.toLocalFile())
            for u in event.mimeData().urls()
            if u.toLocalFile().endswith(".zip")
        ]
        file_names = [
            pathlib.Path(u.toLocalFile()).name
            for u in event.mimeData().urls()
            if u.toLocalFile().endswith(".zip")
        ]
        self.path_text.setText("; ".join(file_names))

    def add_inputbox(self):
        self.path_text = pathText()
        self.btn_browse = btn_browse()
        self.btn_proceed = btn_proceed()
        l1 = QHBoxLayout()
        l1.addWidget(self.path_text)
        l1.addWidget(self.btn_browse)
        l1.addWidget(self.btn_proceed)
        self.addlayout = l1
        self.setLayout(self.addlayout)
        self.btn_browse.clicked.connect(self.browse_click)
        self.btn_proceed.clicked.connect(self.proceed_click)

    def browse_click(self):
        browse_result = QFileDialog.getOpenFileNames(self, filter="*.zip")
        if browse_result != ([], ""):
            self.file_paths = list(map(pathlib.Path, browse_result[0]))
            self.path_text.setText("; ".join([f.name for f in self.file_paths]))

    def proceed_click(self):
        if self.path_text.text() == "":
            self.file_paths = []

        if self.file_paths != []:
            self.btn_proceed.setEnabled(False)
            self.arrange_input()
        else:
            No_Input().exec()

    def arrange_input(self):
        widgets.TableContainer.setAlignment(Qt.AlignTop)
        widgets.TableContainer.addWidget(
            TableModel(self.file_paths, widgets.TableContainer)
        )


class DropLineEdit(QtWidgets.QLineEdit):
    def __init__(self):
        super(DropLineEdit, self).__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        md = event.mimeData()

        if md.hasUrls():
            files = []
            for url in md.urls():
                files.append(url.toLocalFile())
            self.setText(" ".join(files))
            event.acceptProposedAction()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
