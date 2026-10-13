"""
button_delegate.py 


Purpose: 
    Provides the ButtonDelegate class used in home_view.py for the HomeTable(QTableView)
    It is used to draw a button on the View

Exports:
    ButtonDelegate
"""

from PySide6.QtWidgets import QStyle, QApplication, QStyleOptionButton,  QPushButton, QStyledItemDelegate
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QEvent, Signal

class ButtonDelegate(QStyledItemDelegate):
    # Delegate that paints a button in a cell and handles it's clicks"


    button_clicked = Signal(int) # emits row index when clicked

    # def paint(self, painter, option, index):
    #     # Draw the button using the Style system
    #     btn_option = QStyleOptionButton()
    #     btn_option.react = option.rect
    #     btn_option.text = "Open"
    #     btn_option.state = QStyle.State_Enabled | QStyle.State_Active

    #     QApplication.style().drawControl(
    #         QStyle.CE_PushButton, btn_option, painter
    #     )

    def paint(self, painter, option, index):
        # Draw the button using the style system
        btn_option = QStyleOptionButton()
        btn_option.rect = option.rect
        btn_option.text = "Open"
        btn_option.state = QStyle.State_Enabled | QStyle.State_Active

        QApplication.style().drawControl(
            QStyle.CE_PushButton, btn_option, painter
        )
        # print(f"option.rect: {option.rect}")
        # print(f"ption.text: {btn_option.text}")
        """
            option.rect: PySide6.QtCore.QRect(716, 60, 99, 29)
            option.text: Open
        """
    def editorEvent(self, event, model, option, index):
        # Detect mouse release on the button area
        if (event.type() == QEvent.MouseButtonRelease):
            if (option.rect.contains(event.pos())):
                self.button_clicked.emit(index.row())
                return True
        return False

        