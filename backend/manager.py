from backend.simulation import Simulation
import copy

from backend.tape import Tape
from backend.transition import Transition

class Manager:
    def __init__(self, automata, tapes):
        # Initialize the manager with the given automaton and tapes.
        self.automata = automata           # Instance of Automata
        self.tapes = tapes                 # List of Tape objects
        self.accepting_states = automata.accept_states  # Accept states of the automaton
        self.sim = Simulation(self.tapes)  # Current simulation state
        self.visited = {self.sim}          # Set of visited simulations
        self.queue = [self.sim]            # Queue of active simulations

    def mainLoop(self):
        """
        Perform a BFS search to find a path to an accepting state.

        Returns:
            List: The history of the simulation.
        """
        flag = True
        while any(tape.symbol != '#' for tape in self.tapes) and len(self.queue) >= 0:
            if flag:
                sim = self.queue.pop(0)
                self.tapes = sim.tapes
                flag = False

            for transition in self.automata.transitions.get(sim.currentState, []):
                history = sim.history.copy()
                tapesCopy = copy.deepcopy(self.tapes)
                if transition.symbolsVector.matches(tapesCopy):
                    current_state = transition.targetState
                    historySnapShot = [current_state] + [tape.currentPos for tape in tapesCopy]
                    history.append(historySnapShot)
                    newSim = Simulation(tapesCopy, history, current_state)
                    if newSim not in self.visited:
                        self.visited.add(newSim)
                        self.queue.append(newSim)

            sim = self.queue.pop(0)
            self.tapes = sim.tapes
            if (sim.currentState in self.accepting_states) and all(tape.symbol == '#' for tape in self.tapes):
                return sim.history
        return sim.history

    def addTape(self, tape, history):
        """
        Add a new tape to the simulation, ensuring its validity.

        Args:
            tape (str): The tape to add.
            history (list): The simulation history to continue from.
        """
        for char in tape:
            if char not in self.automata.alphabet:
                print("The tape is not valid: at least one of its characters is not in the alphabet")
                return
        self.setTapes(history[-1])
        self.tapes.append(Tape(tape))

    def update(self, history):
        """
        Update the simulation state and find a path to an accepting state.

        Args:
            history (list): The simulation history to update.

        Returns:
            List: The updated simulation history.
        """
        sim = Simulation(self.tapes, history, history[-1][0])
        self.visited = {sim}
        self.queue = [sim]
        self.sim = sim
        return self.mainLoop()

    def setTapes(self, snapShot):
        """
        Set the tapes' positions and symbols based on a snapshot.

        Args:
            snapShot (list): The snapshot containing tape positions.
        """
        snapShot = snapShot[1:]
        for i in range(len(snapShot)):
            self.tapes[i].currentPos = snapShot[i]
            if snapShot[i] >= len(self.tapes[i].symbols):
                self.tapes[i].symbol = '#'
            else:
                self.tapes[i].symbol = self.tapes[i].symbols[snapShot[i]]
