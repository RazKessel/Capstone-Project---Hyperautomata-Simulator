import pytest
from backend.tape import Tape
from backend.symbolVector import SymbolVector
from backend.transition import Transition
from backend.automata import Automata
from backend.simulation import Simulation

# Test for the Tape class
def test_tape_initialization():
    """Test initialization of Tape class."""
    tape = Tape(symbols="abc")
    assert tape.symbols == "abc"
    assert tape.currentPos == 0
    assert tape.symbol == "a"

def test_tape_read():
    """Test the read method of Tape class."""
    tape = Tape(symbols="abc")
    tape.read()
    assert tape.currentPos == 1
    assert tape.symbol == "b"
    tape.read()
    assert tape.currentPos == 2
    assert tape.symbol == "c"
    tape.read()
    assert tape.symbol == "#"  # End of tape

# Test for the SymbolVector class
def test_symbol_vector_initialization():
    """Test initialization of SymbolVector class."""
    vector = SymbolVector(["a", "b", "c"])
    assert vector.vector == ["a", "b", "c"]

def test_symbol_vector_matches():
    """Test matches method of SymbolVector class."""
    tape1 = Tape("abc")
    tape2 = Tape("bbc")
    tape1.read()  # Move tape1 to symbol 'b'
    tape2.read()  # Move tape2 to symbol 'b'
    tapes = [tape1, tape2]
    vector = SymbolVector(["b", "b"])
    assert vector.matches(tapes) == True  # Now matches

    vector = SymbolVector(["b", "c"])
    assert vector.matches(tapes) == False  # Doesn't match


# Test for the Transition class
def test_transition_initialization():
    """Test initialization of Transition class."""
    vector = SymbolVector(["a", "b"])
    transition = Transition(fromState=0, symbols_vector=vector, targetState=1)
    assert transition.fromState == 0
    assert transition.symbolsVector == vector
    assert transition.targetState == 1

# Test for the Automata class
def test_automata_initialization():
    """Test initialization of Automata class."""
    automata = Automata()
    assert automata.states == set()
    assert automata.alphabet == set()
    assert automata.transitions == {}
    assert automata.start_state is None
    assert automata.accept_states == set()

def test_automata_add_state():
    """Test add_state method of Automata class."""
    automata = Automata()
    automata.add_state(0, is_accept=True)
    assert 0 in automata.states
    assert 0 in automata.accept_states

# Test for the Simulation class
def test_simulation_initialization():
    """Test initialization of Simulation class."""
    tape1 = Tape("abc")
    tape2 = Tape("def")
    tapes = [tape1, tape2]
    simulation = Simulation(tapes)
    assert simulation.currentState == 0
    assert simulation.history == [[0, 0, 0]]
    assert simulation.tapes == tapes
