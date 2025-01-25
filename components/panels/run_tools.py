import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from components.utils.constants import ( IMG_SIZE, COLOR_RT_BG, RUN_PAUSES_MS, 
                                        SAVE_WIDTH, SAVE_HEIGHT, AppMode)

from components.utils.logger import operation_logger, error_logger
from components.utils.popup_helper import centered_popup
from components.utils.tooltip import Tooltip


class RunToolsFrame(tk.Frame):
    """ 
        The bottom frame with Run/Pause/Step/Stop/Reload/Save/Load icons and words window.
        Coordinates GUI with run_manager BFS logic.
    """

    def __init__(self, parent, run_mgr, canvas):
        super().__init__(parent, bg=COLOR_RT_BG)
        self.run_mgr = run_mgr
        self.canvas = canvas
        self.running = False
        self.current_setup_window = None
        self.tools_panel_ref = None
        self.words_window_ref = None

        self.after_id = None

        self.icons = {
            "run": self.__load_icon("assets/run.png"),
            "pause": self.__load_icon("assets/pause.png"),
            "step": self.__load_icon("assets/step.png"),
            "stop": self.__load_icon("assets/stop.png"),
            "reload": self.__load_icon("assets/reload.png"),
            "save": self.__load_icon("assets/save.png"),
            "story": self.__load_icon("assets/story.png"),
        }

        # Run button
        self.run_btn = ttk.Button(self, image=self.icons["run"], command=self._on_run)
        self.run_btn.pack(side=tk.LEFT, padx=5, pady=5)
        Tooltip(self.run_btn, f"Run\nRuns the simulation with {RUN_PAUSES_MS}ms per step")

        # Pause button
        self.pause_btn = ttk.Button(self, image=self.icons["pause"], command=self._on_pause)
        self.pause_btn.pack(side=tk.LEFT, padx=5, pady=5)
        Tooltip(self.pause_btn, "Pause\nPause currently running simulation")

        # Step button
        self.step_btn = ttk.Button(self, image=self.icons["step"], command=self._on_step)
        self.step_btn.pack(side=tk.LEFT, padx=5, pady=5)
        Tooltip(self.step_btn, "Step\nRun the simulation one step at a time")

        # Stop button
        self.stop_btn = ttk.Button(self, image=self.icons["stop"], command=self._on_stop)
        self.stop_btn.pack(side=tk.LEFT, padx=5, pady=5)
        Tooltip(self.stop_btn, "Stop\nStop current run and reset")

        # Reload button
        self.reload_btn = ttk.Button(self, image=self.icons["reload"], command=self._on_reload)
        self.reload_btn.pack(side=tk.LEFT, padx=5, pady=5)
        Tooltip(self.reload_btn, "Reload\nClear everything and start fresh")

        # Save button
        self.save_btn = ttk.Button(self, image=self.icons["save"], command=self._on_save_run)
        self.save_btn.pack(side=tk.LEFT, padx=5, pady=5)
        Tooltip(self.save_btn, "Save current run\nProvide name/description for this run")

        # Load button
        self.load_btn = ttk.Button(self, image=self.icons["story"], command=self._on_load_run)
        self.load_btn.pack(side=tk.LEFT, padx=5, pady=5)
        Tooltip(self.load_btn, "Load saved run\nDouble-click on a saved run to load it")


    def __load_icon(self, path):
        """ Load and resize an icon image. """
        try:
            img = Image.open(path)
            img = img.resize(IMG_SIZE)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            error_logger.error(f"Failed to load icon {path}: {e}")
            return None

    def set_current_setup(self, setup_window):
        self.current_setup_window = setup_window
        operation_logger.info("CurrentSetupFrame linked to RunToolsFrame.")

    def set_tools_panel_ref(self, tools_panel):
        self.tools_panel_ref = tools_panel
        operation_logger.info("ToolsPanel linked to RunToolsFrame.")

    def set_words_window_ref(self, words_window):
        self.words_window_ref = words_window
        operation_logger.info("WordsWindow linked to RunToolsFrame.")


    def run_simulation(self):
        """
            Run the BFS simulation step-by-step with a delay.
            Shows "Accepted!" or "Rejected!" message at the end if BFS is finished.
        """
        if self.run_mgr.is_finished():
            if self.run_mgr.is_accepted():
                msg = "Accepted!"
            else:
                msg = "Rejected!"
            messagebox.showinfo("Result", msg)
            operation_logger.info(f"BFS re-run attempt but simulation was finished: {msg}")
            self.finish_run()
            return

        if not self.running:
            return

        snap = self.run_mgr.step()
        if snap:
            self.highlight_step(snap)
            self.after_id = self.after(RUN_PAUSES_MS, self.run_simulation)
        else:
            if self.run_mgr.is_finished():
                if self.run_mgr.is_accepted():
                    msg = "Accepted!"
                else:
                    msg = "Rejected!"
                messagebox.showinfo("Result", msg)
                operation_logger.info(f"BFS simulation ended with result: {msg}")
                self.finish_run()
            else:
                messagebox.showerror(
                    "Error", "Cannot continue simulation until transitions are updated."
                )
                self.run_mgr.pause()

    def finish_run(self):
        """
            Mark BFS as finished, disable editing, and stop automatic stepping.
            If BFS truly ended, the run_manager is set to FINISHED.
        """
        self.running = False
        self.run_mgr.running = False
        if self.tools_panel_ref:
            self.tools_panel_ref.enable_drawing_tools(False)
        operation_logger.info("BFS simulation run finished (no more additions).")

    def highlight_step(self, step):
        """
            Highlight the current BFS step's state in red and update tapes display.
        """
        if not step:
            return
        state_name = step[0]
        self.highlight_state(state_name)
        if self.current_setup_window:
            self.current_setup_window.display_step(step)
        operation_logger.info(f"Highlighted step: {state_name}")

    def highlight_state(self, state_name):
        self.canvas.highlight_state(state_name)

    def _on_save_run(self):
        """
            Save the current run (with name & description) into the database.
        """
        if not self.run_mgr.current_user:
            messagebox.showerror("Error", "No user is currently logged in.")
            error_logger.error("Attempted to save run with no logged-in user.")
            return

        root = self.canvas.winfo_toplevel()
        save_popup = tk.Toplevel(root)
        save_popup.title("Save Run")
        save_popup.geometry(f"{SAVE_WIDTH}x{SAVE_HEIGHT}")
        centered_popup(root, save_popup)

        ttk.Label(save_popup, text="Run Name:").pack(pady=5)
        run_name_var = tk.StringVar()
        run_name_entry = ttk.Entry(save_popup, textvariable=run_name_var, justify='center')
        run_name_entry.pack(pady=5)

        ttk.Label(save_popup, text="Description (optional):").pack()
        desc_text = tk.Text(save_popup, height=4, width=30)
        desc_text.pack(pady=5)

        button_frame = tk.Frame(save_popup)
        button_frame.pack(pady=5)

        def on_ok():
            name_val = run_name_var.get().strip()
            full_desc = name_val
            more_desc = desc_text.get("1.0", tk.END).strip()
            if more_desc:
                full_desc += f" | {more_desc}"
            if not name_val:
                messagebox.showerror("Error", "Please provide at least a Run Name.")
                return
            self.run_mgr.save_current_run(description=full_desc)
            messagebox.showinfo("Saved", "Run history saved successfully!")
            operation_logger.info(f"Run history saved with description: {full_desc}")
            save_popup.destroy()

        def on_cancel():
            save_popup.destroy()

        save_popup.protocol("WM_DELETE_WINDOW", on_cancel)

        ok_button = ttk.Button(button_frame, text="OK", command=on_ok)
        ok_button.pack(side=tk.LEFT, padx=5)
        cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def _on_load_run(self):
        """
            Load a run history from the database. Double-click a listed run to load it.
            After loading, re-draw the automaton and set drawing tools appropriately.
        """
        if not self.run_mgr.current_user:
            messagebox.showerror("Error", "No user is currently logged in.")
            error_logger.error("Attempted to load run without a logged-in user.")
            return

        histories = self.run_mgr.db_manager.list_run_histories(self.run_mgr.current_user)
        if not histories:
            messagebox.showinfo("No Snapshots", "No saved runs for this user.")
            operation_logger.info("No run histories found for user.")
            return

        root = self.canvas.winfo_toplevel()
        load_win = tk.Toplevel(root)
        load_win.title("Load Snapshot")
        load_win.geometry(f"{SAVE_WIDTH}x{SAVE_HEIGHT}")
        centered_popup(root, load_win)

        ttk.Label(load_win, text="Select a snapshot (double click to load):", justify='center').pack(pady=5)
        lb = tk.Listbox(load_win)
        lb.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        records_map = {}
        for i, rec in enumerate(histories):
            rid, desc, automaton_json, hist_json = rec
            record_name = f"ID={rid}: {desc}"
            lb.insert(tk.END, record_name)
            records_map[i] = rec

        def on_select_load(evt):
            selection = lb.curselection()
            if not selection:
                return
            idx = selection[0]
            _, desc, automaton_data_json, history_data_json = records_map[idx]
            import json
            try:
                automaton_data = json.loads(automaton_data_json)
                history_data = json.loads(history_data_json)
            except json.JSONDecodeError as e:
                messagebox.showerror("Error", f"Failed to parse run data: {e}")
                error_logger.error(f"JSON decode error: {e}")
                return

            self.run_mgr.load_run(automaton_data, history_data)
            self.canvas.delete("all")
            self.run_mgr.automata_manager.draw_all(self.canvas)

            if self.words_window_ref:
                self.words_window_ref.refresh()

            if self.current_setup_window:
                self.current_setup_window.display_step(None)

            # Highlight current step if > 0
            if (self.run_mgr.current_step > 0 and
                    self.run_mgr.current_step <= len(self.run_mgr.history)):
                step = self.run_mgr.history[self.run_mgr.current_step - 1]
                self.highlight_step(step)

            # Re-enable or disable drawing tools based on the loaded app_mode
            if self.tools_panel_ref:
                if self.run_mgr.app_mode == AppMode.RUNNING:
                    self.tools_panel_ref.enable_drawing_tools(False)
                elif self.run_mgr.app_mode == AppMode.DRAWING:
                    self.tools_panel_ref.enable_drawing_tools(True)
                else:  # FINISHED
                    self.tools_panel_ref.enable_drawing_tools(False)

            load_win.destroy()
            messagebox.showinfo("Loaded", f"Snapshot '{desc}' loaded successfully.")
            operation_logger.info(f"Run history loaded: {desc}")

        lb.bind("<Double-Button-1>", on_select_load)
        ttk.Label(load_win, text="(Double-click to load)", foreground="gray").pack(pady=5)
        
    def _on_pause(self):
        """ Pause the BFS simulation. """
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        operation_logger.info("BFS simulation paused.")

    def _on_step(self):
        """
            Perform a single BFS step. If BFS is finished, let the user know.
            If transitions need updating, show error.
        """
        if not self.run_mgr.running and self.run_mgr.is_finished():
            response = messagebox.askyesno(
                "Simulation Finished",
                "The previous simulation is finished. Start a new run?"
            )
            if response:
                self.run_mgr.restart()
                self.current_setup_window.display_step(-1)
            else:
                messagebox.showinfo("Run Status", "No changes made.")
            return

        if self.run_mgr.is_finished():
            if self.run_mgr.is_accepted():
                msg = "Accepted!"
            else:
                msg = "Rejected!"
            messagebox.showinfo("Result", msg)
            operation_logger.info(f"BFS simulation ended with result: {msg}")
        
        if not self.run_mgr.can_continue_run():
            messagebox.showerror("Error", "Cannot continue simulation until transitions are updated.")
            return

        if not self.run_mgr.running:
            self.run_mgr.running = True
            self.run_mgr.app_mode = AppMode.RUNNING
            self.run_mgr.initialize_backend()
            self.run_mgr.load_history()

        if self.tools_panel_ref:
            self.tools_panel_ref.enable_drawing_tools(False)

        snap = self.run_mgr.step()
        if snap:
            self.highlight_step(snap)
            

    def _on_stop(self):
        """
            Stop the BFS simulation entirely, resetting everything
            and returning to the drawing state.
        """
        self._on_pause()
        self.run_mgr.restart()
        self.canvas.highlight_state(None)
        self.current_setup_window.display_step(0)

        if self.tools_panel_ref:
            self.tools_panel_ref.enable_drawing_tools(True)

        messagebox.showinfo("Stopped", "Simulation has been reset.")
        operation_logger.info("BFS simulation stopped and reset.")

    def _on_reload(self):
        """
            Clear everything from the automaton: states, transitions, words.
            Return to a clean canvas and drawing mode.
        """
        self._on_pause()
        self.run_mgr.clear_all()
        self.canvas.delete("all")
        if self.words_window_ref:
            self.words_window_ref.refresh()
        if self.current_setup_window:
            self.current_setup_window.display_step(None)
        if self.tools_panel_ref:
            self.tools_panel_ref.enable_drawing_tools(True)
        messagebox.showinfo("Reloaded", "All states and transitions have been cleared.")
        operation_logger.info("BFS simulation reloaded (clear).")

    def _on_run(self):
        """
            Start or continue the BFS simulation. If the BFS is already finished,
            ask the user if they want a new run. If transitions are out-of-date,
            show an error. Otherwise proceed from where we left off.
        """
        if self.run_mgr.is_finished():
            response = messagebox.askyesno(
                "Simulation Finished",
                "The previous simulation is finished. Start a new run?"
            )
            if response:
                self.run_mgr.restart()  # reset to drawing
                self.current_setup_window.display_step(0)
                
            else:
                messagebox.showinfo("Run Status", "No changes made.")
            return

        if not self.run_mgr.can_continue_run():
            messagebox.showerror("Error", "Cannot continue simulation until transitions are updated.")
            return

        if not self.running:
            if len(self.run_mgr.history) == 0:
                self.run_mgr.initialize_backend()
                self.run_mgr.load_history()

        self.run_mgr.app_mode = AppMode.RUNNING
        self.run_mgr.running = True
        if self.tools_panel_ref:
            self.tools_panel_ref.enable_drawing_tools(False)

        self.running = True
        self.run_simulation()
        operation_logger.info("BFS simulation started (run).")