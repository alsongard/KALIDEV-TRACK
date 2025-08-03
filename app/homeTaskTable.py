from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex


class TableModel(QAbstractTableModel):
    def __init__(self, UserData, headerData):
        super().__init__()
        self.myData = UserData # assign data to myData: data will be passe to the class on creating object/instance
        self.headers = headerData


    def rowCount(self, parent=QModelIndex()):
        # print(f"Number of rows of myData:  {len(self.myData)}")
        return len(self.myData)

    def columnCount(self, parent=QModelIndex()):
        # print(f"Number of column is {len(self.myData[0])}") # row index 1  : basically length counts the number of items in an iterable: array we have 2 items: 2 columns
        if len(self.myData[0]) == 0:
            # print(f"Returning 0")
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
        
