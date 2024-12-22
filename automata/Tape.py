#from PathTracker import PathTracker


class Tape:
    def __init__(self, symbols):
        self.symbols = symbols
        self.currentPos = 0
        self.symbol = symbols[0]
        #self.pathTracker = PathTracker()

    def read(self):

        if self.currentPos < len(self.symbols):
            self.currentPos += 1
            if self.currentPos <len(self.symbols):
                self.symbol = self.symbols[self.currentPos]
            else:
                self.symbol = '#'

        else:
            self.symbol = '#'