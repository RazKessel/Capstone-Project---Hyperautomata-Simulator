import tkinter as tk
from tkinter import ttk

from components.utils.logger import operation_logger
from components.utils.constants import MAIN_WINDOW_HEIGHT, MAIN_WINDOW_WIDTH

from components.managers.run_manager import RunManager
from components.managers.automata_manager import AutomataManager

from components.panels.draw_tools import ToolsFrame
from components.panels.run_tools import RunToolsFrame
from components.panels.words import WordsFrame
from components.panels.current_setup import CurrentSetupFrame

from components.buttons.help_button import HelpButton

from components.drawing_board import DrawingBoard

class MainApplication(tk.Tk):
    def __init__(self, current_user, db_manager):
        super().__init__()
        self.title("Hyper Automata")
        self.geometry(f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}")
        operation_logger.info("Application started.")
        
        self.current_user = current_user
        self.db_manager = db_manager

        self._build_main_gui()

    def _build_main_gui(self):
        """ Construct the main automata GUI """
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        top_frame = tk.Frame(self)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        help_btn = HelpButton(
            parent=top_frame,
            text="HELP"
        )
        help_btn.pack(side=tk.LEFT, padx=10, pady=5)

        # Managers
        self.automata_mgr = AutomataManager()
        self.run_mgr = RunManager(
            automata_manager=self.automata_mgr,
            db_manager=self.db_manager,
            current_user=self.current_user
        )
        self.undo_stack = []
        self.redo_stack = []

        # Canvas
        self.canvas = DrawingBoard(self, bg="white", width=900, height=700)
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.run_mgr.set_canvas(self.canvas)

        # Tools panel
        self.tools_panel = ToolsFrame(
            parent=self,
            automata_mgr=self.automata_mgr,
            canvas=self.canvas,
            undo_stack=self.undo_stack,
            redo_stack=self.redo_stack
        )
        self.tools_panel.grid(row=1, column=1, sticky="ns", padx=5, pady=5)

        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(1, weight=1)
        self.bottom_frame.columnconfigure(2, weight=1)

        # Run tools
        self.run_tools = RunToolsFrame(
            parent=self.bottom_frame,
            run_mgr=self.run_mgr,
            canvas=self.canvas
        )
        self.run_tools.grid(row=0, column=0, sticky="nsew")

        # Words window
        self.words_window = WordsFrame(
            parent=self.bottom_frame,
            run_mgr=self.run_mgr,
            tool_window=self.tools_panel,
            automata_manager=self.automata_mgr,
            run_tools=self.run_tools
        )
        self.words_window.grid(row=0, column=1, sticky="nsew")

        # Current Setup display
        self.current_setup = CurrentSetupFrame(
            parent=self.bottom_frame,
            run_mgr=self.run_mgr,
            canvas=self.canvas
        )
        self.current_setup.grid(row=0, column=2, sticky="nsew")

        # Cross references
        self.run_tools.set_current_setup(self.current_setup)
        self.run_tools.set_words_window_ref(self.words_window)
        self.run_tools.set_tools_panel_ref(self.tools_panel)

        if "Selection" in self.tools_panel.tools:
            _, selection_tool = self.tools_panel.tools["Selection"]
            selection_tool.run_mgr = self.run_mgr

        operation_logger.info("Main BFS GUI built successfully.")
