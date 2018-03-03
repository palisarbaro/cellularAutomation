from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QApplication
from cellularAutomaton import cellularAutomaton


class cellularAutomatonView(QWidget):
    intervalChanged = pyqtSignal()
    def __init__(self, automaton, parent=None, colors=None):
        """
        @type automaton: cellularAutomaton
        графическое представление для клеточного автомата cellAuto
        """
        super().__init__(parent=parent)
        self.__interval = 300;
        self.drawingState = 1
        self.automaton = automaton
        self.colors = colors if colors != None else [Qt.black, Qt.green]
        if len(self.colors) < automaton.states:
            raise BaseException("Не достаточно цветов")
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self,val):
        self.__interval = val
        if self.timer.isActive():
            self.stop()
            self.start()
        self.intervalChanged.emit()

    def start(self):
        self.timer.start(self.interval)

    def stop(self):
        self.timer.stop()

    def startStop(self):
        if self.timer.isActive():
            self.stop()
        else:
            self.start()

    def tick(self):
        "тик таймера"
        self.automaton.tick()
        self.update()

    def initUI(self):
        self.setGeometry(0, 0, 500, 500)
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        dx = self.width() / self.automaton.sizeX
        dy = self.height() / self.automaton.sizeY
        for i in range(self.automaton.sizeX):
            for j in range(self.automaton.sizeY):
                color = self.colors[self.automaton.get(i, j)]
                qp.setBrush(QBrush(color))
                # qp.setPen(QPen(color))
                qp.drawRect(dx * i, dy * j, dx, dy)
        qp.end()

    def mouseMoveEvent(self, event):
        x = int(event.x()/self.width()*self.automaton.sizeX)
        y = int(event.y()/self.height()*self.automaton.sizeY)
        if x>=0 and y>=0 and x<self.automaton.sizeX and y< self.automaton.sizeY:
            self.automaton.matrix[x][y] = self.drawingState
            self.update()

    def mousePressEvent(self, event):
        self.mouseMoveEvent(event)