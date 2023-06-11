from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
import pathlib
import zipfile
from typing import Any
import pandas as pd
from io import BytesIO


class ProxyModel(QAbstractProxyModel):
    def __init__(self, model, placeholderText="---", parent=None):
        super().__init__(parent)
        self._placeholderText = placeholderText
        self.setSourceModel(model)

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        return self.createIndex(row, column)

    def parent(self, index: QModelIndex = ...) -> QModelIndex:
        return QModelIndex()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self.sourceModel().rowCount() + 1 if self.sourceModel() else 0

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self.sourceModel().columnCount() if self.sourceModel() else 0

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if index.row() == 0 and role == Qt.DisplayRole:
            return self._placeholderText
        elif index.row() == 0 and role == Qt.EditRole:
            return None
        else:
            return super().data(index, role)

    def mapFromSource(self, sourceIndex: QModelIndex):
        return self.index(sourceIndex.row() + 1, sourceIndex.column())

    def mapToSource(self, proxyIndex: QModelIndex):
        return self.sourceModel().index(proxyIndex.row() - 1, proxyIndex.column())

    def mapSelectionFromSource(self, sourceSelection: QItemSelection):
        return super().mapSelectionFromSource(sourceSelection)

    def mapSelectionToSource(self, proxySelection: QItemSelection):
        return super().mapSelectionToSource(proxySelection)

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole
    ):
        if not self.sourceModel():
            return None
        if orientation == Qt.Vertical:
            return self.sourceModel().headerData(section - 1, orientation, role)
        else:
            return self.sourceModel().headerData(section, orientation, role)

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        return self.sourceModel().removeRows(row, count - 1)


class CellModel:
    raw_table_data = []

    def __init__(self, table: QTableWidget) -> None:
        self.table = table

    def render_model(self, input_paths: list):
        self.input_paths = input_paths
        for row, input_path in enumerate(self.input_paths):
            with zipfile.ZipFile(input_path.as_posix(), "r") as archive:
                self.generate_row(archive.namelist(), row, input_path)
        self.table.removeRow(self.table.rowCount() - 1)

    def generate_row(self, source_list: list, row: int, input_path: pathlib.Path):
        self.table.insertRow(row)
        label0 = QLabel(text=pathlib.Path(input_path).name.replace(".zip", ""))
        checkbox = QCheckBox(text=" " + str(row + 1) + ".")
        label0.setAlignment(Qt.AlignCenter)
        self.table.setRowHeight(row, 45)
        self.table.setCellWidget(row, 0, checkbox)
        self.table.setCellWidget(row, 1, label0)

        zip_sfxs = {
            pathlib.Path(each).name: pathlib.Path(each).suffix
            for each in source_list
            if pathlib.Path(each).suffix == ".zip"
        }

        sgml_sfxs = {
            pathlib.Path(each).name: pathlib.Path(each).suffix
            for each in source_list
            if (
                (pathlib.Path(each).suffix == ".xml")
                or (pathlib.Path(each).suffix == ".sgm")
                or (pathlib.Path(each).suffix == ".sgml")
            )
            and not (
                pathlib.Path(each).name.startswith("PMC-")
                or pathlib.Path(each).name.startswith("DMC-")
            )
        }

        pdf_sfxs = {
            pathlib.Path(each).name: pathlib.Path(each).suffix
            for each in source_list
            if (pathlib.Path(each).suffix == ".pdf")
            or (pathlib.Path(each).suffix == ".PDF")
        }

        source_lens = (
            len(list(zip_sfxs.keys())),
            len(list(sgml_sfxs.keys())),
            len(list(pdf_sfxs.keys())),
        )

        if any(source_lens):
            # ZIP sources
            if source_lens[0] > 1:
                self.widget_multiple_source(row, 2, zip_sfxs)

            elif source_lens[0] == 1:
                self.widget_single_source(row, 2, zip_sfxs)

            else:
                self.widget_no_source("No archive found", row, 2)

            # SGML sources
            if source_lens[1] > 1:
                self.widget_multiple_source(row, 3, sgml_sfxs)

            elif source_lens[1] == 1:
                self.widget_single_source(row, 3, sgml_sfxs)

            else:
                self.widget_no_source("No XML/SGML found", row, 3)

            # PDF sources
            if source_lens[2] > 1:
                self.widget_multiple_source(row, 4, pdf_sfxs)

            elif source_lens[2] == 1:
                self.widget_single_source(row, 4, pdf_sfxs)

            else:
                self.widget_no_source("No PDF found", row, 4)

        else:
            label = QLabel(text="    -- No Source Found --")
            label.setStyleSheet("border-color: rgb(150, 150, 150);")
            label.setCursor(Qt.ForbiddenCursor)
            self.table.setCellWidget(row, 2, label)
            label.setAlignment(Qt.AlignCenter)
            self.table.setSpan(
                row, 2, self.table.rowSpan(row, 2), self.table.columnSpan(row, 2) * 3
            )

    def widget_multiple_source(self, row, col, src_sfxs):
        combox_lay = QComboBox()
        model = QStandardItemModel()
        for archive in list(src_sfxs.keys()):
            model.appendRow(QStandardItem(archive))
        combox_lay.setModel(ProxyModel(model, "    -- Multiple Source Found --"))
        combox_lay.setCurrentIndex(0)
        combox_lay.setCursor(Qt.PointingHandCursor)
        self.table.setCellWidget(row, col, combox_lay)

    def widget_single_source(self, row, col, src_sfxs):
        label = QLabel(text=list(src_sfxs.keys())[0])
        label.setToolTip(list(src_sfxs.keys())[0])
        label.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(row, col, label)

    def widget_no_source(self, signal, row, col):
        label = QLabel(text="--")
        label.setToolTip(signal)
        label.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(row, col, label)


class LoadTable(QTableWidget):
    def __init__(self, input_files: list, parent=None):
        super(LoadTable, self).__init__(1, 5, parent)
        self.setFont(QFont("Helvetica", 10, QFont.Normal, italic=False))
        headertitle = (
            "  Select  ",
            "FOLDER NAME",
            "ZIP SOURCE",
            "XML/SGML",
            "PDF SOURCE",
        )
        self.setHorizontalHeaderLabels(headertitle)
        self.verticalHeader().hide()
        self.horizontalHeader().setHighlightSections(False)
        self.resizeColumnToContents(0)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setStyleSheet(
            """
            QHeaderView::section {
                border-top:1.5px solid;
                border-left:1.5px solid;
                border-right:1.5px solid;
                border-bottom: 1.5px solid;
                padding:4px;
                margin-left: 5px;
                border-radius: 10px;
                border-color: rgb(180, 100, 180);
                font-weight:600;
                margin-right: 5px;
        }
        """
        )

        self.setStyleSheet(
            """
        QLabel { 
                border-top:1.5px solid;
                border-left:1.5px solid;
                border-right:1.5px solid;
                border-bottom: 1.5px solid;
                border-radius: 10px;
                border-color: rgb(98, 114, 164);
                font-weight:600;
                margin-top: 10px;
                height: 50px;
                           }
        QLabel:hover { 
                border-top:1.5px solid;
                border-left:1.5px solid;
                border-right:1.5px solid;
                border-bottom: 1.5px solid;
                border-radius: 10px;
                border-color: rgb(139, 233, 253);
                font-weight:600;
                margin-top: 10px;
                height: 50px;
                           }
        QComboBox { 
                border-top:1.5px solid;
                border-left:1.5px solid;
                border-right:1.5px solid;
                border-bottom: 1.5px solid;
                border-radius: 10px;
                border-color: rgb(255, 85, 85);
                font-weight:600;
                margin-top: 10px;
                height: 50px;
                           }

        QComboBox:hover { 
                border-top:1.5px solid;
                border-left:1.5px solid;
                border-right:1.5px solid;
                border-bottom: 1.5px solid;
                border-radius: 10px;
                border-color: rgb(139, 233, 253);
                font-weight:600;
                margin-top: 10px;
                height: 50px;
                           }
        """
        )

        CellModel(self).render_model(input_files)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)


class topButton(QPushButton):
    def __init__(self, text: str, icon: str):
        super().__init__()
        self.name = text
        self.ico = icon
        self.configure()

    def configure(self):
        self.setText(self.name)
        icon = QIcon()
        icon.addFile(f":/icons/icons/{self.ico}", QSize(), QIcon.Normal, QIcon.Off)
        self.setIcon(icon)
        self.setMinimumHeight(40)
        self.setMinimumWidth(100)
        self.setStyleSheet(
            """
                QPushButton {
                    background-color: rgb(100, 30, 156);
                    border: 1.5px solid;
                    border-color: rgb(100, 100, 100);
                    border-radius: 15px;
                }

                QPushButton:hover {
                    background-color: rgb(111, 56, 167);
                    border-color: rgb(180, 100, 180);
                }

                QPushButton:disabled {
                    background-color: rgb(50, 50, 50);
                    border-color: rgb(100, 100, 100);
                }

                QPushButton:pressed {
                    background-color: #6272a4;
                    border-color: #bd93f1;
                }
            """
        )


class TableModel(QFrame):
    deleted_rows = []

    def __init__(self, input_files: list, parent_layout: QVBoxLayout):
        super().__init__()
        del self.deleted_rows[:]
        if isinstance(input_files, str):
            self.input_files = input_files.split("; ")
        else:
            self.input_files = input_files
        self.parent_layout = parent_layout
        self.initUi()
        self.setStyleSheet(
            """QFrame {
                        border: none;
                            }"""
        )

    def initUi(self):
        layoutV = QVBoxLayout(self)

        area = QScrollArea(self)
        area.setWidgetResizable(True)
        scrollAreaWidgetContents = QWidget()
        mainlayout = QHBoxLayout()
        self.table = LoadTable(self.input_files)

        mainlayout.addWidget(self.table)
        self.setTopButtons(layoutV)
        scrollAreaWidgetContents.setLayout(mainlayout)
        area.setWidget(scrollAreaWidgetContents)
        layoutV.addWidget(area)

    def setTopButtons(self, rootlayout: QVBoxLayout):
        mainlayout = QHBoxLayout()

        self.next_button = topButton("  Next", "cil-arrow-circle-right.png")
        self.export_button = topButton("  Export", "cil-external-link.png")
        self.save_button = topButton("  Save", "cil-save.png")
        self.reload_button = topButton("  Reload", "cil-reload.png")
        self.delete_button = topButton("  Delete", "cil-x.png")
        self.restore_button = topButton("  Restore", "cil-window-restore.png")

        self.restore_button.setEnabled(False)
        self.reload_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.export_button.setEnabled(False)

        self.save_button.clicked.connect(self.save_data)
        self.reload_button.clicked.connect(self.reload_table_data)
        self.delete_button.clicked.connect(self.remove_rows)
        self.restore_button.clicked.connect(self.restore_rows)
        self.next_button.clicked.connect(self.segregation_context)
        self.export_button.clicked.connect(self.export_to_excel)

        mainlayout.addWidget(self.delete_button)
        mainlayout.addWidget(self.restore_button)
        mainlayout.addWidget(self.save_button)
        mainlayout.addWidget(self.reload_button)
        mainlayout.addWidget(self.export_button)
        mainlayout.addWidget(self.next_button)

        mainlayout.setAlignment(Qt.AlignRight)
        rootlayout.addLayout(mainlayout)

    def save_data(self):
        self.table_data = []
        self.table_save = True
        del self.table_data[:]
        for row in range(self.table.rowCount()):
            row_data = []
            for column in range(self.table.columnCount()):
                each = self.table.cellWidget(row, column)
                if isinstance(each, QLabel):
                    row_data.append(each.text())
                elif isinstance(each, QComboBox):
                    current_text = each.currentText()
                    if not current_text.__contains__("Multiple Source Found"):
                        label5 = QLabel(text=current_text)
                        row_data.append(current_text)
                        self.table.removeCellWidget(row, column)
                        self.table.setCellWidget(row, column, label5)
                        label5.setToolTip(current_text)
                        label5.setAlignment(Qt.AlignCenter)
                    else:
                        self.table_save = False
                elif each == None:
                    row_data.append(None)
            if self.table_save == True:
                self.table_data.append(row_data)

        if self.table_save == True:
            for i, items in enumerate(self.table_data):
                if None in items:
                    del self.table_data[i]
            self.reload_button.setEnabled(True)
            self.next_button.setEnabled(True)
            self.delete_button.setEnabled(False)
            self.restore_button.setEnabled(False)
            self.export_button.setEnabled(True)
        else:
            del self.table_data[:]

    def reload_table_data(self):
        self.setParent(None)
        self.parent_layout.addWidget(TableModel(self.input_files, self.parent_layout))

    def remove_rows(self):
        [self.remove_selected() for n in range(2)]

    def remove_selected(self):
        for row_checked in range(self.table.rowCount()):
            checkmark = self.table.cellWidget(row_checked, 0)
            if isinstance(checkmark, QCheckBox) and checkmark.isChecked():
                self.deleted_rows.append(
                    int(checkmark.text().replace(" ", "").replace(".", "")) - 1
                )

        for row_count in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row_count, 0)
            if isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                self.table.removeRow(row_count)

        self.restore_button.setEnabled(True)

    def restore_rows(self):
        for each in dict.fromkeys(self.deleted_rows):
            with zipfile.ZipFile(self.input_files[each].as_posix(), "r") as archive:
                CellModel(self.table).generate_row(
                    archive.namelist(), each, self.input_files[each]
                )
        self.restore_button.setEnabled(False)
        del self.deleted_rows[:]

    def segregation_context(self):
        for source in self.table_data:
            # S1000D/NONS1000D
            if source[1] != "--":
                pass
            # ISPEC
            elif source[2] != "--":
                pass

            # PDF
            elif source[3] != "--":
                pass

    def export_to_excel(self):
        filename = QFileDialog.getSaveFileName(self, filter="*.xlsx")
        if filename != ("", ""):
            excel = pathlib.Path(filename[0])
            df = pd.DataFrame(
                self.table_data,
                columns=[
                    "FOLDER NAME",
                    "ZIP SOURCE",
                    "XML/SGML",
                    "PDF SOURCE",
                ],
            )
            with pd.ExcelWriter(excel, mode="w", engine="xlsxwriter") as writer:
                df.to_excel(writer, "REMARKS", index=False)
                tbl_hdr = [{"header": c} for c in df.columns]
                writer.sheets["REMARKS"].add_table(
                    "A1:" + "D" + str(len(df) + 1),
                    {"columns": tbl_hdr, "style": "Table Style Medium 2"},
                )
