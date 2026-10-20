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


## QWidget
What is a QWidget:this is an empty GUI widget
```py
window = QWidget()
window.show()
```

**How to use try except else finally block**

We use the try block to run code , if an error occurs this error is handled gracefully by the catch block
The else block runs the code when either try or catch block is executed
The finally block will always run if either the try or catch block is executed
```py
try:
    print(x)
except: 
    print("Error: X is undefined")
else:
    print("Status: ")
finally:
    return 0 # return 1
```


QMessageBox built in Interfaces/Methods for displaying messages:
```py
QMessageBox.warning(
	self,
	"Warning", 
	"Your subscribtion will expire in 3 days. Please renew to avoid service interruption"
	buttons=QMessageBox.StandardButton.Ok
)


QMessageBox.information(
        self,
        "Information",
        "Your tax return has been successfully submitted.",
        buttons=QMessageBox.StandardButton.Ok
)
QMessageBox.critical(
        self,
        "Error",
        "Failed to connect to the server. Please check your internet connection and try again.",
        buttons=QMessageBox.StandardButton.Ok
)
QMessageBox.question(
        self,
        "Confirm Action",
        "Are you sure you want to delete this file? This action cannot be undone.",
        buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        defaultButton=QMessageBox.StandardButton.No
)
```

Error : Positional argument error
Positional argument: not parameter name is used when passing the argument
Keyword argument: key=argument

Python requires that all positional argument come before keyword argument
```py
def sum(a, b, c):
	return a + b + c

print(sum(a=2, 4, c=8)) # results in the error: Positional argument error

print(sum(2, 4, c=8)) # this works
```


## Signals
To pass a signal from your child window widget to parent we use the Signal() class
```py
class ChildWindow(QWidget):
    closed = Signal()


    def __init__(self):
        super().__init__()
        exitBtn = QPushButton("Exit")
        exitBtn.clicked.connect(self.close_window)

    # custom method 
    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def close_window(self):
        self.close() # this method is used for closing the window

class ParentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.childW = None

        openChildBtn = QPushButton("Open Child")

    
    def to_open_child_window(self):
        if self.childW is None:
            self.childW = ChildWindow()
            self.childW.closed.connect(self.on_child_window_run)
            self.childW.show()
        else:
            if self.childW is not None:
                self.childW.close()
                self.childW = None

    def on_child_window_run(self):
        self.childW = None
```
- ``self.close()`` this is a built in method inherited from QWidget (and its ancestor QObject). When you call it:
- Qt generates a close event
- The event is delivered to the widgets closeEvent() handler. *the custom method ``closeEvent(self,event)``*
- if ``closeEvent()`` method accepts the event, which is the same as ``super().closeEvent(self, event)`` the widget is hidden and closes.


```
User clicks "Exit" in child
        │
        ▼
exitBtn.clicked → self.close_window() → self.close()
        │
        ▼
Qt creates a QCloseEvent and calls ChildWindow.closeEvent(event)
        │
        ├── self.closed.emit() ────► Parent.on_child_window_run()
        │                                 └── self.childW = None
        │
        └── super().closeEvent(event) → QWidget hides the window
```


## Logging
To setup logger, we do the following:
```py
import logging

# settup the logger
loggin.basicConfig(
    level=logging.DEBUG, # the level of logger e.g DEBUG, INFO
    format="%s(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
    datefmt="[%x]", 
)

logger = logging.getLogger(__name__)

logger.debug("info is correct")
```


## Refreshing QTableView using QAbstractTableModel 

QAbstractTableModel refresh after data change beginResetModel endResetModel

To notify  any view such as (QTableView or QListView) whose data is passed through the a model of changes on data, we use the function ``endResetModel()``. 
it's part of a pair with the ``beginResetModel()`` method.  Both methods must be called within the table Model.
Example:
```py
def udpateDate(const QModelIndex& index, const QVariant^ value, newData) {
    beginResetModel()
    self._data = newData
    endResetModel()
}
```

While the above method works, it is expensive. Only use it incases you are entering a new csv file e.t.c


In a small case, where you're removing rows use the below:
```py
removeRow(int row) {
    if (row < 0 || row >= rowCount(QModelIndex())) {
        return;
    }

    beginRemoveRows(QModelIndex(), row, row);

    // ... remove the item from your internal data structure ...

    endRemoveRows();
}
```

**Using Comprehension**
```py
self._display_projects = [
	{k: v for k,v in p.items() if k in keys}
	for p in self._all_projects
	if p.get("project_status").lower() == "completed" or p.get("project_status").lower() == "finished"
]
```



## Using DocStrings for file module, class and function 
Examples:

- **DocStrings for File Modules**
```py
"""
home_view.py

Purpose:
    Provides the main landing view for KALIDEV-TRACK.
    Displays a table of projects and the action buttons for managing them.

Depends on:
    - models/home_table_model.HomeTableModel
    - views/project_page.ProjectViewAdd
    - utils.file_operations.load_projects

Exports:
    HomeView
"""
```

- **DocStrings for Class**
```py
class TableModel(QAbstractTableModel):
    """
    Read-only table model that maps a 2D list to a QTableView.

    Attributes:
        _data (list[list]): Row-major data, e.g. [["A", 1], ["B", 2]]
        _headers (list[str]): Column header labels.

    Example:
        >>> model = TableModel([["A", 1]], ["Name", "Count"])
        >>> model.rowCount()
        1
    """
```

- **DocStrings for functions**
```py
def load_projects(project_dir: str) -> list[dict]:
    """
    Read all project JSON files from the given directory.

    Args:
        project_dir (str): Absolute path to the PROJECTS folder.

    Returns:
        list[dict]: Each dict has keys:
            - project_name (str)
            - status       (str)
            - phases       (list[dict])

    Raises:
        FileNotFoundError: If project_dir does not exist.

    Example:
        >>> load_projects("/home/user/PROJECTS")
        [{'project_name': 'my-app', 'status': 'Active', ...}]
    """
```




# UI Components
The below shows some of the most common Widgets:
- QLineEdit
QLineEdit is used to get user input 

**Common methods**
- setText(): this sets the text for the QLineEdit
- clear(): this clear the text  in the QLineEdit
- text() : get's the text (retrieves the text from the user)





## TOML 
Tom Obvious Minimal Language

**Why use TOML**
- TOML in Python refers to a minimal configuration file format that’s convenient to read and parse.
- TOML files are primarily used for configuration, separating code from settings for flexibility.
pyproject.toml is crucial for package configuration and specifies the build system and dependencies.
- Loading a TOML file in Python involves using tomli or tomllib to parse it into a dictionary, with tomlib being the standard in pythob


## Which Packages to Add to Dependency or build
using the command below:

1. Install the package: 
```bash
pip install pipdeptree

pipdeptree
# the output of this command is a tree of packages

# e.g
Send2Trash==2.1.0
watchfiles==1.2.0
┗━━ ✓ anyio required: >=3.0.0 installed: 4.14.2
    ┗━━ ✓ idna required: >=2.8 installed: 3.19
```
Add packages that are not tested, from which you could determine if it's a dependency or not


2. Using the command:
```bash
pip show <package_name>
```
