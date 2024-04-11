import os

from PyQt5.QtCore import QTime, pyqtSignal, Qt, QProcess, QByteArray, QElapsedTimer, QEventLoop
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog, QMessageBox, \
    QApplication, QScrollArea

from chessboard import chessboard
from engine import engine


class player(QWidget):
    withdraw_signal = pyqtSignal(int)
    engine_state_flip_signal = pyqtSignal(int)

    def __init__(self, parent=None, color=None):
        super().__init__(parent)

        self.load_button = None
        self.unload_button = None

        self.is_AI = False
        self.AI_thread = engine()
        self.AI_output = None
        self.AI_fileName = None

        self.color = color
        self.init_widget()
        self.connect_signal_to_slot()

    def connect_signal_to_slot(self):
        self.AI_thread.outputChanged.connect(self.engine_output)

    def init_widget(self):
        self.setMinimumSize(200, 200)
        self.setMaximumSize(200, 200)
        layout = QVBoxLayout(self)

        player_name_label = QLabel(self)

        font = QFont()
        font.setPixelSize(25)
        font.setBold(True)
        font.setStyle(QFont.StyleNormal)

        player_name_label.setFont(font)
        player_name_label.setAlignment(Qt.AlignCenter)
        if self.color == chessboard.BLACK:
            player_name_label.setText("Black(First)")
        else:
            player_name_label.setText("White(Second)")
        player_name_label.setMinimumSize(180, 30)
        player_name_label.setMaximumSize(180, 30)

        withdraw_button = QPushButton(self)
        withdraw_button.setText("Undo")
        withdraw_button.clicked.connect(self.withdraw)
        withdraw_button.resize(60, 50)
        withdraw_button.setMinimumSize(60, 30)

        engine_setting = QHBoxLayout(self)

        self.load_button = QPushButton()
        self.load_button.setText("Load")
        self.load_button.setMinimumSize(60, 30)
        self.load_button.clicked.connect(self.get_fileName)
        self.load_button.setEnabled(True)

        self.unload_button = QPushButton()
        self.unload_button.setText("Quit")
        self.unload_button.setMinimumSize(60, 30)
        self.unload_button.clicked.connect(self.unload_engine)
        self.unload_button.setEnabled(False)

        engine_setting.addWidget(self.load_button)
        engine_setting.addWidget(self.unload_button)

        layout.addWidget(player_name_label)
        layout.addLayout(engine_setting)
        layout.addWidget(withdraw_button)
        self.setLayout(layout)

    def engine_output(self, data):
        self.AI_output = data

    def withdraw(self):
        self.withdraw_signal.emit(self.color)

    def get_fileName(self):
        self.AI_fileName, _ = QFileDialog.getOpenFileName(None, 'Select Program', '.', 'Executable Files (*.exe)')
        if self.AI_fileName:
            self.is_AI = True
            self.load_button.setEnabled(False)
            self.unload_button.setEnabled(True)
            self.engine_state_flip_signal.emit(self.color)

    def load_engine(self):
        if self.AI_fileName is None:
            self.get_fileName()
        if self.AI_fileName:
            self.AI_thread.startEngine(self.AI_fileName)
            self.run_AI()

    def unload_engine(self):
        self.is_AI = False
        self.AI_thread.terminateEngine()
        self.AI_fileName = None
        self.AI_output = None

        self.load_button.setEnabled(True)
        self.unload_button.setEnabled(False)
        self.engine_state_flip_signal.emit(self.color)

    def isready(self):
        self.AI_thread.sendCommand("isready")
        return self.AI_output == "readyok"

    def obtain_best_move(self, fen):
        print("position fen " + fen)
        self.AI_thread.sendCommand("uainewgame")
        self.AI_thread.sendCommand("position fen " + fen)
        self.AI_thread.sendCommand("go")

        timer = QElapsedTimer()
        timer.start()

        loop = QEventLoop()
        while self.AI_thread.state != self.AI_thread.FREE or timer.elapsed() < 300:
            if self.AI_thread.state == self.AI_thread.END:
                return None
            loop.processEvents()
        return self.AI_output

    def run_AI(self):
        self.AI_thread.sendCommand("uai")
        loop = QEventLoop()
        while self.AI_thread.state != self.AI_thread.FREE:
            if self.AI_thread.state == self.AI_thread.END:
                break
            loop.processEvents()

    def game_over(self):
        if self.is_AI:
            self.AI_output = None
            self.AI_thread.terminateEngine()

    def reset(self):
        if self.is_AI:
            self.AI_output = None
            self.load_engine()

    def show_warning(self, message):
        meg = QMessageBox()
        meg.setIcon(QMessageBox.Warning)
        meg.setText(message)
        meg.setWindowTitle("Error")
        meg.exec_()
