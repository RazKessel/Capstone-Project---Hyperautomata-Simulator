from automata.SymbolVector import SymbolVector
from automata.Transition import Transition


class Automata:
    def __init__(self):
        self.states = set()  # Set of states
        self.alphabet = set()  # Input symbols
        self.transitions = {}  # State transitions
        self.start_state = None
        self.accept_states = set()

    def add_state(self, state, is_accept=False):
        self.states.add(state)
        if is_accept:
            self.accept_states.add(state)

    def set_start_state(self, state):
        self.start_state = state
        self.states.add(state)

    def add_transition(self, transition):
        if transition.fromState not in self.transitions:
            self.transitions[transition.fromState] = []
        self.transitions[transition.fromState].append(transition)


