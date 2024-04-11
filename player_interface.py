from PyQt5.QtCore import Qt, QTime, pyqtSignal
from PyQt5.QtGui import QResizeEvent, QCloseEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from analysis import analysis
from player import player
from chessboard import chessboard


class player_interface(QWidget):
    game_over_signal = pyqtSignal()
    best_move_info_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.black = player(self, color=chessboard.BLACK)
        self.white = player(self, color=chessboard.WHITE)
        self.AI_analysis = analysis(self)
        self.init_widget()
        self.connect_signal_to_slot()

    def init_widget(self):
        self.setMinimumSize(900, 600)

        horizon_layout = QHBoxLayout(self)
        player_setting = QWidget(self)
        player_setting.setMaximumSize(220, 600)
        player_setting.setMinimumSize(220, 600)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.black)
        vertical_layout.addWidget(self.white)
        player_setting.setLayout(vertical_layout)
        horizon_layout.addWidget(player_setting)
        horizon_layout.addWidget(self.AI_analysis)
        self.setLayout(horizon_layout)

    def connect_signal_to_slot(self):
        pass

    def reset(self):
        self.black.reset()
        self.white.reset()

    def game_over(self):
        self.black.game_over()
        self.white.game_over()

    def obtain_next_move(self, color, fen):
        info = []
        print(fen)
        if color == chessboard.BLACK and self.black.is_AI:
            info = self.black.obtain_best_move(fen)
        elif color == chessboard.WHITE and self.white.is_AI:
            info = self.white.obtain_best_move(fen)
        if info is None:
            return
        if len(info) == 0:
            return
        print(info[-1])
        best_move = info[-1].split(' ')[-1]
        print(best_move)
        if best_move == '0000':
            return
        self.displaytext(info)
        self.best_move_info_signal.emit(best_move)

    def displaytext(self, text):
        self.AI_analysis.display(text)
