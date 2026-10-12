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


## Working with QStyledItemDelegate
The class above is used to add widgets to a TableView. It sits in between/middle of the Model and the  View. 

To use QStyledItemDelegate you subclass a class , which provides the below methods:
- ``paint(QPainter *painter, const QStyleOptionViewItem &option, const QModelIndex &index) ``
this is where you draw the custom content for the item. 

- ``createEditor(QWidget *parent, const QStyleOptionViewItem &option, const QModelIndex &index)``
the createEditor method enables the creationg of the custom widget (Like a QSpinBox or QComboBox) used for editing an item

- ``setEditorData(QWidget *editor, const QModelIndex &index)``
The setEditorData method transfers data from the model to your custom widget
 

- ``setModelData(QWidget *editor, QAbstractItemModel *model, const QModelIndex &index)``
This transfers data from your custom editor widget back to the model

- ``updateEditorGeometry(QWidget *editor, const QStyleOptionViewItem &option, const QModelIndex &index)``
This positions and sizes the editor widget correctly.


Further information from docs:
QStyledItemDelegate is the default delegate that is used by all QItem Views e.g QTableView

``displayText (value, local)`` This function returns the string that the delegate will use to display the Qt::DisplayRole of the model in locale. value is the value of the Qt::DisplayRole provided by the model.

does this method state that it sets the text for a button.

Also i have some further questions:
- why not use QPushButton and use QStyleOptionButton. What is the difference
