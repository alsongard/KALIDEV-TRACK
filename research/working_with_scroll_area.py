from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGroupBox, QScrollArea, QWidget, QApplication, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()


        main_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.widget = QWidget()
        self.vert_layout = QVBoxLayout()

        self.address_count = 1

        self.address_label_array = []
        self.address_lineedit_array = []

        title_label = QLabel('Address Information')
        addAddressBtn = QPushButton("Add another address")
        addAddressBtn.clicked.connect(self.add_address)

        self.vert_layout.addWidget(title_label)
        self.vert_layout.addWidget(addAddressBtn)

        self.set_address() # called once to add the QGroupBox for an address
        self.widget.setLayout(self.vert_layout)

        self.scroll_area.setWidget(self.widget)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)

        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)

    

    def set_address(self):
        address_label = QLabel("Add address below")
        address_input = QLineEdit()

        self.address_label_array.append(address_label)
        self.address_lineedit_array.append(address_input)

        saveBtn = QPushButton("Save")
        g = QGroupBox(f"Address  {self.address_count}")
        g_layout = QVBoxLayout()
        g_layout.addWidget(address_label)
        g_layout.addWidget(address_input)
        g_layout.addWidget(saveBtn)

        g.setLayout(g_layout)

        self.vert_layout.addWidget(g)

        

    def add_address(self):
        self.set_address()


app = QApplication([])
window = MainWindow()
window.show()

app.exec()