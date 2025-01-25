import pytest
from unittest.mock import MagicMock
from components.login_window import LoginWindow
from components.run_app import MainApplication
from components.state import State
from components.transition import Transition
from components.db_integration import DBManager
from components.drawing_board import DrawingBoard
from components.buttons.add_state_button import AddStateTool
from components.buttons.add_transition_button import AddTransitionTool
from components.buttons.selection_button import SelectionTool
from components.managers.automata_manager import AutomataManager
from components.managers.run_manager import RunManager

# Test for LoginWindow
def test_login_window_initialization():
    """Test initialization of LoginWindow."""
    import tkinter as tk
    root = tk.Tk()
    mock_db_manager = MagicMock()
    mock_callback = MagicMock()
    login_window = LoginWindow(root, mock_db_manager, mock_callback)
    assert login_window.db_manager == mock_db_manager
    assert login_window.success_callback == mock_callback
    root.destroy()

# Test for MainApplication
def test_main_application_initialization():
    """Test initialization of MainApplication."""
    mock_user = "test_user"
    mock_db_manager = MagicMock()
    app = MainApplication(mock_user, mock_db_manager)
    assert app.current_user == mock_user
    assert app.db_manager == mock_db_manager

# Test for State class
def test_state_initialization():
    """Test initialization of State class."""
    state = State(name="q0", x=100, y=100, is_start=True, is_accept=False)
    assert state.name == "q0"
    assert state.x == 100
    assert state.y == 100
    assert state.is_start is True
    assert state.is_accept is False

def test_state_draw():
    """Test draw method of State class."""
    mock_canvas = MagicMock()
    state = State(name="q0", x=100, y=100)
    state.draw(mock_canvas)
    mock_canvas.create_oval.assert_called()

# Test for Transition class
def test_transition_initialization():
    """Test initialization of Transition class."""
    source = State("q0", 100, 100)
    target = State("q1", 200, 200)
    transition = Transition(source, target, [["a"]])
    assert transition.source == source
    assert transition.target == target
    assert transition.transition_vectors == [["a"]]

# Test for DBManager
def test_db_manager_initialization():
    """Test initialization of DBManager."""
    db_manager = DBManager("sqlite:///:memory:")
    assert db_manager.engine is not None

def test_add_user():
    """Test add_user method of DBManager."""
    db_manager = DBManager("sqlite:///:memory:")
    result, message = db_manager.add_user("test_user", "password")
    assert result is True
    assert message == "User created."

# Test for DrawingBoard
def test_drawing_board_initialization():
    """Test initialization of DrawingBoard."""
    mock_parent = MagicMock()
    board = DrawingBoard(mock_parent, bg="white", width=500, height=500)
    assert board.current_highlight is None

def test_drawing_board_highlight_state():
    """Test highlight_state method of DrawingBoard."""
    mock_parent = MagicMock()
    board = DrawingBoard(mock_parent, bg="white", width=500, height=500)
    mock_canvas_item = MagicMock()
    board.current_highlight = mock_canvas_item
    board.highlight_state("q0")
    # Ensure the highlight logic was executed
    assert board.current_highlight is None  # Simulated removal

# Test for AddStateTool
def test_add_state_tool_initialization():
    """Test initialization of AddStateTool."""
    mock_canvas = MagicMock()
    mock_automata_manager = MagicMock()
    mock_undo_stack = MagicMock()
    mock_redo_stack = MagicMock()
    tool = AddStateTool(mock_canvas, mock_automata_manager, mock_undo_stack, mock_redo_stack)
    assert tool.canvas == mock_canvas
    assert tool.automata_manager == mock_automata_manager
    assert tool.undo_stack == mock_undo_stack
    assert tool.redo_stack == mock_redo_stack

# Test for AddTransitionTool
def test_add_transition_tool_initialization():
    """Test initialization of AddTransitionTool."""
    mock_canvas = MagicMock()
    mock_automata_manager = MagicMock()
    mock_undo_stack = MagicMock()
    mock_redo_stack = MagicMock()
    tool = AddTransitionTool(mock_canvas, mock_automata_manager, mock_undo_stack, mock_redo_stack)
    assert tool.canvas == mock_canvas
    assert tool.automata_manager == mock_automata_manager
    assert tool.undo_stack == mock_undo_stack
    assert tool.redo_stack == mock_redo_stack

# Test for SelectionTool
def test_selection_tool_initialization():
    """Test initialization of SelectionTool."""
    mock_canvas = MagicMock()
    mock_automata_manager = MagicMock()
    mock_undo_stack = MagicMock()
    mock_redo_stack = MagicMock()
    tool = SelectionTool(mock_canvas, mock_automata_manager, mock_undo_stack, mock_redo_stack)
    assert tool.canvas == mock_canvas
    assert tool.automata_mgr == mock_automata_manager
    assert tool.undo_stack == mock_undo_stack
    assert tool.redo_stack == mock_redo_stack

# Test for AutomataManager
def test_automata_manager_initialization():
    """Test initialization of AutomataManager."""
    manager = AutomataManager()
    assert manager.states == []
    assert manager.transitions == []
    assert manager.word_count == 1

def test_automata_manager_add_state():
    """Test adding a state in AutomataManager."""
    manager = AutomataManager()
    state = manager.add_state("q0", x=100, y=100, is_start=True, is_accept=False)
    assert state.name == "q0"
    assert state in manager.states

def test_automata_manager_add_transition():
    """Test adding a transition in AutomataManager."""
    manager = AutomataManager()
    source = manager.add_state("q0", x=100, y=100)
    target = manager.add_state("q1", x=200, y=200)
    transition = manager.add_transition(source, target, [["a"]])
    assert transition.source == source
    assert transition.target == target
    assert transition in manager.transitions

# Test for RunManager
def test_run_manager_initialization():
    """Test initialization of RunManager."""
    mock_automata_manager = MagicMock()
    mock_db_manager = MagicMock()
    run_manager = RunManager(mock_automata_manager, mock_db_manager, "test_user")
    assert run_manager.automata_manager == mock_automata_manager
    assert run_manager.db_manager == mock_db_manager
    assert run_manager.current_user == "test_user"

def test_run_manager_add_word():
    """Test adding a word in RunManager."""
    mock_automata_manager = MagicMock()
    mock_db_manager = MagicMock()
    run_manager = RunManager(mock_automata_manager, mock_db_manager, "test_user")
    run_manager.add_word("test")
    assert "test" in run_manager.words

def test_run_manager_initialize_backend():
    """Test initializing the backend in RunManager."""
    mock_automata_manager = MagicMock()
    mock_db_manager = MagicMock()
    mock_automata_manager.states = []
    mock_automata_manager.transitions = []
    run_manager = RunManager(mock_automata_manager, mock_db_manager, "test_user")
    run_manager.initialize_backend()
    assert run_manager.manager is not None
