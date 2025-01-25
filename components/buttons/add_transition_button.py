from components.buttons.selection_button import SelectionTool

from components.utils.logger import operation_logger
from components.utils.constants import COLOR_BLACK, COLOR_RED

class AddTransitionTool:
    """
        Tool to add a new transition by selecting two states on the canvas.
        If a transition in the same direction exists, it opens an edit window instead.
    """

    def __init__(self, canvas, automata_manager, undo_stack, redo_stack):
        self.canvas = canvas
        self.automata_manager = automata_manager
        self.undo_stack = undo_stack
        self.redo_stack = redo_stack
        self.selected_states = []

    def activate(self):
        """ Activate the tool by binding the click event. """
        self.canvas.bind("<Button-1>", self._on_click)
        operation_logger.info("AddTransitionTool activated.")

    def deactivate(self):
        """ Deactivate the tool by unbinding the click event and clearing selections. """
        self.canvas.unbind("<Button-1>")
        self.selected_states.clear()
        operation_logger.info("AddTransitionTool deactivated.")

    def _on_click(self, event):
        """
            On left-click:
             1) If a state is found at (x,y), highlight it and store it.
             2) Once two states are selected, either open 'Edit Transition' if it exists, 
                or 'Add Transition' if it doesn't.
        """
        selected_state = self._find_state(event.x, event.y)
        if selected_state:
            self._highlight_state(selected_state, on=True)
            self.selected_states.append(selected_state)
            if len(self.selected_states) == 2:
                s1, s2 = self.selected_states
                existing = self._find_transition_same_dir(s1, s2)

                selection_tool = SelectionTool(
                    canvas=self.canvas,
                    automata_manager=self.automata_manager,
                    undo_stack=self.undo_stack,
                    redo_stack=self.redo_stack
                )

                if existing:
                    # edit
                    selection_tool.open_transition_window(
                        existing_transition=existing
                    )
                    operation_logger.info(f"Existing transition selected: {s1.name} -> {s2.name}")
                else:
                    # add
                    selection_tool.open_transition_window(
                        src=s1, tgt=s2,
                        existing_transition=None
                    )
                    operation_logger.info(f"New transition to create: {s1.name} -> {s2.name}")

                # Unhighlight
                for st in self.selected_states:
                    self._highlight_state(st, on=False)
                self.selected_states.clear()
        else:
            # Clicked on empty space; reset selections
            for st in self.selected_states:
                self._highlight_state(st, on=False)
            self.selected_states.clear()
            operation_logger.warning("Clicked on empty space while adding transition.")

    def _find_state(self, x, y):
        """ Find and return the state at the given coordinates. """
        for s in self.automata_manager.states:
            dx, dy = x - s.x, y - s.y
            if (dx**2 + dy**2)**0.5 <= s.radius:
                return s
        return None

    def _highlight_state(self, state_obj, on=True):
        """ Highlight or unhighlight a state on the canvas. """
        color = COLOR_RED if on else COLOR_BLACK
        if state_obj.canvas_id:
            self.canvas.itemconfig(state_obj.canvas_id, outline=color, width=(3 if on else 2))

    def _find_transition_same_dir(self, s1, s2):
        """ Check if a transition from state1 to state2 already exists. """
        for t in self.automata_manager.transitions:
            if t.source == s1 and t.target == s2:
                return t
        return None
