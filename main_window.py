from PyQt5.QtWidgets import QMainWindow, QGridLayout, QHBoxLayout, QApplication, QAction, QSizePolicy
from PyQt5.QtGui import QIcon, QResizeEvent, QCloseEvent
from PyQt5.QtCore import pyqtSignal, QObject
from chessboard_interface import chessboard_interface
from engine_interface import engine_interface
from player_interface import player_interface


class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.chessboard_interface = chessboard_interface(self)
        self.player_interface = player_interface(self)
        self.engine_interface = engine_interface()
        self.init_main_window()
        self.connect_signal_to_slot()

    def connect_signal_to_slot(self):
        self.chessboard_interface.game_over_signal.connect(self.player_interface.game_over)

        self.player_interface.black.withdraw_signal.connect(self.chessboard_interface.withdraw)
        self.player_interface.white.withdraw_signal.connect(self.chessboard_interface.withdraw)

        self.player_interface.black.engine_state_flip_signal.connect(self.chessboard_interface.engine_state_flip)
        self.player_interface.white.engine_state_flip_signal.connect(self.chessboard_interface.engine_state_flip)

        self.chessboard_interface.obtain_next_move_signal.connect(self.player_interface.obtain_next_move)
        self.player_interface.best_move_info_signal.connect(self.chessboard_interface.AI_put_chess)

    def init_main_window(self):
        self.resize(1500, 650)
        self.setWindowTitle("Ataxx")
        self.setWindowIcon(QIcon("image/icon.png"))

        layout = QHBoxLayout()
        layout.addWidget(self.chessboard_interface)
        layout.addWidget(self.player_interface)
        self.setLayout(layout)

        self.init_menu()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def init_menu(self):
        menu = self.menuBar()
        menu.setNativeMenuBar(False)

        game_menu = menu.addMenu("Game")

        new_game_act = QAction("New Game", self)
        new_game_act.triggered.connect(self.new_game)
        game_menu.addAction(new_game_act)

        exit_game_act = QAction("Quit", self)
        exit_game_act.triggered.connect(self.close_clicked)
        game_menu.addAction(exit_game_act)

        engine_menu = menu.addMenu("Engine")

        load_engine_act = QAction("Load AI Engine", self)
        load_engine_act.triggered.connect(self.engine_interface.load_engine)
        engine_menu.addAction(load_engine_act)

        unload_engine_act = QAction("Quit AI Engine", self)
        unload_engine_act.triggered.connect(self.engine_interface.unload_engine)
        engine_menu.addAction(unload_engine_act)

    def resizeEvent(self, a: QResizeEvent):
        super().resizeEvent(a)
        self.player_interface.move(self.width() - 920, 20)

    def new_game(self):
        self.player_interface.reset()
        self.chessboard_interface.reset()

    def closeEvent(self, e: QCloseEvent):
        self.chessboard_interface.closeEvent(e)
        e.accept()

    def close_clicked(self):
        close_event = QCloseEvent()
        self.closeEvent(close_event)
        if not close_event.isAccepted():
            return
        self.close()
