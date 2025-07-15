from PySide6.QtWidgets import QApplication, QWidget, QTableView,  QVBoxLayout
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
import sys
class TableModel(QAbstractTableModel):
    def __init__(self, UserData, headerData):
        super().__init__()
        self.myData = UserData # assign data to myData: data will be passe to the class on creating object/instance
        self.headers = headerData


    def rowCount(self, parent=QModelIndex()):
        print(f"Number of rows of myData:  {len(self.myData)}")
        return len(self.myData)

    def columnCount(self, parent=QModelIndex()):
        print(f"Number of column is {len(self.myData[0])}") # row index 1  : basically length counts the number of items in an iterable: array we have 2 items: 2 columns
        if len(self.myData[0]) == 0:
            print(f"Returning 0")
            return 0
        else:
            return len(self.myData[0])
    
    def headerData(self, section, orientation, role=Qt.DisplayRole): # this methods returns a string for the header
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.headers[section])
            else:
                return str(section+1)
            

    def data(self, index, role=Qt.DisplayRole): # The `data` method must return the data as a string. We are doing `str(self.myData[row][col])` which is correct.
        # this methods returns data for the given index and role
        # index: QModelIndex containing row and column
        # role : data role, (DisplayRole=text, decorationRole=icon)
        row = index.row()
        col = index.column()

        if role == Qt.DisplayRole:
            # print(str(self.myData[row][col])) won't work
            return str(self.myData[row][col])
        
            
    

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        myHeaders = ["Task", "Priority","Start Date", "End Date",  "Status"]
        users_data = [
            ["FreeCodeCamp JavaScript & DataStructures", "10", "2025-07-07", "2025-07-10", "In progress"],
            ["KaliDev-Track","10", "2025-07-07", "2025-07-10", "Upcoming"],
            ["ANN", "10", "2025-07-07", "2025-07-10", "Finished"]
        ]
        vLayout=QVBoxLayout()
        model = TableModel(users_data, myHeaders)
        myTable = QTableView()
        myTable.setModel(model)
        myTable.setColumnWidth(0, 350)
        vLayout.addWidget(myTable)
        self.setGeometry(0, 0, 800,500)

        self.setLayout(vLayout)

app = QApplication()
window = MainWindow()
window.show()
exit_code = app.exec()
sys.exit(exit_code)
"""
QAbstractionTableModel is used for customizing tables. The QTableView is used for creating tables but is limited/offers little.
QAbstractionTableModel lets you define your own spreadsheet-like data and tell Qt how to display, access, and edit it — without using predefined widgets like QTableWidget. For large dynamic data, QAbstractionTableModel is needed.

To use QAbstractionTableModel you subcass:inherit it:

| Method              | What it does                                                       |
| ------------------- | ------------------------------------------------------------------ |
| `rowCount()`        | Returns the number of rows                                         |
| `columnCount()`     | Returns the number of columns                                      |
| `data(index, role)` | Returns the data for a given row/column (`index`) and display role |
| `headerData()`      | Sets header labels (row numbers, column names)                     |
| `setData()`         | (Optional) Allows editing data in the model                        |
| `flags()`           | (Optional) Specifies whether a cell is editable, selectable, etc.  |


why pass parent argument to __init__() constructor. the parent argument is important in qt as it manages hierachy, ownership and memory management.
When creating a QWidget object or QWidget, nearly all of them accept parent argument.e.g. (QWidget, QLabel, QAbstractTableModel, etc.)
```python
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__
```

Uses
1. Hierachy/Ownership
when a Qwidget has a parent this establishes hierarchy. When the parent widget is destroyed so does the child widget/object


2. Memory Management (Automatic Deletion)
- Qt uses parent-child trees to manage memory.
- If a widget has no parent, you must delete it yourself (especially in C++).
- In Python, the garbage collector does this, but Qt's system helps avoid memory leaks and dangling pointers.


Signal Routing & Event Filtering
    In advanced use cases, parent lets you filter or intercept events from child widgets.
    It also helps with scoped object names, signal-slot management, etc.


In QAbstractionTableModel is has already predefined methods that should be used for setting headers, getting data, setting data to display, ... e.t.c

```python

# the method for getting data in QAbstractionTableModel is ``def data()``
# the method for getting headers in QAbstractionTableModel  is ``def headerData()``
```
"""