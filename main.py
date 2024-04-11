import sys

from PyQt5.QtWidgets import QApplication
from main_window import main_window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = main_window()
    main_window.show()
    app.exec_()
