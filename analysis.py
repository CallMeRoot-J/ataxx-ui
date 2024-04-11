from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QTextEdit


class analysis(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.textarea = QTextEdit(self)
        self.scrollBar = self.textarea.verticalScrollBar()

        self.init_widget()

    def init_widget(self):
        self.setMinimumSize(640, 560)
        self.textarea.setMinimumSize(self.width(), self.height()-50)
        self.textarea.move(0, 50)
        self.textarea.setFont(QFont('Aria', 8))
        self.textarea.setReadOnly(True)
        self.textarea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollBar.valueChanged.connect(self.textarea.verticalScrollBar().setValue)

    def display(self, text):
        context = '\n'.join(text)
        self.textarea.setText(context)
