from components.state import State
from components.transition import Transition
from components.utils.logger import operation_logger


class AutomataManager:
    """
    Manages the states and transitions in a graphical user interface (GUI) for an automaton.
    """

    def __init__(self):
        # Initialize the automata manager with empty states and transitions.
        self.states = []  # List of State objects
        self.transitions = []  # List of Transition objects
        self.word_count = 1  # Number of symbols per transition vector
        operation_logger.info("AutomataManager initialized.")

    def add_state(self, name, x, y, is_start=False, is_accept=False):
        """
        Add a new state to the automaton.

        Args:
            name (str): The name of the state.
            x (int): The x-coordinate of the state in the GUI.
            y (int): The y-coordinate of the state in the GUI.
            is_start (bool): Whether the state is the start state.
            is_accept (bool): Whether the state is an accept state.

        Returns:
            State: The created state object.
        """
        st = State(name, x, y, is_start, is_accept)
        self.states.append(st)
        operation_logger.info(f"State added: {name}")
        return st

    def add_transition(self, src, tgt, vectors):
        """
        Add a new transition between two states.

        Args:
            src (State): The source state.
            tgt (State): The target state.
            vectors (list): A list of transition vectors.

        Returns:
            Transition: The created transition object.
        """
        tr = Transition(src, tgt, vectors)
        self.transitions.append(tr)
        operation_logger.info(f"Transition added: {src.name} -> {tgt.name}")
        return tr

    def set_word_count(self, new_count):
        """
        Set the number of symbols per transition vector and adjust existing transitions.

        Args:
            new_count (int): The new word count.
        """
        self.word_count = new_count
        for tr in self.transitions:
            new_vecs = []
            for vec in tr.transition_vectors:
                lst = list(vec)
                if len(lst) < new_count:
                    lst += ['#'] * (new_count - len(lst))
                elif len(lst) > new_count:
                    lst = lst[:new_count]
                new_vecs.append(tuple(lst))
            tr.transition_vectors = new_vecs
        operation_logger.info(f"Word count set to: {new_count}")

    def draw_all(self, canvas):
        """
        Draw all states and transitions on the canvas.

        Args:
            canvas: The GUI canvas object where the automaton will be drawn.
        """
        canvas.delete("all")
        for s in self.states:
            s.draw(canvas)
        for t in self.transitions:
            t.draw(canvas)
        operation_logger.info("All states and transitions drawn on canvas.")
