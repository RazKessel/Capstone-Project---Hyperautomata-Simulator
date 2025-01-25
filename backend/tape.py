class Tape:
    """
    Represents a tape used in automata operations, containing symbols and a current position.
    """

    def __init__(self, symbols):
        # Initialize the tape with a sequence of symbols.
        self.symbols = symbols            # List of symbols on the tape
        self.currentPos = 0               # Current position on the tape
        self.symbol = symbols[0]          # Current symbol at the tape's position

    def read(self):
        """
        Advance the current position on the tape and update the current symbol.

        If the end of the tape is reached, the symbol is set to '#'.
        """
        if self.currentPos < len(self.symbols):
            self.currentPos += 1
            if self.currentPos < len(self.symbols):
                self.symbol = self.symbols[self.currentPos]
            else:
                self.symbol = '#'
        else:
            self.symbol = '#'
