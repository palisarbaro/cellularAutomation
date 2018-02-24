import cellularAutomaton
class gameOfLife(cellularAutomaton.cellularAutomaton):
    def state0(self, x, y):
        count = self.countAround(x, y, 1)
        if count == 3:
            return 1
        else:
            return 0
    def state1(self,x,y):
        count = self.countAround(x,y,1)
        if count==2 or count==3:
            return 1
        else:
            return 0

    def __init__(self, sizeX, sizeY,
                 errorState: "Состояние которое возвращается при неправильных координатах" = 0,
                 looping=True):
        super().__init__(sizeX,sizeY,2,errorState,looping)
        self.transitionFunctionList[0] = self.state0
        self.transitionFunctionList[1] = self.state1

