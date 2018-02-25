import copy


class cellularAutomaton():
    def __init__(self, sizeX, sizeY,
                 states: "количество возможны состояний клетки" = 2,
                 errorState: "Состояние которое возвращается при неправильных координатах" = 0,
                 looping=True):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.states = states
        self.errorState = errorState
        self.looping = looping
        self.matrix = [[0] * sizeY for i in range(sizeX)]
        self.buffer = copy.deepcopy(self.matrix)

        p = lambda i: lambda self, x, y: i
        self.transitionFunctionList = [p(i) for i in range(states)]
        """список функций перехода
        transitionFunctionList[i](self,x,y) - функция, которая возвращает состояние,
        в которое должна перейти клетка(x,y) из состояния i
        по умолчанию состояния не изменяются
        """

    def loopCoordinates(self, x_y):
        "зацикливает координаты"
        x = x_y[0]
        y = x_y[1]
        x = x % self.sizeX
        y = y % self.sizeY
        return (x, y)

    def get(self, x, y=None):
        """
        Если аргумент один, то считается, что вызвано get((x,y))
        Возвращает состояние клетки (x,y),
        если x или y выходят за пределы поля, то в зависимости от looping
        либо возвращает errorState либо зацикливает координаты"""
        if y == None:
            y = x[1]
            x = x[0]

        if self.looping:
            x, y = self.loopCoordinates((x, y))
            return self.matrix[x][y]
        else:
            if (x, y) != self.loopCoordinates((x, y)):
                return self.errorState
            else:
                return self.matrix[x][y]

    def countAround(self, x, y, state):
        "считает сколько вокруг (x,y) клеток с состоянием state"
        coords = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1),
                  (x + 1, y + 1)]
        counter = 0
        for x_y in coords:
            if self.get(x_y) == state:
                counter += 1
        return counter

    def tick(self):
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                self.buffer[x][y] = self.transitionFunctionList[self.get(x, y)](self,x, y)
        self.matrix = copy.deepcopy(self.buffer)
