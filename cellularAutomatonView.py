from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QApplication
from cellularAutomaton import cellularAutomaton


class cellularAutomatonView(QWidget):
    def __init__(self, automaton, parent=None, colors=None):
        """
        @type automaton: cellularAutomaton
        графическое представление для клеточного автомата cellAuto
        """
        super().__init__(parent=parent)
        self.automaton = automaton
        self.colors = colors if colors != None else [Qt.black, Qt.green]
        if len(self.colors) < automaton.states:
            raise BaseException("Не достаточно цветов")
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)

    def start(self, interval):
        "запускает таймер с интервалом interval"
        self.timer.start(interval)

    def stop(self):
        "отсанавливает таймер"
        self.timer.stop()

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
