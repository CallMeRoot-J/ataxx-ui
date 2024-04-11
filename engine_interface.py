from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QWidget, QFileDialog


class engine_interface(QWidget):
    def __init__(self):
        # todo
        super().__init__()
        self.init_widget()

    def init_widget(self):
        # todo
        pass

    def load_engine(self):
        fileName, _ = QFileDialog.getOpenFileName(None, 'Select Program', '.', 'Executable Files (*.exe)')

        # 如果有选中程序，则启动程序
        if fileName:
            # 创建QProcess对象，并设置程序路径
            process = QProcess()
            process.setProgram(fileName)

            # 启动程序
            process.start()

    def unload_engine(self):
        # todo
        pass
