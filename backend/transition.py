from backend.symbolVector import SymbolVector

class Transition:
    """
    Represents a transition in an automaton, defining the transition conditions
    and the target state based on a given state and input vector.
    """

    def __init__(self, fromState, symbols_vector, targetState):
        # Initialize the transition with a source state, a symbols vector, and a target state.
        self.symbolsVector = symbols_vector  # Instance of SymbolVector defining the transition condition
        self.targetState = targetState       # The state to transition to
        self.fromState = fromState           # The state to transition from

    def __repr__(self):
        """
        Return a string representation of the transition.
        """
        return f"Transition({self.fromState} -> {self.targetState}, vec={self.symbolsVector})"
