from PySide6.QtWidgets import QComboBox,QWidget, QApplication, QVBoxLayout
import os
import sys
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        vert_layout = QVBoxLayout()
        combobox = QComboBox()
        combobox.addItems(["One", "Two", "Three"])

        combobox.currentIndexChanged.connect(self.index_changed) # the currentIndexChanged is a signal that is emited when the index value of QComboBox changes

        combobox.currentTextChanged.connect(self.text_changed) # signal is emited when the text changes in QComboBox

        vert_layout.addWidget(combobox)

        self.setLayout(vert_layout)

    def index_changed(self, index):
        print(index)
    
    def text_changed(self, text):
        print(f"text changed: {text}")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()