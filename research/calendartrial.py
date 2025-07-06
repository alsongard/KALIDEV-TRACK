from PySide6.QtWidgets import (
    QApplication, QPushButton, QWidget, QCalendarWidget, 
    QLabel, QVBoxLayout, QHBoxLayout, QLineEdit
)
from PySide6.QtCore import QDate
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        vLayout = QVBoxLayout()

        myCalender = QCalendarWidget()
        myCalender.setGridVisible(True)

        label = QLabel("Selection Date")

        vLayout.addWidget(myCalender)
        self.setLayout(vLayout)



app = QApplication()
window = MainWindow()
window.show()
exit_code = app.exec()
sys.exit(exit_code)