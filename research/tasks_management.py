from PySide6.QtWidgets import QTableView, QGroupBox, QWidget, QApplication, QMainWindow, QLabel,QVBoxLayout
from  PySide6 import QtCore
from PySide6.QtCore import Qt, QSize
import sys
from read_task_file import ReadTaskFiles
# Model , View & Controller (MVC) : View & Controller are treated as one

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, mydata, myHeaderData): 
        super().__init__()
        self._data = mydata
        self.headers = myHeaderData

    # returns rowCount
    def rowCount(self, index): 
        # print(f"this is index in rowCount: {index}")
        return len(self._data)

    # returns column count
    def columnCount(self, index):
        # print(f" this is count in columnCount method: {len(self.data[0])}")
        return len(self._data[0])

    # returns headers
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.headers[section])
            else:
                return str(section+1)

    # return value to displayed at given row & col index
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        # print(f"index in data method: {index}")
        # print(f"role in data method: {role}")
        # print(f'DisplayRole: {Qt.DisplayRole}')
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole  or role == Qt.ItemDataRole.EditRole: 
                value =  str(self._data[index.row()][index.column()])
                # print(f"Display value at ({index.row()}, {index.column()}): {self._data[index.row()][index.column()]}")
                return value
        return None

    # enables editing
    def setData(self, index, value, role ):
        if role == Qt.ItemDataRole.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    
    # enables editing
    def flags(self, index): 
        return (
            Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEnabled 
            | Qt.ItemFlag.ItemIsEditable
        )
        

    
class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table = QTableView() # view instance

        verticalLayout =  QVBoxLayout()
        self.central_widget = QWidget()

        filename = "/home/alson-kali/PROGRAMMING/KALIDEV-TRACK/research/random_task_data.json"

        # instance of ReadTaskFiles class
        readTaskInstance = ReadTaskFiles(filepath=filename) 
        returnedTaskData = readTaskInstance.readData()

        print("Task read from file")
        print(returnedTaskData)


        print()
        print("-------")
        phase_count = 0
        for phase_content in returnedTaskData:
            phaseContentGroupBox = QGroupBox() # GroupBox to enable styling
            phaseLayout = QVBoxLayout() # layout for the phaseContentGroupBox
            phaseTable = QTableView()
            phaseTable.wordWrapTrue = True
            phaseName = QLabel()
            phaseGoal = QLabel()

            print("this is a single phaseContent ")
            print(phase_content)
            phaseName.setText(phase_content[0]) # name
            phaseGoal.setText(f"Goal: {phase_content[1]}") # goal

            verticalLayout.addWidget(phaseName)
            verticalLayout.addWidget(phaseGoal)

            each_data = []

            for item in phase_content[2]: # array of dictionaries
                thetask = [item['subtaskname'], item["subtaskdescription"], item["subtaskstatus"]]
                each_data.append(thetask)


            print('this is all_sub_task_for_table')
            print(each_data)

            header_data = ["Module", "Description", "Status"]
            self.model = TableModel(each_data, header_data)
            phaseTable.setModel(self.model)
            phaseTable.resizeColumnsToContents()
            verticalLayout.addWidget(phaseTable)

        self.central_widget.setLayout(verticalLayout)

        self.central_widget.setStyleSheet("""
            
        """)
        self.setFixedSize(1200,600)
        self.setCentralWidget(self.central_widget)


app = QApplication()
window =  Mainwindow()
window.show()
app.exec()

"""
import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        print(f"Role in data method: {role}")
        print(f"Index in data method: {index}")
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        print(f"Index in rowCount method: {index}")
        print(f"Length in rowCount method: {len(self._data)}")

        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        print(f"Index in columnCount method: {index}")
        return len(self._data[0])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        data = [
          [4, 9, 2],
          [1, 0, 0],
          [3, 5, 0],
          [3, 3, 2],
          [7, 8, 9],
        ]

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)


app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec()


"""