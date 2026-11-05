"""
task_table_model.py 

Purpose: 
    Provides the TaskTableModel used for TaskView
    The Model is used to drive the view 


Exports:
    TaskTableModel
"""

from  PySide6 import QtCore
from PySide6.QtCore import Qt, QModelIndex
import logging

logger = logging.getLogger(__name__)
# Model , View & Controller (MVC) : View & Controller are treated as one
class TaskTableModel(QtCore.QAbstractTableModel):
    """

    """
    
    def __init__(self, mydata, myHeaderData): 
        super().__init__()
        self._data = mydata
        self.headers = myHeaderData
        self._column_keys = ["Module", "Description", "Status"]

    # returns rowCount
    def rowCount(self, parent=QModelIndex()): 
        # print(f"this is index in rowCount: {index}")
        return len(self._data)

    # returns column count
    def columnCount(self, parent=QModelIndex()):
        # print(f" this is count in columnCount method: {len(self.data[0])}")
        return len(self._column_keys)

    # returns headers
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.headers[section])
            else:
                return str(section+1)

    # return value to displayed at given row & col index
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        # index is an instance from the QModelIndex , which provide methods row and column
        columns_from_dict = ["module name", "module description", "status"]

        if index.isValid():
            row = index.row()
            col = index.column()
            if role == Qt.ItemDataRole.DisplayRole  or role == Qt.ItemDataRole.EditRole: 
                # return value
                # value =  str(self._data[index.row()][index.column()])
                # print(f"Display value at ({index.row()}, {index.column()}): {self._data[index.row()][index.column()]}")
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

            # get the row and index
            row = index.row()  # represents the dictionary row index in list
            column = index.column() # represents the column which can be mapped to the key

            key = self.headers[column].lower()


            # logger.debug("Data edited on row: %s , key %s", row, key)

            # logger.debug("Data changed from: %s", self._data[row][key])
            # logger.debug("To: %s", value)

            self._data[row][key] = value
            return True
        return False

    
    # enables editing
    def flags(self, index): 
        return (
            Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEnabled 
            | Qt.ItemFlag.ItemIsEditable
        )
        
