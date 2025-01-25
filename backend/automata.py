class Automata:
    def __init__(self):
        # Initialize the automaton with empty sets of states and alphabet,
        # an empty dictionary for transitions, and placeholders for start and accept states.
        self.states = set()  # Set of states
        self.alphabet = set()  # Input symbols
        self.transitions = {}  # State transitions, mapping a state to a list of transitions
        self.start_state = None  # Initial state of the automaton
        self.accept_states = set()  # Set of accept states

    def add_state(self, state, is_accept=False):
        """
        Add a new state to the automaton.
        If the state is an accept state, add it to the accept_states set as well.

        Args:
            state: The name or identifier of the state.
            is_accept (bool): Whether the state is an accept state.
        """
        self.states.add(state)
        if is_accept:
            self.accept_states.add(state)

    def set_start_state(self, state):
        """
        Set the start state of the automaton.

        Args:
            state: The name or identifier of the state to set as the start state.
        """
        self.start_state = state
        self.states.add(state)

    def add_transition(self, transition):
        """
        Add a transition to the automaton.

        Args:
            transition (Transition): The transition to add, including the source state, target state, and symbol.
        """
        if transition.fromState not in self.transitions:
            self.transitions[transition.fromState] = []
        self.transitions[transition.fromState].append(transition)

    def rename_state(self, old_name, new_name):
        """
        Rename a state in the automaton and update all related transitions.

        Args:
            old_name: The current name of the state.
            new_name: The new name for the state.
        """
        if old_name == new_name:
            return
        if old_name in self.states:
            self.states.remove(old_name)
            self.states.add(new_name)
        if old_name in self.accept_states:
            self.accept_states.remove(old_name)
            self.accept_states.add(new_name)
        if old_name == self.start_state:
            self.start_state = new_name
        if old_name in self.transitions:
            self.transitions[new_name] = self.transitions.pop(old_name)
            for tr in self.transitions[new_name]:
                tr.fromState = new_name
        for tr_list in self.transitions.values():
            for tr in tr_list:
                if tr.targetState == old_name:
                    tr.targetState = new_name
