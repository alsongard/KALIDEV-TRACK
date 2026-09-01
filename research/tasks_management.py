from PySide6.QtWidgets import QTableView, QGroupBox, QWidget, QApplication, QMainWindow, QLabel,QVBoxLayout
from  PySide6 import QtCore
from PySide6.QtCore import Qt, QSize, QModelIndex
import sys
from read_task_file import ReadTaskFiles
# Model , View & Controller (MVC) : View & Controller are treated as one

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, mydata, myHeaderData): 
        super().__init__()
        self._data = mydata
        self.headers = myHeaderData
        self._column_keys = ["subtaskname", "description", "status"]

    # returns rowCount
    def rowCount(self, parent=QModelIndex()): 
        # print(f"this is index in rowCount: {index}")
        return len(self._data)

    # returns column count
    def columnCount(self, parent=QModelIndex()):
        # print(f" this is count in columnCount method: {len(self.data[0])}")
        return len(self._column_keys)

    # returns headers
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.headers[section])
            else:
                return str(section+1)

    # return value to displayed at given row & col index
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        # index is an instance from the QModelIndex , which provide methods row and column
        columns_from_dict = ["subtaskname", "description", "status"]

        if index.isValid():
            row = index.row()
            col = index.column()
            if role == Qt.ItemDataRole.DisplayRole  or role == Qt.ItemDataRole.EditRole: 
                # value =  str(self._data[index.row()][index.column()])
                # print(f"Display value at ({index.row()}, {index.column()}): {self._data[index.row()][index.column()]}")
                # return value
                # print(f"row value: {row}\ncol value: {col}")
                row_in_dict = self._data[row]
                key = self._column_keys[col]
                # print(f"dictionary row: {row_in_dict}")
                # print(f"Cell value: {row_in_dict[key]}")
                return str(row_in_dict.get(key, ""))
                
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

        self.verticalLayout =  QVBoxLayout()
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

        # trial on using dictionary to set Widgets and Table
        # for item_in_dict in returnedTaskData:

        self.projectName = QLabel()
        self.projectName.setText(returnedTaskData["project"])

            # phases key has the data for table
        for item in  returnedTaskData["phases"]: # item is a dictionary
            self.phaseContentGroupBox = QGroupBox() # GroupBox to enable styling
            self.phaseLayout = QVBoxLayout() # layout for the self.phaseContentGroupBox
            self.phaseTable = QTableView()
            self.phaseTable.wordWrapTrue = True
            
            self.phaseName = QLabel()
            self.phaseName.setText(item["name"])

            self.phaseGoal = QLabel()
            self.phaseGoal.setText(item["goal"])

            self.phaseName.setObjectName("phaseNameLabel")
            self.phaseGoal.setObjectName("phaseGoalLabel")


            self.phaseLayout.addWidget(self.phaseName)
            self.phaseLayout.addWidget(self.phaseGoal)
            # each_data = []
            # for subtasks in  item["subtasks"]:
            #     print('')

            header_data  = ["Module", "Description", "Status"] 
            self.model = TableModel(item["subtasks"], myHeaderData=header_data )
            self.phaseTable.setModel(self.model)
            self.phaseTable.resizeColumnsToContents()

            self.phaseLayout.addWidget(self.phaseTable)

            self.phaseContentGroupBox.setLayout(self.phaseLayout)
            self.verticalLayout.addWidget(self.phaseContentGroupBox)




        # using array for setting data to  QLable and QTable View 
        """
        for phase_content in returnedTaskData:
            self.phaseContentGroupBox = QGroupBox() # GroupBox to enable styling
            self.phaseLayout = QVBoxLayout() # layout for the self.phaseContentGroupBox
            self.phaseTable = QTableView()
            self.phaseTable.wordWrapTrue = True
            self.phaseName = QLabel()
            self.phaseName.setObjectName("phaseNameLabel")
            self.phaseGoal = QLabel()
            self.phaseGoal.setObjectName("phaseGoalLabel")



            print("this is a single phaseContent ")
            print(phase_content)
            self.phaseName.setText(phase_content[0]) # name
            self.phaseGoal.setText(f"Goal: {phase_content[1]}") # goal

            self.phaseLayout.addWidget(self.phaseName)
            self.phaseLayout.addWidget(self.phaseGoal)

            self.each_data = []

            for item in phase_content[2]: # array of dictionaries
                thetask = [item['subtaskname'], item["subtaskdescription"], item["subtaskstatus"]]
                self.each_data.append(thetask)


            print('this is all_sub_task_for_table')
            print(self.each_data)

            header_data = ["Module", "Description", "Status"]
            self.model = TableModel(self.each_data, header_data)
            self.phaseTable.setModel(self.model)
            self.phaseTable.resizeColumnsToContents()
            self.phaseLayout.addWidget(self.phaseTable)


            self.phaseContentGroupBox.setLayout(self.phaseLayout)
            self.verticalLayout.addWidget(self.phaseContentGroupBox)
        """

        self.central_widget.setLayout(self.verticalLayout)

        
        self.central_widget.setStyleSheet("""
            QGroupBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QLabel#phaseNameLabel {
                    padding-top: 5px;
                    padding-bottom: 5px;
                    padding-left: 10px;b
                    padding-right: 10px;
                    border-radius: 8px;
                    background-color: rgba(255, 255, 255, 0.1);   /* Semi‑transparent overlay for contrast */
                    color: #ffffff;                              /* Adjust text colour for dark background */
                    font-size: 18px;
                }
            }
            QLabel#phaseGoalLabel {
                font-style: italic;
                font-size: 14px;
                color: #9BBCE0;
                margin-bottom: 8px;
            }
        """)
    

        # self.setFixedSize(1200,600)
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


"""
output for dictionary row, col values
-------
row value: 0
col value: 0
dictionary row: {'subtaskname': 'db.sql', 'description': 'Master database initialization(schema creation, UUID extensions)', 'status': 'pending'}
Cell value: db.sql
row value: 0
col value: 1
dictionary row: {'subtaskname': 'db.sql', 'description': 'Master database initialization(schema creation, UUID extensions)', 'status': 'pending'}
Cell value: Master database initialization(schema creation, UUID extensions)
row value: 0
col value: 2
dictionary row: {'subtaskname': 'db.sql', 'description': 'Master database initialization(schema creation, UUID extensions)', 'status': 'pending'}
Cell value: pending
row value: 1
col value: 0
dictionary row: {'subtaskname': 'home.sql', 'description': 'Single-row table for Hero/Mission statement, Hero Image URL.', 'status': '✅ Completed'}
Cell value: home.sql
row value: 1
col value: 1
dictionary row: {'subtaskname': 'home.sql', 'description': 'Single-row table for Hero/Mission statement, Hero Image URL.', 'status': '✅ Completed'}
Cell value: Single-row table for Hero/Mission statement, Hero Image URL.
row value: 1
col value: 2
dictionary row: {'subtaskname': 'home.sql', 'description': 'Single-row table for Hero/Mission statement, Hero Image URL.', 'status': '✅ Completed'}
Cell value: ✅ Completed
"""