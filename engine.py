from PyQt5.QtCore import QProcess, pyqtSignal


class engine(QProcess):
    outputChanged = pyqtSignal(list)
    BUSY = 0
    FREE = 1
    END = 2

    def __init__(self):
        super().__init__()
        self.setProcessChannelMode(QProcess.MergedChannels)
        self.readyReadStandardOutput.connect(self.readOutput)
        self.total_data = []
        self.state = self.END

    def readOutput(self):
        data = self.readAllStandardOutput().data().decode('utf-8').split('\r\n')
        data.pop()
        if len(data) == 0:
            return
        items = data[-1].split(maxsplit=1)
        if not items:
            return
        self.total_data += data
        instruct = items[0]
        if instruct in ['uaiok', 'bestmove']:
            self.outputChanged.emit(self.total_data)
            self.total_data.clear()
            self.state = self.FREE

    def startEngine(self, enginePath):
        self.start(enginePath)
        self.state = self.FREE

    def sendCommand(self, command):
        self.state = self.BUSY
        self.write(bytes(command + '\n', 'utf-8'))

    def terminateEngine(self):
        self.kill()
        self.state = self.END
