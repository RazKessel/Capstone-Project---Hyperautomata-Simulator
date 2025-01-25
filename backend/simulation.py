class Simulation:
    '''
    Represents a snapshot of a state in the automaton.
    '''
    def __init__(self, tapes, history=None, currentState=0):
        # Initialize the simulation with tapes, history, and current state.
        self.currentState = currentState          # The current state of the automaton.
        self.tapes = tapes                        # List of tapes associated with the simulation.
        self.history = history if history is not None else [[0] * (len(tapes) + 1)]
        self.id = self.__hash__()                # Unique identifier for the simulation.

    def __hash__(self):
        '''
        Compute a unique hash for the simulation based on the latest history snapshot.
        '''
        return hash(tuple(self.history[-1]))

    def __eq__(self, other):
        '''
        Check equality between two simulation objects based on their unique IDs.
        '''
        return self.id == other.id
