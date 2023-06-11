import sys
from PySide6.QtCore import Qt, QAbstractProxyModel, QModelIndex, QItemSelection
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (QApplication, QGridLayout, QWidget, QComboBox)
from typing import Any

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(50,50,320,200)
        # self.setWindowTitle(f"Qt Version {QT_VERSION_STR}")

        layout = QGridLayout()

        cmbox = QComboBox()

        model = QStandardItemModel()
        
        for i in range(1, 11):
            model.appendRow(QStandardItem(f"Item {i}"))

        cmbox.setModel(ProxyModel(model, '---PlaceholderText---'))
        cmbox.setCurrentIndex(0)
        layout.addWidget(cmbox, 0, 0)
        

        self.setLayout(layout)
        self.show()


class ProxyModel(QAbstractProxyModel):
    def __init__(self, model, placeholderText='---', parent=None):
        super().__init__(parent)
        self._placeholderText = placeholderText
        self.setSourceModel(model)
        
    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        return self.createIndex(row, column)

    def parent(self, index: QModelIndex = ...) -> QModelIndex:
        return QModelIndex()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self.sourceModel().rowCount()+1 if self.sourceModel() else 0

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
        return self.index(sourceIndex.row()+1, sourceIndex.column())

    def mapToSource(self, proxyIndex: QModelIndex):
        return self.sourceModel().index(proxyIndex.row()-1, proxyIndex.column())

    def mapSelectionFromSource(self, sourceSelection: QItemSelection):
        return super().mapSelection(sourceSelection)

    def mapSelectionToSource(self, proxySelection: QItemSelection):
        return super().mapSelectionToSource(proxySelection)
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if not self.sourceModel():
            return None
        if orientation == Qt.Vertical:
            return self.sourceModel().headerData(section-1, orientation, role)
        else:
            return self.sourceModel().headerData(section, orientation, role)

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        return self.sourceModel().removeRows(row, count -1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())