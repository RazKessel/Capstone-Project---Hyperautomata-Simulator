import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from components.buttons.add_state_button import AddStateTool
from components.buttons.add_transition_button import AddTransitionTool
from components.buttons.selection_button import SelectionTool

from components.utils.logger import operation_logger, error_logger
from components.utils.tooltip import Tooltip
from components.utils.constants import IMG_SIZE, COLOR_DT_BG

class ToolsFrame(tk.Frame):
    """
    A side panel containing tools for interacting with the automata canvas.
    Provides functionality to:
    - Add states and transitions
    - Select and modify elements
    - Undo and redo actions
    - Adjust word count and zoom level
    """

    def __init__(self, parent, automata_mgr, canvas, undo_stack, redo_stack):
        """
        Initialize the ToolsFrame with various tools and controls.

        Args:
            parent: The parent widget.
            automata_mgr: The AutomataManager instance.
            canvas: The canvas to draw on.
            undo_stack: Stack to track undoable actions.
            redo_stack: Stack to track redoable actions.
        """
        super().__init__(parent, bg=COLOR_DT_BG)
        self.automata_mgr = automata_mgr
        self.canvas = canvas
        self.undo_stack = undo_stack
        self.redo_stack = redo_stack
        self.active_tool = None
        self.tools = {}
        self.buttons_dict = {}

        # Load icons for the tools
        self.icons = {
            "add_state": self.load_icon("assets/circle.png"),
            "add_transition": self.load_icon("assets/arrow.png"),
            "select": self.load_icon("assets/arrow_select.png"),
            "undo": self.load_icon("assets/arrow_back.png"),
            "redo": self.load_icon("assets/arrow_forward.png"),
            "zoom_in": self.load_icon("assets/zoom_in.png"),
            "zoom_out": self.load_icon("assets/zoom_out.png"),
        }

        # Configure button styles
        style = ttk.Style()
        style.configure("PressedToolButton.TButton", relief="sunken")
        style.configure("Danger.TButton", foreground="red")

        # Add word count controls
        self.setup_word_count_controls()

        # Add tool buttons
        self.setup_tool_buttons()

        # Add undo/redo/zoom buttons
        self.setup_action_buttons()

    def load_icon(self, path):
        """
        Load and resize an icon image.

        Args:
            path (str): The file path of the image to load.

        Returns:
            PhotoImage: The loaded and resized image, or None if loading fails.
        """
        try:
            img = Image.open(path)
            img = img.resize(IMG_SIZE)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            error_logger.error(f"Failed to load icon {path}: {e}")
            return None

    def setup_word_count_controls(self):
        """ Set up controls for adjusting the word count. """
        wc_frame = tk.Frame(self, bg=COLOR_DT_BG)
        wc_frame.pack(pady=5)
        ttk.Label(wc_frame, text="Word Count:").pack(side=tk.LEFT, padx=2)
        self.word_count_var = tk.IntVar(value=self.automata_mgr.word_count)
        self.wc_entry = ttk.Entry(
            wc_frame, textvariable=self.word_count_var, width=4, justify='center')
        self.wc_entry.pack(side=tk.LEFT, padx=2)

        plus_btn = ttk.Button(wc_frame, text="+", width=3,
                              command=self.increment_word_count)
        plus_btn.pack(side=tk.LEFT, padx=2)
        minus_btn = ttk.Button(wc_frame, text="-", width=3,
                               command=self.decrement_word_count)
        minus_btn.pack(side=tk.LEFT, padx=2)

    def setup_tool_buttons(self):
        """ Set up buttons for tools like Add State, Add Transition, and Selection. """
        btn_add_state = self.add_tool_button(
            label="Add State",
            tool_obj=AddStateTool(self.canvas, self.automata_mgr,
                                  self.undo_stack, self.redo_stack),
            icon=self.icons["add_state"],
            tooltip_text="Add State\nClick on canvas to add state"
        )
        btn_add_transition = self.add_tool_button(
            label="Add Transition",
            tool_obj=AddTransitionTool(
                self.canvas, self.automata_mgr, self.undo_stack, self.redo_stack),
            icon=self.icons["add_transition"],
            tooltip_text="Add Transition\nClick on two states to add transition"
        )
        btn_select = self.add_tool_button(
            label="Selection",
            tool_obj=SelectionTool(self.canvas, self.automata_mgr,
                                   self.undo_stack, self.redo_stack),
            icon=self.icons["select"],
            tooltip_text="Selection\nLeft-click on state/transition to edit.\nRight-click + drag on state to move."
        )

        self.buttons_dict["Add State"] = btn_add_state
        self.buttons_dict["Add Transition"] = btn_add_transition
        self.buttons_dict["Selection"] = btn_select

    def setup_action_buttons(self):
        """ Set up buttons for undo, redo, and zoom actions. """
        undo_btn = ttk.Button(self, image=self.icons["undo"],
                              command=self.undo)
        undo_btn.pack(pady=3)
        Tooltip(undo_btn, "Undo\nRevert the last action.")

        redo_btn = ttk.Button(self, image=self.icons["redo"],
                              command=self.redo)
        redo_btn.pack(pady=3)
        Tooltip(redo_btn, "Redo\nReapply the last undone action.")

        zoom_in_btn = ttk.Button(self, image=self.icons["zoom_in"],
                                 command=self.zoom_in)
        zoom_in_btn.pack(pady=3)
        Tooltip(zoom_in_btn, "Zoom In\nIncrease the canvas view size.")

        zoom_out_btn = ttk.Button(self, image=self.icons["zoom_out"],
                                  command=self.zoom_out)
        zoom_out_btn.pack(pady=3)
        Tooltip(zoom_out_btn, "Zoom Out\nDecrease the canvas view size.")

    def add_tool_button(self, label, tool_obj, icon, tooltip_text):
        """
        Add a button for a specific tool to the tools panel.

        Args:
            label (str): The name of the tool.
            tool_obj: The tool object associated with the button.
            icon (PhotoImage): The icon for the button.
            tooltip_text (str): The tooltip text for the button.

        Returns:
            ttk.Button: The created button.
        """
        btn = ttk.Button(self, image=icon, command=lambda: self.activate_tool(label))
        btn.pack(pady=3)
        self.tools[label] = (btn, tool_obj)
        Tooltip(btn, tooltip_text)
        operation_logger.info(f"Tool button added: {label}")
        return btn

    def activate_tool(self, label):
        """ Activate the selected tool and deactivate the previous one. """
        if self.active_tool:
            self.reset_tool(self.active_tool)
        self.active_tool = label
        btn, t = self.tools[label]
        btn.config(style="PressedToolButton.TButton")
        t.activate()
        operation_logger.info(f"Tool activated: {label}")

    def reset_tool(self, label):
        """ Reset the given tool to its default state. """
        btn, t = self.tools[label]
        btn.config(style="TButton")
        t.deactivate()
        self.active_tool = None
        operation_logger.info(f"Tool reset: {label}")

    def enable_drawing_tools(self, enable: bool):
        """ Enable or disable drawing tools based on the application's state. """
        state_ = tk.NORMAL if enable else tk.DISABLED
        for k in ["Add State", "Add Transition"]:
            if k in self.buttons_dict:
                self.buttons_dict[k].config(state=state_)
        operation_logger.info(
            f"Drawing tools {'enabled' if enable else 'disabled'}.")

    # Word Count
    def increment_word_count(self):
        """ Increase the word count and update the automata. """
        self.word_count_var.set(self.word_count_var.get() + 1)
        self.set_word_count()

    def decrement_word_count(self):
        """ Decrease the word count and ensure it doesn't go below 1. """
        val = self.word_count_var.get()
        if val > 1:
            self.word_count_var.set(val - 1)
            self.set_word_count()

    def set_word_count(self):
        """ Update the word count in the automata manager and redraw the canvas. """
        val = self.word_count_var.get()
        self.automata_mgr.set_word_count(val)
        self.canvas.delete("all")
        self.automata_mgr.draw_all(self.canvas)
        operation_logger.info(f"Word count set to: {val}")

    # Undo/Redo
    def undo(self):
        """ Perform an undo operation. """
        if not self.undo_stack:
            messagebox.showinfo("Undo", "Nothing to undo.")
            operation_logger.info("Undo attempted with empty stack.")
            return
        action, obj = self.undo_stack.pop()
        if action == "add_state":
            self.remove_state_obj(obj)
        elif action == "add_transition":
            self.remove_transition_obj(obj)
        elif action == "remove_state":
            st, tr_list = obj
            self.automata_mgr.states.append(st)
            st.draw(self.canvas)
            for tr in tr_list:
                self.automata_mgr.transitions.append(tr)
                tr.source.outgoing_transitions.append(tr)
                tr.target.incoming_transitions.append(tr)
                tr.draw(self.canvas)
        elif action == "remove_transition":
            tr = obj
            self.automata_mgr.transitions.append(tr)
            tr.source.outgoing_transitions.append(tr)
            tr.target.incoming_transitions.append(tr)
            tr.draw(self.canvas)

        self.redo_stack.append((action, obj))
        operation_logger.info(f"Undo performed: {action} for {obj}")

    def redo(self):
        """ Perform a redo operation. """
        if not self.redo_stack:
            messagebox.showinfo("Redo", "Nothing to redo.")
            operation_logger.info("Redo attempted with empty stack.")
            return
        action, obj = self.redo_stack.pop()
        if action == "add_state":
            self.automata_mgr.states.append(obj)
            obj.draw(self.canvas)
        elif action == "add_transition":
            self.automata_mgr.transitions.append(obj)
            obj.source.outgoing_transitions.append(obj)
            obj.target.incoming_transitions.append(obj)
            obj.draw(self.canvas)
        elif action == "remove_state":
            st, _ = obj
            self.remove_state_obj(st)
        elif action == "remove_transition":
            self.remove_transition_obj(obj)

        self.undo_stack.append((action, obj))
        operation_logger.info(f"Redo performed: {action} for {obj}")

    def remove_state_obj(self, st):
        """ Remove a state and its transitions from the automata manager and canvas. """
        if st.canvas_id:
            self.canvas.delete(st.canvas_id)
        if st.label_id:
            self.canvas.delete(st.label_id)
        for exid in st.extra_ids:
            self.canvas.delete(exid)
        if st in self.automata_mgr.states:
            self.automata_mgr.states.remove(st)
        all_trans = st.outgoing_transitions + st.incoming_transitions
        for t in all_trans:
            self.remove_transition_obj(t)
        operation_logger.info(f"State removed via undo: {st.name}")

    def remove_transition_obj(self, tr):
        """ Remove a transition from the automata manager and canvas. """
        for cid in tr.canvas_ids:
            self.canvas.delete(cid)
        if tr in self.automata_mgr.transitions:
            self.automata_mgr.transitions.remove(tr)
        if tr in tr.source.outgoing_transitions:
            tr.source.outgoing_transitions.remove(tr)
        if tr in tr.target.incoming_transitions:
            tr.target.incoming_transitions.remove(tr)
        operation_logger.info(f"Transition removed via undo: {tr.source.name} -> {tr.target.name}")

    def zoom_in(self):
        """ Zoom in the canvas view. """
        self.canvas.scale("all", 0, 0, 1.2, 1.2)
        operation_logger.info("Canvas zoomed in.")

    def zoom_out(self):
        """ Zoom out the canvas view. """
        self.canvas.scale("all", 0, 0, 0.8, 0.8)
        operation_logger.info("Canvas zoomed out.")
