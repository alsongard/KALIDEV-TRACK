from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout

app = QApplication()


window = QWidget()

ver_layout = QVBoxLayout()
okay_1 = QPushButton("Okay user 1")

ver_layout.addWidget(okay_1)



user_2 = QPushButton("Okay User 2")
ver_layout.addWidget(user_2)


ver_layout.addStretch(0)

window.setLayout(ver_layout)
window.show()
app.exec()