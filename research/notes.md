## Manipulating data in QTableView
From the docs this involves 2 functions : flags, setData in the model
Remember that the model drives the data to the View .

- setup the flag() method in your method
```py
def flags(self, index):
    return (
        Qt.ItemFlag.ItemIsSelectable 
        | Qt.ItemFlag.ItemIsEnabled
        | Qt.ItemFlag.ItemIsEditable
    )

```




-  the next method is using setData(). 
This method is the model's interface between Qt and your data object. It takes care of making the changes to the data.

```py
def setData(self, index, value, role ):
    if role == Qt.ItemDataRole.EditRole:
        self._data[index.row()][index.column()] = value
        return True
```

However , using the above method will result in   the entire current cell data being erased. To enable editing of a cell, with it's information you will need to return it's current value and the updated value. Without this every time you select a Table Cell, the cells becomes empty

```py
def setData(self, index, value, role ):
    if role == Qt.ItemDataRole.EditRole:
        current_value = self._data[index.row()][index.column()]
        self._data[index.row()][index.column()] = current_value +  value
        return True
```