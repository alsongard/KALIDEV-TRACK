from PySide6.QtWidgets import QStyle, QStyleOptionButton, QApplication, QTableView,QVBoxLayout, QMessageBox, QPushButton, QItemDelegate, QStyledItemDelegate, QWidget
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QEvent, Signal,Qt

class ButtonDelegate(QStyledItemDelegate):
    # Delegate that paints a button in a cell and handles it's clicks"
    button_clicked = Signal(int) # emits row index when clicked


    def paint(self, painter, option, index):
        # Draw the button using the style system
        btn_option = QStyleOptionButton()
        btn_option.rect = option.rect
        btn_option.text = "Open"
        btn_option.state = QStyle.State_Enabled | QStyle.State_Active

        QApplication.style().drawControl(
            QStyle.CE_PushButton, btn_option, painter
        )

    """
     def paint(self, painter, option, index):
        if not option.rect.isValid() or option.rect.width() == 0:
            return # skip painting

        print("this is painter")
        print(painter)

        print("this is option")
        print(option)

        print(f"This is index: {index}")
        # Draw the button uasing the Style system
        btn_option = QStyleOptionButton()
        btn_option.react = option.rect
        btn_option.text = "Open"
        btn_option.state = QStyle.State_Enabled | QStyle.State_Active

        QApplication.style().drawControl(
            QStyle.CE_PushButton, btn_option, painter
        )

        # print(f"Value of button: {btn_option.text}")
        # print(f"Rect of button: {btn_option.rect}")
    """

    def editorEvent(self, event, model, option, index):
        # Detect mouse release on the button area
        if (event.type() == QEvent.MouseButtonRelease):
            if (option.rect.contains(event.pos())):
                self.button_clicked.emit(index.row())
                return True
        return False
        

class TableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            # Return empty string for the button column
            if index.column() == 2:
                return ""
            return str(self._data[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        data = [
            ["Project A", "Active", ""],
            ["Project B", "Pending", ""],
            ["Project C", "Done", ""],
        ]
        headers = ["Name", "Status", "Action"]

        self.model = TableModel(data, headers)
        print(f"Column count: {self.model.columnCount()}")
        self.table = QTableView()
        self.table.setModel(self.model)

        # Attach the delegate to the button column
        self.delegate = ButtonDelegate()
        self.delegate.button_clicked.connect(self.on_button_clicked)
        self.table.setItemDelegateForColumn(2, self.delegate)

        # Adjust row height so the button fits nicely
        self.table.verticalHeader().setDefaultSectionSize(35)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def on_button_clicked(self, row):
        name = self.model._data[row][0]
        QMessageBox.information(self, "Row clicked", f"You clicked: {name}")


app = QApplication([])
window = MainWindow()
window.show()
app.exec()