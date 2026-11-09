
from PySide6.QtWidgets import QApplication, QGraphicsPixmapItem, QHBoxLayout, QPushButton, QTableView, QVBoxLayout, QWidget
from PySide6 import QtCore
from PySide6.QtCore import Qt
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)

class TableModel(QtCore.QAbstractTableModel):
    """
    """
    def __init__(self, data, header_data):
        super().__init__() # call the constructor of the QAbstractTableModel
        self._data = data
        self._header_data = header_data


    def rowCount(self, index):
        # returns the length of the entire data
        # logger.debug("rowCount: %s", len(self._data))
        return len(self._data)

    def columnCount(self, index) -> int:
        # returns the length of the columns e.g for row 0 same as others
        # logger.debug("columnCount: %s", len(self._data[0]))
        return len(self._data[0])



    def headerData(self, section: int, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._header_data[section]

    def data(self, index, role):
        if index is None:
            return None

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            # logger.debug("Index:  %s", index)
            # logger.debug("row: %s, column: %s", index.row(), index.column())
            
            # get dictionary in list for the current row
            row_dict = self._data[index.row()]

            # get column key using index.column() 
            column_key = self._header_data[index.column()]
            

            value = row_dict.get(column_key, "") # retrieves value from the dictionary

            # logger.debug("Value: %s", value)
            return str(value)
        return None    


    # setting editable methods
    def flags(self, index):
        return (
            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
        )

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:

            # index has 2 properties row and column
            # row returns the row
            # column returns the key

            row_num = index.row()

            column_num  = index.column()

            key = self._header_data[column_num]

            self._data[row_num][key] = value # value is was the user inserts
            return True

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position+ rows -1)
        logger.debug("position: %s, rows: %s, ", position, rows)
        position = len(self._data) 
        for i in range(rows):
            empty_dict ={"id": " ","first_name": "","last_name": "","email": "","gender": "","University": ""}
            self._data.insert(position, empty_dict)
        self.endInsertRows()
        # self.layoutChanged.emit()
        return True

    def removeRows(self, position, rows,  parent = QtCore.QModelIndex()) -> bool:
        logger.debug("position: %s, rows: %s", position, rows)
        self.beginRemoveRows(parent, position, position + rows - 1)
        for i in range(rows):
            del self._data[position]
        self.endRemoveRows()
        # self.layoutChanged.emit()
        return True



class StudentTable(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Table Practise")
        self.main_layout = QVBoxLayout()

        student_data = [
            {"id": 1,"first_name": "Brennan","last_name": "Roscow","email": "broscow0@patch.com","gender": "Male","University": "Niigata University of International and Information Studies"}, 
            {"id": 2,"first_name": "Marmaduke","last_name": "Lemm","email": "mlemm1@buzzfeed.com","gender": "Bigender","University": "Utsunomiya University"}, 
            {"id": 3,"first_name": "Niccolo","last_name": "Idwal Evans","email": "nidwalevans2@biblegateway.com","gender": "Non-binary","University": "Physical Education Academy Jedrzej Sniadecki in Gdansk"}, 
            {"id": 4,"first_name": "Brooke","last_name": "Hosby","email": "bhosby3@japanpost.jp","gender": "Female","University": "Guilan University of Medical Sciences"}, 
            {"id": 5,"first_name": "Eugenius","last_name": "Abramzon","email": "eabramzon4@4shared.com","gender": "Male","University": "Hokkaido University of Health Sciences"}, 
            {"id": 6,"first_name": "Zacharias","last_name": "Rustman","email": "zrustman5@friendfeed.com","gender": "Male","University": "Sree Rama Krishna Degree College"}, 
            {"id": 7,"first_name": "Rich","last_name": "Ruffell","email": "rruffell6@biblegateway.com","gender": "Male","University": "Universidad Católica de Ávila"},
            {"id": 8,"first_name": "Eilis","last_name": "Hamlington","email": "ehamlington7@privacy.gov.au","gender": "Female","University": "Guru Ghasidas University"},
            {"id": 9,"first_name": "Mendel","last_name": "MacCambridge","email": "mmaccambridge8@xing.com","gender": "Male","University": "Fachhochschule Aschaffenburg"}, 
            {"id": 10,"first_name": "Blaire","last_name": "Daughtry","email": "bdaughtry9@smugmug.com","gender": "Female","University": "St. Mary's University of Minnesota"}
        ]

        logger.debug("type of student_data : %s", type(student_data[0])) # list type(student_data) , dict type(student_data[0])

        data = [
          [4, 9, 2],
          [1, 0, 0],
          [3, 5, 0],
          [3, 3, 2],
          [7, 8, 9],
        ]

        header_data = ["id", "first_name", "last_name", "email", "gender", "University"]
        self.model = TableModel(student_data,  header_data=header_data)
        self.myTable = QTableView()
        self.myTable.setModel(self.model)

        self.main_layout.addWidget(self.myTable)

        hor_layout = QHBoxLayout()
        insertBtn = QPushButton("Insert Row")
        removeBtn = QPushButton("Remove Row")
        insertBtn.clicked.connect(self.insert_row)
        removeBtn.clicked.connect(self.remove_row)

        hor_layout.addWidget(insertBtn)
        hor_layout.addWidget(removeBtn)
        self.main_layout.addLayout(hor_layout)

        self.setMinimumSize(400, 400)
        self.setLayout(self.main_layout)
        
    def remove_row(self):
        """
        Method remove_row is used to remove row in the table from current selected row
        """

        index = self.myTable.currentIndex()
        self.model.removeRows(index.row(), 1)

    def insert_row(self):
        """
        Method insert_row is used to insert a row at the table based on the ucrrent selectd row
        """
        index = self.myTable.currentIndex()
        self.model.insertRows(index.row(), 1)
        

app = QApplication([])
window = StudentTable()
window.show()
app.exec()