from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtWidgets import QApplication, QTableView, QVBoxLayout, QWidget

class CustomTableModel(QAbstractTableModel):
    def __init__(self, data, headers, parent=None):
        """
        Initialize the model with data and headers.
        
        Args:
            data: 2D list containing table data [[row1], [row2], ...]
            headers: List of column header strings
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        self._data = data
        self._headers = headers

    def rowCount(self, parent=QModelIndex()):
        """Return number of rows (length of data)"""
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        """Return number of columns (length of first row if exists, else 0)"""
        return len(self._data[0]) if self._data else 0

    def data(self, index, role=Qt.DisplayRole):
        """
        Return data for given index and role.
        
        Args:
            index: QModelIndex containing row/column
            role: Data role (DisplayRole = text, DecorationRole = icon, etc.)
        
        Returns:
            Data for the requested role at index
        """
        if not index.isValid():
            return None
            
        row = index.row()
        col = index.column()
        
        if role == Qt.DisplayRole:
            # Return text for display
            return str(self._data[row][col])
            
        elif role == Qt.TextAlignmentRole:
            # Align numbers right, text left
            value = self._data[row][col]
            if isinstance(value, (int, float)):
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter
            
        elif role == Qt.BackgroundRole:
            # Color code negative numbers
            value = self._data[row][col]
            if isinstance(value, (int, float)) and value < 0:
                return Qt.red  # Highlight negatives in red
        
        return None  # Default for unhandled roles

    def headerData(self, section, orientation, role):
        """
        Return header data for section (row/column index).
        
        Args:
            section: Index of header item
            orientation: Qt.Horizontal (columns) or Qt.Vertical (rows)
            role: Data role (usually DisplayRole for text)
        """
        if role != Qt.DisplayRole:
            return None
            
        if orientation == Qt.Horizontal:
            # Column header
            return self._headers[section] if section < len(self._headers) else None
        else:
            # Row header (show row numbers)
            return str(section + 1)

    def flags(self, index):
        """Return item flags (editable, selectable, etc.)"""
        base_flags = super().flags(index)
        return base_flags | Qt.ItemIsEditable  # Make cells editable

    def setData(self, index, value, role=Qt.EditRole):
        """
        Set data at index to value.
        
        Args:
            index: QModelIndex to modify
            value: New value to set
            role: Role being modified (EditRole for user edits)
        
        Returns:
            True on success, False on failure
        """
        if not index.isValid() or role != Qt.EditRole:
            return False
            
        row = index.row()
        col = index.column()
        
        try:
            # Convert to original type if possible
            original_type = type(self._data[row][col])
            if original_type == int:
                self._data[row][col] = int(value)
            elif original_type == float:
                self._data[row][col] = float(value)
            else:
                self._data[row][col] = value
                
            # Notify views that data changed
            self.dataChanged.emit(index, index, [role])
            return True
        except ValueError:
            return False

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Sample data
        data = [
            ["Product A", 150, 12.99],
            ["Product B", -25, 24.50],  # Negative for demo
            ["Product C", 300, 8.75],
            ["Product D", 80, 32.00]
        ]
        
        headers = ["Product Name", "Stock", "Price"]
        
        # Create model and view
        self.model = CustomTableModel(data, headers)
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        
        # Configure view
        self.table_view.resizeColumnsToContents()
        self.table_view.setAlternatingRowColors(True)
        
        # Setup layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        self.setLayout(layout)
        
        # Window settings
        self.setWindowTitle("Custom Table Model Demo")
        self.resize(600, 400)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()