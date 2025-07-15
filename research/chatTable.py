from PySide6.QtWidgets import QWidget, QApplication, QPushButton, QTableView, QVBoxLayout
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
import sys

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.myData = data # assign data to myData: data will be passe to the class on creating object/instance


    def rowCount(self, parent=QModelIndex()):
        print(f"Number of rows of myData:  {len(self.myData)}")
        return len(self.myData)

    def columnCount(self, parent=QModelIndex()):
        print(f"Number of column is {len(self.myData[1])}") # row index 1  : basically length counts the number of items in an iterable: array we have 2 items: 2 columns
        if len(self.myData) == 0:
            print(f"Returning 0")
            return 0
        else:
            return len(self.myData[0])
    
    def getData(self, index, role=Qt.DisplayRole):
        # this methods returns data for the given index and role
        # index: QModelIndex containing row and column
        # role : data role, (DisplayRole=text, decorationRole=icon)
        row = index.row()
        col = index.column()

        if role == Qt.DisplayRole:
            print(str(self.myData[row][col]))
            return str(self.myData[row][col])
        
    def headerColumns(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                print(f"Column {section}")
                return f'Column {section}'
            else:
                print(f"Row {section}")
                return(f"Row {section}")
            
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        users_data = [
            ["FreeCodeCamp JavaScript & DataStructures", 25],
            ["KaliDev-Track", 26],
            ["ANN", 27]
        ]
        vLayout=QVBoxLayout()
        model = TableModel(users_data)
        myTable = QTableView()
        myTable.setModel(model)
        vLayout.addWidget(myTable)

        self.setLayout(vLayout)

app = QApplication()
window = MainWindow()
window.show()
exit_code = app.exec()
sys.exit(exit_code)



# first_instance = TableModel(users_data)
# first_instance.rowCount()
# first_instance.columnCount()
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         TableModel()