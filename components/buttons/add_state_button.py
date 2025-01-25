from components.utils.logger import operation_logger

from components.buttons.selection_button import SelectionTool

class AddStateTool:
    """
        Tool to add a new state by clicking on the canvas.
        Opens a Toplevel window to name the state, set start/accept flags.
    """

    def __init__(self, canvas, automata_manager, undo_stack, redo_stack):
        self.canvas = canvas
        self.automata_manager = automata_manager
        self.undo_stack = undo_stack
        self.redo_stack = redo_stack

    def activate(self):
        """ Activate the tool by binding the click event. """
        self.canvas.bind("<Button-1>", self._on_click)
        operation_logger.info("AddStateTool activated.")

    def deactivate(self):
        """ Deactivate the tool by unbinding the click event. """
        self.canvas.unbind("<Button-1>")
        operation_logger.info("AddStateTool deactivated.")

    def _on_click(self, event):
        """
            Handle canvas click to add a new state. Use coordinates of click to
            open window near cursors    
            - If there's a State at (x, y), open 'Edit State' window.
            - Else, open 'Add State' window at that coordinate.
        """
        selected_state = self._find_state(event.x, event.y)
        selection_tool = SelectionTool(
            canvas=self.canvas,
            automata_manager=self.automata_manager,
            undo_stack=self.undo_stack,
            redo_stack=self.redo_stack
        )
        if selected_state:
            # Edit
            selection_tool.open_state_window(
                state=selected_state,
                x=event.x, y=event.y
            )
        else:
            # Add
            selection_tool.open_state_window(
                x=event.x, y=event.y
            )

    def _find_state(self, x, y):
        """ Find and return the state at the given coordinates. """
        for s in self.automata_manager.states:
            dx, dy = x - s.x, y - s.y
            if (dx**2 + dy**2)**0.5 <= s.radius:
                return s
        return None
