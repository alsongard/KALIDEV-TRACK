from PySide6.QtWidgets import QApplication, QWidget, QDateTimeEdit, QCalendarWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import QDate
class SmallWindow(QWidget):
    def __init__(self):
        super().__init__()

        vertLayout = QVBoxLayout()
        dateTimeEditObject = QDateTimeEdit()
        dateTimeEditObject.setMinimumDate(QDate.currentDate())
        endDateProjectTime = QDateTimeEdit()
        endDateProjectTime.setMinimumDate(QDate.currentDate())
        startDateLabel = QLabel('Starting Date')
        endDateLabel = QLabel('Ending Date')

        vertLayout.addWidget(startDateLabel)
        vertLayout.addWidget(dateTimeEditObject)
        vertLayout.addWidget(endDateLabel)
        vertLayout.addWidget(endDateProjectTime)

        # trial on displaying QCalendarWidget
        trialCalendarPopUp = QDateTimeEdit()
        trialCalendarPopUp.setCalendarPopup(True)
        vertLayout.addWidget(trialCalendarPopUp)

        self.setLayout(vertLayout)


app = QApplication()
window = SmallWindow()
window.show()
app.exec()
        