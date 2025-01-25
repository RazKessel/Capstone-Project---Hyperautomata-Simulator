import tkinter as tk
from tkinter import messagebox, ttk

from components.utils.logger import operation_logger, error_logger
from components.utils.constants import COLOR_BLACK, COLOR_RED, POP_WIDTH, POP_HEIGHT
from components.utils.popup_helper import centered_popup

class SelectionTool:
    """
        Tool for selecting and editing states or transitions.
        Supports:
          - Normal click to edit states or transitions.
          - Right-click drag to move states
    """

    def __init__(self, canvas, automata_manager, undo_stack, redo_stack):
        self.canvas = canvas
        self.automata_mgr = automata_manager
        self.undo_stack = undo_stack
        self.redo_stack = redo_stack
        self.dragged_state = None
        self.temp_trans_states = []
        self.run_mgr = None 

    def activate(self):
        """ Activate the tool by binding mouse events. """
        self.canvas.bind("<Button-1>", self._on_left_click)
        self.canvas.bind("<Button-3>", self._on_right_click)
        operation_logger.info("SelectionTool activated.")

    def deactivate(self):
        """ Deactivate the tool - unbind mouse events and clear selections. """
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-3>")
        self.canvas.unbind("<B3-Motion>")
        self.canvas.unbind("<ButtonRelease-3>")
        self.temp_trans_states.clear()
        operation_logger.info("SelectionTool deactivated.")

    def _on_left_click(self, event):
        """ Handle left mouse click for selecting or editing states/transitions. """
        st = self._find_state(event.x, event.y)
        if st:
            self.open_state_window(st, event.x_root, event.y_root)
        else:
            tr = self._find_transition(event.x, event.y)
            if tr:
                self.open_transition_window(src=None, tgt=None,
                                            existing_transition=tr)

    def _on_right_click(self, event):
        """ Handle right mouse click for dragging states. """
        st = self._find_state(event.x, event.y)
        if st:
            self.dragged_state = st
            self.canvas.bind("<B3-Motion>", self._on_drag)
            self.canvas.bind("<ButtonRelease-3>", self._on_release)
            operation_logger.info(f"Started dragging state: {st.name}")

    def _on_drag(self, event):
        """ Handle the dragging of a state. """
        if self.dragged_state:
            self.dragged_state.move(self.canvas, event.x, event.y)
            for out_tr in self.dragged_state.outgoing_transitions:
                out_tr.redraw(self.canvas)
            for in_tr in self.dragged_state.incoming_transitions:
                in_tr.redraw(self.canvas)

    def _on_release(self, event):
        """ Handle the release of a dragged state. """
        if self.dragged_state:
            operation_logger.info(f"Finished dragging state: {self.dragged_state.name}")
            self.dragged_state = None
            self.canvas.unbind("<B3-Motion>")
            self.canvas.unbind("<ButtonRelease-3>")

    def _find_state(self, x, y):
        """ Find and return the state at the given coordinates. """
        for s in self.automata_mgr.states:
            dx, dy = x - s.x, y - s.y
            if (dx**2 + dy**2)**0.5 <= s.radius:
                return s
        return None

    def _find_transition(self, x, y):
        """ Find and return the transition at the given coordinates. """
        closest = self.canvas.find_closest(x, y)
        for tr in self.automata_mgr.transitions:
            if any(cid == closest[0] for cid in tr.canvas_ids):
                return tr
        return None

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
        operation_logger.info(f"Transition removed: {tr.source.name} -> {tr.target.name}")

    def remove_state_obj(self, st):
        """ Remove a state and its associated transitions from the automata manager and canvas. """
        if st.canvas_id:
            self.canvas.delete(st.canvas_id)
        if st.label_id:
            self.canvas.delete(st.label_id)
        for exid in st.extra_ids:
            self.canvas.delete(exid)
        if st in self.automata_mgr.states:
            self.automata_mgr.states.remove(st)

        trans_to_remove = st.outgoing_transitions + st.incoming_transitions
        for t in trans_to_remove:
            self.remove_transition_obj(t)
        operation_logger.info(f"State and transitions removed: {st.name}")

    def open_transition_window(self, src=None, tgt=None, existing_transition=None):
        """ Open a window to add/edit a transition. """
        root = self.canvas.winfo_toplevel()
        is_edit = existing_transition is not None

        win = tk.Toplevel(root)
        win.title("Edit Transition" if is_edit else "Add Transition")
        win.geometry(f"{POP_WIDTH}x{POP_HEIGHT}")
        centered_popup(root, win)

        if is_edit:
            src = existing_transition.source
            tgt = existing_transition.target
            vectors_init = existing_transition.transition_vectors
        else:
            vectors_init = [tuple([""] * self.automata_mgr.word_count)]

        frame_vec = tk.Frame(win)
        frame_vec.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        vector_inputs = []

        def add_vector_line(vals=None):
            """ Add a new line of vector inputs. """
            rowframe = tk.Frame(frame_vec)
            rowframe.pack(fill=tk.X, pady=5)

            rowgrid = tk.Frame(rowframe)
            rowgrid.pack(anchor="center")

            entries = []
            for c, v in enumerate(vals if vals else [""]*self.automata_mgr.word_count):
                e = tk.Entry(rowgrid, width=4, justify='center')
                e.insert(0, v)
                e.grid(row=0, column=c, padx=3)
                entries.append(e)

            rm_btn = ttk.Button(
                rowgrid, text="X", style="Danger.TButton",
                command=lambda: remove_line(rowframe, rowgrid, entries)
            )
            rm_btn.grid(row=0, column=len(entries), padx=3)
            vector_inputs.append(entries)

        def remove_line(outer_frame, rowgrid, row_entries):
            vector_inputs.remove(row_entries)
            rowgrid.destroy()
            outer_frame.destroy()
            operation_logger.info("Transition condition line removed.")
        
        # Populate existing vectors
        for vec in vectors_init:
            add_vector_line(vec)
            
        # Button to add more condition vectors
        btn_add_cond = ttk.Button(win, text="Add Condition",
                                 command=lambda: add_vector_line(None))
        btn_add_cond.pack(pady=5)

        def on_save():
            """ Save the transition after validation. """
            new_vecs = []
            for row in vector_inputs:
                arr = [e.get().strip() or '#' for e in row]
                if len(arr) != self.automata_mgr.word_count:
                    messagebox.showerror("Error", "Vector length mismatch.")
                    error_logger.error("Transition save: vector length mismatch.")
                    return
                new_vecs.append(tuple(arr))

            if is_edit:
                existing_transition.transition_vectors = new_vecs
                existing_transition.clear(self.canvas)
                existing_transition.draw(self.canvas)
                # revert color to black if updated transition
                existing_transition.set_color(self.canvas, COLOR_BLACK)
                existing_transition.requires_update = False
                operation_logger.info(f"Transition edited: {src.name} -> {tgt.name}")
            else:
                new_tr = self.automata_mgr.add_transition(src, tgt, new_vecs)
                parallels = [t for t in self.automata_mgr.transitions
                             if (t.source == src and t.target == tgt)]
                new_tr.offset_index = len(parallels) - 1
                new_tr.draw(self.canvas)
                self.undo_stack.append(("add_transition", new_tr))
                self.redo_stack.clear()
                operation_logger.info(f"New transition added: {src.name} -> {tgt.name}")

            # Mark transitions updated if BFS is running
            if self.run_mgr and self.run_mgr.running:
                self.run_mgr.updated_transitions = True
            win.destroy()

        def on_delete():
            if not is_edit:
                return
            self.undo_stack.append(("remove_transition", existing_transition))
            self.redo_stack.clear()
            self.remove_transition_obj(existing_transition)
            operation_logger.info(
                f"Transition deleted: {existing_transition.source.name} -> {existing_transition.target.name}"
            )
            if self.run_mgr and self.run_mgr.running:
                self.run_mgr.updated_transitions = True
            win.destroy()

        def on_close():
            # If user just closes via [X], we do nothing special.
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)

        frm_btn = tk.Frame(win)
        frm_btn.pack(pady=5)
        ttk.Button(frm_btn, text="Save", command=on_save).pack(side=tk.LEFT, padx=5)
        if is_edit:
            ttk.Button(frm_btn, text="Delete", style="Danger.TButton", command=on_delete).pack(side=tk.LEFT, padx=5)

    def open_state_window(self, state=None, x=None, y=None):
        """ Open window to add/edit state """
        root = self.canvas.winfo_toplevel()
        is_edit = state is not None

        win = tk.Toplevel(root)
        win.title("Edit State" if is_edit else "Add State")
        win.geometry(f"{POP_WIDTH}x{POP_HEIGHT}")
        centered_popup(root, win)

        if is_edit:
            name_var = tk.StringVar(value=state.name)
            start_var = tk.BooleanVar(value=state.is_start)
            accept_var = tk.BooleanVar(value=state.is_accept)
        else:
            name_var = tk.StringVar(value=f"q{len(self.automata_mgr.states)}")
            start_var = tk.BooleanVar(value=False)
            accept_var = tk.BooleanVar(value=False)

        ttk.Label(win, text=("Edit State" if is_edit else "Add State"),
                 font=("Arial", 12), justify='center').pack(pady=5)
        ttk.Label(win, text="Name:", justify='center').pack(pady=2)
        tk.Entry(win, textvariable=name_var, justify='center').pack(pady=2)
        ttk.Checkbutton(win, text="Start", variable=start_var).pack(pady=2)
        ttk.Checkbutton(win, text="Accept", variable=accept_var).pack(pady=2)

        def on_save():
            """ Save or update the state after validation. """
            st_name = name_var.get().strip()
            if not st_name:
                messagebox.showerror("Error", "State name cannot be empty.")
                error_logger.error("Attempt to add/edit a state with empty name.")
                return
            if is_edit:
                if st_name != state.name and any(s.name == st_name for s in self.automata_mgr.states):
                    messagebox.showerror("Error", f"State '{st_name}' already exists.")
                    error_logger.error(f"Rename state => name already exists: {st_name}")
                    return
                state.name = st_name
                state.is_start = start_var.get()
                state.is_accept = accept_var.get()
                state.draw(self.canvas)
                self.undo_stack.append(("edit_state", state))
                self.redo_stack.clear()
                operation_logger.info(f"State edited: {st_name}")
            else:
                if any(s.name == st_name for s in self.automata_mgr.states):
                    messagebox.showerror("Error", f"State '{st_name}' already exists.")
                    error_logger.error(f"Add state => name already exists: {st_name}")
                    return
                new_st = self.automata_mgr.add_state(
                    name=st_name, x=x, y=y,
                    is_start=start_var.get(),
                    is_accept=accept_var.get()
                )
                new_st.draw(self.canvas)
                self.undo_stack.append(("add_state", new_st))
                self.redo_stack.clear()
                operation_logger.info(f"State added: {st_name} at ({x}, {y})")
            win.destroy()

        def on_delete():
            """ Delete the selected state after confirmation. """
            if not is_edit:
                return
            if messagebox.askyesno("Delete State", f"Are you sure you want to delete '{state.name}'?"):
                transitions = state.outgoing_transitions + state.incoming_transitions
                self.undo_stack.append(("remove_state", (state, transitions)))
                self.redo_stack.clear()
                self.remove_state_obj(state)
                operation_logger.info(f"State deleted: {state.name}")
                if self.run_mgr and self.run_mgr.running:
                    self.run_mgr.updated_transitions = True
                win.destroy()

        def on_close():
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)

        frm_btn = tk.Frame(win)
        frm_btn.pack(pady=5)
        ttk.Button(frm_btn, text="Save", command=on_save).pack(side=tk.LEFT, padx=5)
        if is_edit:
            ttk.Button(frm_btn, text="Delete", style="Danger.TButton", command=on_delete).pack(side=tk.LEFT, padx=5)
