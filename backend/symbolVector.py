class SymbolVector:
    """
    Represents a vector of symbols used in automata operations.
    """

    def __init__(self, vector):
        # Initialize the SymbolVector with a given vector.
        self.vector = vector

    def __iter__(self):
        """
        Return an iterator for the vector.
        """
        return iter(self.vector)

    def matches(self, tapes):
        """
        Check if the SymbolVector matches the symbols on the given tapes.

        Args:
            tapes (list): List of Tape objects.

        Returns:
            bool: True if the vector matches the tapes' symbols, otherwise False.
        """
        tapesLog = tapes.copy()  # Backup the original tapes
        tapesSymbols = [tape.symbol for tape in tapes]  # Extract symbols from tapes
        i = 0

        for sv, tp in zip(self.vector, tapesSymbols):
            if sv == '#':  # Ignore '#' symbol in the vector
                i += 1
                continue
            elif sv == tp:  # If the symbols match, read the tape
                tapes[i].read()
                i += 1
            else:  # If there is a mismatch, restore tapes and return False
                tapes = tapesLog
                return False

        return True
