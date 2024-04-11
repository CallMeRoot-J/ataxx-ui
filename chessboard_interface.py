import numpy as np
from PyQt5.QtCore import pyqtSignal, Qt, QPoint, QSize
from PyQt5.QtGui import QPainter, QPen, QMouseEvent, QResizeEvent, QFont, QPixmap, QCloseEvent
from PyQt5.QtWidgets import QWidget, QMessageBox

from chessboard import chessboard


class chessboard_interface(QWidget):
    game_over_signal = pyqtSignal()
    obtain_next_move_signal = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_black_AI = False
        self.is_white_AI = False

        self.is_start = False
        self.board_len = 7

        self.last_click = None
        self.chessboard = chessboard(board_len=self.board_len)
        self.chess_list = []
        self.available_moves = []

        self.margin = 5
        self.grid_size = 78
        self.chess_size = 60
        self.setMinimumSize(650, 650)
        self.setMaximumSize(650, 650)
        self.setMouseTracking(True)
        self.connect_signal_to_slot()

    def connect_signal_to_slot(self):
        pass

    def mousePressEvent(self, e: QMouseEvent):
        cor = self.get_mat_position(e.pos())
        self.put_chess(cor)

    def get_mat_position(self, pos):
        n = self.board_len
        left, top = self.__getMargin()
        poses = np.array(
            [[[i * self.grid_size + left, (self.board_len - 1 - j) * self.grid_size + top] for j in range(n)]
             for i in range(n)])
        # Qt坐标系与矩阵的相反
        distances = (poses[:, :, 0] - pos.x()) ** 2 + (poses[:, :, 1] - pos.y()) ** 2
        col, row = np.where(distances == distances.min())
        return col[0], row[0]

    def paintEvent(self, e):
        # 绘制棋盘
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        # 绘制网格
        left, top = self.__getMargin()
        font = QFont()
        font.setPixelSize(25)
        font.setBold(True)
        font.setStyle(QFont.StyleNormal)
        painter.setFont(font)
        for i in range(self.board_len):
            x = y = self.margin + i * self.grid_size
            x = left + i * self.grid_size
            y = top + i * self.grid_size
            # 竖直线
            width = 2 if i in [0, self.board_len - 1] else 1
            painter.setPen(QPen(Qt.black, width))
            painter.drawText(x, self.width() - top + top // 2, chr(ord('A') + i))
            painter.drawLine(x, top, x, self.height() - top)
            # 水平线
            painter.drawText(left - left // 2, y, chr(ord('7') - i))
            painter.drawLine(left, y, self.width() - left - 1, y)
        # 绘制棋子
        for x in range(self.board_len - 1, -1, -1):
            for y in range(self.board_len - 1, -1, -1):
                pos = QPoint(x, self.board_len - 1 - y) * self.grid_size + QPoint(left - self.chess_size // 2,
                                                                                  top - self.chess_size // 2)
                if (x, y) in self.available_moves:
                    pen = QPen(Qt.darkGreen, 2)  # 设置画笔颜色为黑色，宽度为2px
                    painter.setPen(pen)
                    painter.drawRect(pos.x(), pos.y(), self.chess_size, self.chess_size)

                if self.chessboard.board[x][y] == chessboard.EMPTY:
                    continue
                if self.chessboard.board[x][y] == chessboard.BLACK:
                    pixmap = QPixmap("image/black.png")
                else:
                    pixmap = QPixmap("image/white.png")
                pixmap = pixmap.scaled(self.chess_size, self.chess_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                painter.drawPixmap(pos, pixmap)

                if (x, y) == self.last_click:
                    pen = QPen(Qt.red, 2)  # 设置画笔颜色为黑色，宽度为2px
                    painter.setPen(pen)
                    painter.drawRect(pos.x(), pos.y(), self.chess_size, self.chess_size)

        self.update()

    def withdraw(self, withdraw_player):
        if not self.is_start:
            self.show_warning("对局尚未开始!")
            return
        ok = 1
        if self.chessboard.current_player == -withdraw_player:
            ok = self.chessboard.withdraw()
            self.chess_list.pop()
            self.last_click = None
            self.available_moves.clear()
        else:
            for i in range(2):
                ok = self.chessboard.withdraw()
                self.chess_list.pop()
            self.last_click = None
            self.available_moves.clear()
        if not ok:
            self.show_warning("无法悔棋")

    def engine_state_flip(self, color):
        if color == chessboard.BLACK:
            self.is_black_AI = not self.is_black_AI
        else:
            self.is_white_AI = not self.is_white_AI

    def __getMargin(self):
        """ 获取棋盘边距 """
        left = (self.width() - (self.board_len - 1) * self.grid_size) // 2
        top = (self.height() - (self.board_len - 1) * self.grid_size) // 2
        return left, top

    def reset(self):
        self.chessboard.clear()
        self.chess_list.clear()
        self.is_start = True
        if self.is_black_AI:
            self.obtain_next_move_signal.emit(self.chessboard.current_player, self.chessboard.to_fen())

    def AI_put_chess(self, pos):
        if len(pos) == 2:
            x, y = ord(pos[0]) - ord('a'), ord(pos[1]) - ord('1')
            lastX, lastY = x, y
        else:
            lastX, lastY = ord(pos[0]) - ord('a'), ord(pos[1]) - ord('1')
            x, y = ord(pos[2]) - ord('a'), ord(pos[3]) - ord('1')
        chessType = self.chessboard.do_action(lastX, lastY, x, y)
        if not chessType:
            self.chess_list.append(self.tostring(x, y))
        else:
            self.chess_list.append((self.tostring(lastX, lastY, x, y)))

        res = self.chessboard.is_game_over()

        if res != 0:
            self.is_start = False
            self.game_over_signal.emit()
            if res == 1:
                self.show_meg("黑方获胜")
            elif res == -1:
                self.show_meg("白方获胜")
            else:
                self.show_meg("和棋")

        if self.is_start:
            if self.chessboard.current_player == chessboard.BLACK and self.is_black_AI:
                self.obtain_next_move_signal.emit(self.chessboard.current_player, self.chessboard.to_fen())
            elif self.chessboard.current_player == chessboard.WHITE and self.is_white_AI:
                self.obtain_next_move_signal.emit(self.chessboard.current_player, self.chessboard.to_fen())

    def put_chess(self, pos):
        if not self.is_start:
            self.show_warning("对局尚未开始！")
            return False
        x, y = pos
        if self.last_click is None:
            if not self.chessboard.is_available(x, y):
                return False
            self.available_moves = self.chessboard.get_available_actions(x, y)
            if len(self.available_moves) == 0:
                return False
            self.last_click = pos
        else:
            if (x, y) not in self.available_moves:
                if (x, y) == self.last_click:
                    self.last_click = None
                    self.available_moves.clear()
                    return
                if self.chessboard.is_available(x, y):
                    self.last_click = (x, y)
                    self.available_moves = self.chessboard.get_available_actions(x, y)
                return
            lastX, lastY = self.last_click

            chessType = self.chessboard.do_action(lastX, lastY, x, y)
            if not chessType:
                self.chess_list.append(self.tostring(x, y))
            else:
                self.chess_list.append((self.tostring(lastX, lastY, x, y)))
            self.last_click = None
            self.available_moves.clear()
            res = self.chessboard.is_game_over()

            if res != 0:
                self.is_start = False
                self.game_over_signal.emit()
                if res == 1:
                    self.show_meg("黑方获胜")
                elif res == -1:
                    self.show_meg("白方获胜")
                else:
                    self.show_meg("和棋")
            if self.is_start:
                if self.chessboard.current_player == chessboard.BLACK and self.is_black_AI:
                    self.obtain_next_move_signal.emit(self.chessboard.current_player, self.chessboard.to_fen())
                elif self.chessboard.current_player == chessboard.WHITE and self.is_white_AI:
                    self.obtain_next_move_signal.emit(self.chessboard.current_player, self.chessboard.to_fen())

    def tostring(self, x1, y1, x2=None, y2=None):
        x1 = chr(ord('a') + x1)
        y1 = chr(ord('1') + y1)
        if x2 is not None:
            x2 = chr(ord('a') + x2)
        if y2 is not None:
            y2 = chr(ord('1') + y2)
        if x2 is None:
            return x1 + y1
        else:
            return x1 + y1 + x2 + y2

    def show_warning(self, message):
        meg = QMessageBox()
        meg.setIcon(QMessageBox.Warning)
        meg.setText(message)
        meg.setWindowTitle("Error")
        meg.exec_()

    def show_meg(self, message):
        meg = QMessageBox()
        meg.setText(message)
        meg.setWindowTitle("对局结束")
        meg.exec_()

    def closeEvent(self, e: QCloseEvent):
        self.game_over_signal.emit()
        e.accept()
