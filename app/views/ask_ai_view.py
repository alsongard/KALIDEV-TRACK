"""
ask_ai_view.py

Purpose:
    Proviedes a view for the Ask AI feature in the application. This view allows users to input their questions and receive answers from the AI model.


Depends:
    utils.config_manager.ConfigManager


"""
from re import S
import re
from typing import Container
from PySide6.QtWidgets import QApplication, QGroupBox, QHBoxLayout, QTextEdit, QScrollArea, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit
from PySide6.QtCore import Qt, Signal
from ollama import chat
import logging
from rich.logging import RichHandler


from app.utils.config_manager import ConfigManager

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger(__name__)


class AskAIView(QWidget):
    """
    Class AskAIView provides a user interface for the Ask AI feature

    Class Attributes:

    """
    closed = Signal()
    def __init__(self):
        """
        Initializes the AskAIView class and sets up the user interface components.
        """
        super().__init__()
        self.setWindowTitle("Ask AI")

        self.main_layout = QVBoxLayout()
        ai_assistant_label = QLabel("Your AI Assistant: ")
        self.messages = []
        self.main_layout.addWidget(ai_assistant_label)

        self.setGeometry(100, 100, 400, 200)

        # Create UI components
        question_label = QLabel("Enter your question:")
        self.main_layout.addWidget(question_label)

        hor_layout = QVBoxLayout()

        self.question_input = QTextEdit()
        self.question_input.setPlaceholderText("Type your question here...")
        self.question_input.setMaximumHeight(50)
        self.ask_button = QPushButton("Ask")
        self.ask_button.setCheckable(True)
        self.ask_button.clicked.connect(self.ask_ai)

        hor_layout.addWidget(self.question_input, alignment=Qt.AlignmentFlag.AlignTop)
        hor_layout.addWidget(self.ask_button, alignment=Qt.AlignmentFlag.AlignRight)


        self.main_layout.addLayout(hor_layout)


        self.container = QGroupBox() # groupbox to be set for the generated response
        container_layout = QVBoxLayout() # groupbox layout

        self.scroll_area = QScrollArea() # scroll_area used for the responses , enable scrolling
        scroll_widget = QWidget() # widget for the scroll_area
        self.scroll_widget_layout = QVBoxLayout() # layout for the scroll_area


        scroll_widget.setLayout(self.scroll_widget_layout) 
        self.scroll_area.setWidget(scroll_widget)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)

        container_layout.addWidget(self.scroll_area)

        self.container.setLayout(container_layout)

        self.main_layout.addWidget(self.container)

        self.setLayout(self.main_layout)


    def ask_ai(self, checked):
        """
        Method ask_ai is a slot method that is used to send  a message to the chat model

        Args:
            checked (bool) : a boolean value representing the status of the QPushButton
        """
        
        if checked:
            self.ask_button.setChecked(False)
            question = self.question_input.toPlainText()
            message = [{
                "role": "user", 
                "content": question
            }]

            response = chat(model="qwen2.5:0.5b", messages=message)
            logger.debug("response message body: %s", response.message)
            logger.debug("response: %s", response.message.content)

            self.messages.append(response.message)

            self.add_to_response_layout(question, response.message.content)


    def add_to_response_layout(self, question, answer):
        """
        Method add_to_response_layout is used to add the generated response(answer) provided by your model.

        Args: 
            content(string) : answer to the question

        Return: 
            None
        """
        # question_text_edit = QTextEdit()
        # answer_text_edit  = QTextEdit()
        # question_text_edit.setMarkdown(question)
        # answer_text_edit.setReadOnly(True)
        # question_text_edit.setReadOnly(True)
        # question_text_edit.setMaximumHeight(50)
        # question_text_edit.setMinimumWidth(100)

        # answer_text_edit.setMarkdown(answer)
        # self.scroll_widget_layout.addWidget(question_text_edit, alignment=Qt.AlignmentFlag.AlignRight)
        # self.scroll_widget_layout.addWidget(answer_text_edit)

        # self.scroll_widget_layout.addStretch(0)


        question_label = QLabel(question)
        question_label.setWordWrap(True) # allows text to wrap to next line
        question_label.setMinimumWidth(400)
        question_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        question_label.setStyleSheet("""
            background-color: #919191;
            border-radius: 10px;
            border: 2px solid #748F8B;
            padding: 10px;
            font-size: 14px;
        """)

        self.scroll_widget_layout.addWidget(question_label, alignment=Qt.AlignmentFlag.AlignRight)

        # --- AI Answer Bubble ---
        answer_label = QLabel(answer)
        answer_label.setWordWrap(True)
        # answer_label.setMinimumWidth(400)
        answer_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        answer_label.setStyleSheet("""
            background-color: rgba(57, 57, 57, 51);
            border-radius: 10px; 
            border: 2px solid #524B4B;
            padding: 10px;
            font-size: 14px;
        """)
        self.scroll_widget_layout.addWidget(answer_label)
        
        self.ask_button.setChecked(False)
        # Add a spacer to push everything up
        self.scroll_widget_layout.addStretch(1)

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)



