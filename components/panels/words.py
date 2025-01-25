import tkinter as tk
from tkinter import ttk, messagebox

from components.utils.logger import operation_logger, error_logger
from components.utils.constants import COLOR_WW_BG, POP_WIDTH, POP_HEIGHT, AppMode
from components.utils.popup_helper import centered_popup
from components.utils.tooltip import Tooltip


class WordsFrame(tk.Frame):
    """
    Displays the list of words. Supports:
     - Adding words (if not finished).
     - Editing words during run or drawing on double click.
     - Removing words only if not running on double click.
    """

    def __init__(self, parent, run_mgr, tool_window, automata_manager, run_tools):
        super().__init__(parent, bg=COLOR_WW_BG)
        self.run_mgr = run_mgr
        self.tool_window = tool_window
        self.automata_manager = automata_manager
        self.run_tools = run_tools

        ttk.Label(self, text="Words Window", justify='center').pack(pady=5)

        ttk.Label(
            self,
            text="Double-click a word to edit.",
            wraplength=200
        ).pack(padx=5)

        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.listbox.bind("<Double-Button-1>", self._on_click_word)

        self.add_button = ttk.Button(self, text="Add Word", command=self._on_add_word)
        self.add_button.pack(pady=5)
        Tooltip(self.add_button, "Add Word\nClick to add a new word")
        operation_logger.info("WordsFrame initialized.")

    def refresh(self):
        """ Refresh the list of words displayed. """
        self.listbox.delete(0, tk.END)
        for w in self.run_mgr.words:
            self.listbox.insert(tk.END, w)

        # Disable add button if run finished
        if self.run_mgr.is_finished():
            self.add_button.config(state=tk.DISABLED)
        else:
            self.add_button.config(state=tk.NORMAL)
        operation_logger.info("WordsFrame refreshed.")

    def open_edit_window(self, idx, old_word):
        """ Open a window to edit/delete a selected word. """
        root = self.winfo_toplevel()
        win = tk.Toplevel(root)
        win.title("Edit Word")
        win.geometry(f"{POP_WIDTH}x{POP_HEIGHT}")
        centered_popup(root, win)

        ttk.Label(win, text=f"Current word: {old_word}", justify='center').pack(pady=5)
        new_var = tk.StringVar(value=old_word)
        ttk.Entry(win, textvariable=new_var, justify='center').pack(pady=5)

        def on_change():
            """ Change the selected word after validation. """
            new_w = new_var.get().strip()
            if new_w:
                try:
                    self.run_mgr.change_word(idx, new_w)
                    self.automata_manager.draw_all(self.run_tools.canvas)
                    self.refresh()
                    operation_logger.info(f"Word changed from {old_word} to {new_w}")
                except Exception as ex:
                    messagebox.showerror("Error", f"Failed to change word: {ex}")
                    error_logger.error(f"Error changing word: {ex}")
            win.destroy()

        def on_delete():
            """ Delete the selected word if the simulation is not running and not finished. """
            if self.run_mgr.running and not self.run_mgr.is_finished():
                messagebox.showerror(
                    "Error", "Cannot delete a word while the simulation is running."
                )
                error_logger.warning("Attempted to delete word during run.")
                return
            try:
                self.run_mgr.remove_word(idx)
                self.automata_manager.draw_all(self.run_tools.canvas)
                self.refresh()
                operation_logger.info(f"Word deleted at index {idx}")
            except Exception as ex:
                messagebox.showerror("Error", f"Failed to delete word: {ex}")
                error_logger.error(f"Error deleting word: {ex}")
            win.destroy()

        def on_close():
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)

        frm = tk.Frame(win)
        frm.pack(pady=5)

        ttk.Button(frm, text="Change", command=on_change).pack(side=tk.LEFT, padx=5)
        ttk.Button(frm, text="Delete", style="Danger.TButton", command=on_delete).pack(side=tk.LEFT, padx=5)

    def tkraise(self, aboveThis=None):
        """ Override tkraise to refresh the list when the frame is raised. """
        super().tkraise(aboveThis)
        self.refresh()

    def _on_add_word(self):
        """ Prompt user to add a new word if not finished the run. """
        if self.run_mgr.is_finished():
            messagebox.showerror(
                "Error", "Cannot add words after the simulation has finished. Please start a new run.")
            error_logger.error("Attempted to add word after simulation finished.")
            return

        root = self.winfo_toplevel()
        popup = tk.Toplevel(root)
        popup.title("Add Word")
        popup.geometry(f"{POP_WIDTH}x{POP_HEIGHT}")
        centered_popup(root, popup)

        ttk.Label(popup, text="Enter a new word:", justify='center').pack(pady=10)
        word_var = tk.StringVar()
        ttk.Entry(popup, textvariable=word_var, justify='center').pack(pady=5)

        def on_submit():
            w = word_var.get().strip()
            if w:
                try:
                    self.run_mgr.add_word(w)
                    # Force a draw-all so transitions show color after change
                    self.automata_manager.draw_all(self.run_tools.canvas)
                    self.refresh()
                    if len(self.run_mgr.words) > self.automata_manager.word_count:
                        self.tool_window.word_count_var.set(
                            len(self.run_mgr.words))
                        self.tool_window.set_word_count()

                    # Highlight the current state if simulation is running
                    if self.run_mgr.app_mode == AppMode.RUNNING and self.run_mgr.current_step > 0:
                        snap = None
                        if self.run_mgr.current_step <= len(self.run_mgr.history):
                            snap = self.run_mgr.history[self.run_mgr.current_step - 1]
                        if snap:
                            self.run_tools.highlight_state(snap[0])

                    operation_logger.info(f"Word added: {w}")
                    popup.destroy()
                except Exception as ex:
                    messagebox.showerror("Error", f"Failed to add word: {ex}")
                    error_logger.error(f"Exception while adding word: {ex}")
            else:
                messagebox.showerror("Error", "Word cannot be empty.")

        def on_cancel():
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_cancel)

        ttk.Button(popup, text="Add", command=on_submit).pack(pady=10)

    def _on_click_word(self, event):
        """ Handle double-click to edit or remove a word. """
        idx = self.listbox.curselection()
        if not idx:
            return
        index = idx[0]
        old_word = self.run_mgr.words[index]
        self.open_edit_window(index, old_word)
