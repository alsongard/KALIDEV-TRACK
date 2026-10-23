from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QGroupBox, QVBoxLayout, QLabel, QPushButton, QApplication


class AddingWidgetsExampleOne(QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QVBoxLayout()
        self.label = QLabel("Welcome to Trial")
        self.add_address = QPushButton("Click to add label")
        self.add_address.clicked.connect(self.adding_new_widget)
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.add_address)
        self.setLayout(self.mainLayout)

    def adding_new_widget(self):
        new_label = QLabel("Hi My Name is Mars")
        self.mainLayout.addWidget(new_label)


class AddingWidgets(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.address_count = 1
        self.input_array = []
        self.label_array = []

        # GroupBox for holding UI Components
        self.groupBox = QGroupBox()

        # layout for the groupBox
        self.vert_layout = QVBoxLayout() 

        label = QLabel(f"Address {self.address_count}: ")
        address_input = QLineEdit()
        self.input_array.append(address_input)
        self.label_array.append(label)
        self.vert_layout.addWidget(label)
        self.vert_layout.addWidget(address_input)
        self.groupBox.setLayout(self.vert_layout)

        self.main_layout.addWidget(self.groupBox)

        # button layout
        button_layout = QHBoxLayout()
        self.add_address = QPushButton("Add Address")
        self.add_address.clicked.connect(self.adding_new_widget)
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_address_info)
        button_layout.addWidget(self.add_address)
        button_layout.addWidget(self.save_btn)

        self.main_layout.addLayout(button_layout)

        

    def adding_new_widget(self):
        self.address_count+=1 
        label = QLabel(f"Address {self.address_count}")
        address_input = QLineEdit()
        self.vert_layout.addWidget(label)
        self.vert_layout.addWidget(address_input)

        self.label_array.append(label)
        self.input_array.append(address_input)

    

    def save_address_info(self):
        for index, input_component in enumerate(self.input_array):
            print(f"Index: {index}\t {input_component.text()}")



app = QApplication([])
window = AddingWidgets()
window.show()
app.exec()