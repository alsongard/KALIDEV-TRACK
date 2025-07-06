from PySide6.QtWidgets import QApplication, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
import sys
class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("qFrame practise")
        mainHorLayout = QHBoxLayout()


        mainFrame = QFrame()
        mainFrame.setFrameShape(QFrame.Shape.Panel)
        # mainFrame.setFrameShadow(QFrame.Shadow.Raised)
        mainFrame.setLineWidth(2)

        v_layout = QVBoxLayout()
        okayBtn = QPushButton('Okay')
        v_layout.addWidget(okayBtn)
        mainFrame.setLayout(v_layout)

    
        mainHorLayout.addWidget(mainFrame)

        self.setLayout(mainHorLayout)

app = QApplication(sys.argv)
window = MainApp()
window.show()
app.exec()

"""
QFrame is a versatile widget that provides a way to group other widgets and apply different styles. 
The QFrame class can also be used directly for creating simple placeholder frames without any contents.

The frame style is specified by a frame shape and a shadow style that is used to visually separate the frame from surrounding widgets. These properties can be set together using the setFrameStyle() function and read with frameStyle() .

The frame shapes are NoFrame , Box , Panel , StyledPanel , HLine and VLine ; the shadow styles are Plain , Raised and Sunken .

A frame widget has three attributes that describe the thickness of the border: lineWidth , midLineWidth , and frameWidth .
    The line width is the width of the frame border. It can be modified to customize the frame’s appearance.
    The mid-line width specifies the width of an extra line in the middle of the frame, which uses a third color to obtain a special 3D effect. Notice that a mid-line is only drawn for Box , HLine and VLine frames that are raised or sunken.

    The frame width is determined by the frame style, and the frameWidth() function is used to obtain the value defined for the style used.


from other examples it seems that adding a widget to frame object is impossible however you can add a layout:
```python
mainFrame = QFrame()
v_layout =  QVBoxLayout()
okBtn = QPushButton("Okay")
cancelBtn = QPushButton("Cancel")
v_layout.addButton(cancelBtn)
mainFrame.setLayout(v_layout) # remember we use setLayout()

"""