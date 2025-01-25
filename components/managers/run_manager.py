import copy
from tkinter import messagebox

from backend.automata import Automata
from backend.manager import Manager
from backend.tape import Tape
from backend.symbolVector import SymbolVector
from backend.transition import Transition

from components.utils.logger import operation_logger, error_logger
from components.utils.constants import AppMode, COLOR_BLACK, COLOR_UPDATED
from components.utils.manager_serializer import serialize_manager, deserialize_manager


class RunManager:
    """
    Coordinates BFS logic, partial BFS updates, user actions (word add/remove),
    DB saving/loading, and tracks app_mode: 'drawing'/'running'.
    """

    def __init__(self, automata_manager, db_manager, current_user):
        self.automata_manager = automata_manager
        self.db_manager = db_manager
        self.current_user = current_user

        self.words = []
        self.history = []
        self.current_step = 0
        self.manager = None
        self.canvas = None

        self.running = False
        self.updated_during_run = False
        self.history_backup = []
        self.updated_transitions = False
        self.app_mode = AppMode.DRAWING

        operation_logger.info(f"RunManager initialized for user: {self.current_user}")

    def set_canvas(self, canvas):
        self.canvas = canvas

    def initialize_backend(self):
        """ Build the backend Automata from GUI states/transitions and tapes from self.words. """
        try:
            automata = Automata()
            for gui_state in self.automata_manager.states:
                automata.add_state(gui_state.name, is_accept=gui_state.is_accept)
                if gui_state.is_start:
                    automata.set_start_state(gui_state.name)

            for gui_tr in self.automata_manager.transitions:
                source = gui_tr.source.name
                target = gui_tr.target.name
                for vec in gui_tr.transition_vectors:
                    sym_vec = SymbolVector(list(vec))
                    for c in vec:
                        automata.alphabet.add(c)
                    b_tr = Transition(fromState=source, symbols_vector=sym_vec, targetState=target)
                    automata.add_transition(b_tr)

            tapes = [Tape(w) for w in self.words]
            self.manager = Manager(automata, tapes)
            operation_logger.info("Backend Manager initialized.")

            if automata.start_state is None:
                self.history = []
                self.current_step = 0
                operation_logger.warning("No start state in automata. Emptied history.")
            else:
                snap = [automata.start_state] + [0] * len(tapes)
                self.history = self.manager.update([snap])
                self.current_step = 0
                operation_logger.info("Initial BFS history snapshot created.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize backend: {e}")
            error_logger.error(f"Failed to initialize backend: {e}")

    def load_history(self):
        """ Return the current history. """
        return self.history

    def is_finished(self):
        return self.app_mode == AppMode.FINISHED

    def can_continue_run(self):
        """ True if no transition requires update. """
        for tr in self.automata_manager.transitions:
            if tr.requires_update:
                return False
        return True

    def __update_run_history(self, new_word=True):
        """ Update the run history when words are added or removed during a run. """
        self.history_backup = self.history[:self.current_step]
        for snap in self.history_backup:
            while len(snap) < (len(self.words) + 1):
                if new_word:
                    snap.append(0)
                else:
                    break
        self.updated_during_run = True

    def simulate_from_updated_history(self):
        """ Simulate BFS steps from the updated history backup. """
        if not self.manager or not self.history_backup:
            return
        last_snap = self.history_backup[-1]
        positions = last_snap[1:]
        for i, tape in enumerate(self.manager.tapes):
            if i < len(positions):
                pos = positions[i]
                tape.currentPos = pos
                tape.symbol = tape.symbols[pos] if pos < len(tape.symbols) else '#'

        self.history = self.manager.update(copy.deepcopy(self.history_backup))
        self.current_step = len(self.history_backup)
        self.updated_during_run = False

    def add_word(self, new_word):
        """ Add a new word to the simulation. """
        if self.is_finished():
            raise Exception("Cannot add words after the simulation has finished.")
        if not new_word:
            return
        self.words.append(new_word)
        operation_logger.info(f"Word added: {new_word}")

        if self.running:
            self.__update_run_history(new_word=True)
            self.simulate_from_updated_history()
            if self.manager:
                self.manager.tapes.append(Tape(new_word))
            # Mark all transitions as needing update and color them
            for tr in self.automata_manager.transitions:
                if self.canvas:
                    tr.set_color(self.canvas, COLOR_UPDATED)
                tr.requires_update = True

    def change_word(self, idx, new_word):
        """ Change an existing word in the simulation. """
        if 0 <= idx < len(self.words):
            old_word = self.words[idx]
            self.words[idx] = new_word
            operation_logger.info(f"Word changed from {old_word} to {new_word} at idx={idx}")

            if self.running:
                partial = self.history[:self.current_step]
                if partial:
                    last_snap = partial[-1]
                    if (idx + 1) < len(last_snap):
                        last_snap[idx + 1] = 0
                self.history_backup = partial
                if self.manager and idx < len(self.manager.tapes):
                    self.manager.tapes[idx].symbols = new_word
                self.simulate_from_updated_history()

                # Mark transitions as needing update
                for tr in self.automata_manager.transitions:
                    if self.canvas:
                        tr.set_color(self.canvas, COLOR_UPDATED)
                    tr.requires_update = True

    def remove_word(self, idx=None):
        """ Remove a word from the simulation. """
        if not self.words:
            return
        if idx is None or idx >= len(self.words):
            removed_word = self.words.pop()
            if self.manager and self.manager.tapes:
                self.manager.tapes.pop()
            operation_logger.info(f"Word removed: {removed_word}")
        else:
            removed_word = self.words.pop(idx)
            if self.manager and idx < len(self.manager.tapes):
                self.manager.tapes.pop(idx)
            operation_logger.info(f"Word removed at index {idx}: {removed_word}")

        if self.running:
            self.__update_run_history(new_word=False)
            self.simulate_from_updated_history()

    def step(self):
        """ Perform a single step in the BFS simulation. """
        if self.running and not self.can_continue_run():
            return None

        self.running = True
        self.app_mode = AppMode.RUNNING
        if self.updated_transitions:
            self.update_transitions_in_backend()
            self.updated_transitions = False

        if self.current_step < len(self.history):
            snap = self.history[self.current_step]
            self.current_step += 1
            if self.current_step == len(self.history):
                self.app_mode = AppMode.FINISHED
            return snap
        else:
            self.running = False
            self.app_mode = AppMode.FINISHED
            operation_logger.info("BFS simulation completed all steps.")
            return None

    def is_accepted(self):
        """ Check if the BFS simulation ended in an accepting state. """
        if not self.history:
            return False
        last_snap = self.history[-1]
        last_state = last_snap[0]
        if last_state in self.manager.automata.accept_states:
            # check if all tapes are fully read
            for i, pos in enumerate(last_snap[1:]):
                tape = self.manager.tapes[i]
                if pos < len(tape.symbols):
                    return False
            return True
        return False

    def resume(self):
        """ Resume the BFS simulation. """
        self.running = False
        self.app_mode = AppMode.RUNNING
        if self.updated_during_run:
            self.simulate_from_updated_history()
        operation_logger.info("BFS simulation resumed.")

    def restart(self):
        """ Restart the BFS simulation. """
        self.history.clear()
        self.current_step = 0
        self.running = False
        self.updated_during_run = False
        self.updated_transitions = False
        self.app_mode = AppMode.DRAWING
        for tr in self.automata_manager.transitions:
            if self.canvas:
                tr.set_color(self.canvas, COLOR_BLACK)
            tr.requires_update = False
        operation_logger.info("BFS simulation restarted.")

    def clear_all(self):
        """ Clear all data from the simulation. """
        self.words.clear()
        self.automata_manager.states.clear()
        self.automata_manager.transitions.clear()
        self.automata_manager.word_count = 1
        self.history.clear()
        self.current_step = 0
        self.running = False
        self.updated_during_run = False
        self.app_mode = AppMode.DRAWING
        operation_logger.info("All simulation data cleared.")

    def update_transitions_in_backend(self):
        """ Update transitions in the backend Automata based on GUI transitions. """
        if not self.manager or not self.manager.automata:
            return
        self.manager.automata.transitions.clear()
        self.history_backup = self.history[:self.current_step]

        for gui_tr in self.automata_manager.transitions:
            source = gui_tr.source.name
            target = gui_tr.target.name
            for vec in gui_tr.transition_vectors:
                sym_vec = SymbolVector(list(vec))
                for c in vec:
                    self.manager.automata.alphabet.add(c)
                b_tr = Transition(fromState=source, symbols_vector=sym_vec, targetState=target)
                self.manager.automata.add_transition(b_tr)

        operation_logger.info("Backend transitions updated from GUI.")

        self.simulate_from_updated_history()

    def save_current_run(self, description=""):
        """ Save the current run history to the database. Serialize the run. """
        try:
            st_list = []
            for s in self.automata_manager.states:
                st_list.append({
                    'name': s.name,
                    'x': s.x,
                    'y': s.y,
                    'is_start': s.is_start,
                    'is_accept': s.is_accept
                })
            tr_list = []
            for tr in self.automata_manager.transitions:
                tr_list.append({
                    'source': tr.source.name,
                    'target': tr.target.name,
                    'vectors': tr.transition_vectors
                })

            manager_data = serialize_manager(self.manager)

            automata_data = {
                'states': st_list,
                'transitions': tr_list,
                'word_count': self.automata_manager.word_count,
                'words': self.words,
                'current_step': self.current_step,
                'app_mode': self.app_mode.value,
                'manager': manager_data
            }

            history_data = self.history

            self.db_manager.save_run_history(
                username=self.current_user,
                automata_data=automata_data,
                history_data=history_data,
                description=description
            )
            operation_logger.info(f"Run history saved. Description: {description}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save run history: {e}")
            error_logger.error(f"Exception saving run: {e}")

    def load_run(self, automata_data, history_data):
        """ Load a run history from the database. Unserializing the data"""
        try:
            self.words.clear()
            self.automata_manager.states.clear()
            self.automata_manager.transitions.clear()

            for st in automata_data.get('states', []):
                self.automata_manager.add_state(
                    name=st['name'],
                    x=st['x'],
                    y=st['y'],
                    is_start=st['is_start'],
                    is_accept=st['is_accept']
                )

            for tdata in automata_data.get('transitions', []):
                src, tgt = None, None
                for s in self.automata_manager.states:
                    if s.name == tdata['source']:
                        src = s
                    if s.name == tdata['target']:
                        tgt = s
                if src and tgt:
                    vectors_list = tdata.get('vectors', [])
                    self.automata_manager.add_transition(src, tgt, vectors_list)

            self.words = automata_data.get('words', [])
            wc = automata_data.get('word_count', 1)
            self.automata_manager.set_word_count(wc)

            self.history = history_data
            self.current_step = automata_data.get('current_step', 0)

            # restore app_mode
            mode_val = automata_data.get('app_mode', AppMode.DRAWING.value)
            self.app_mode = AppMode(mode_val) if mode_val in [m.value for m in AppMode] else AppMode.DRAWING

            loaded_automata = Automata()
            for st_obj in self.automata_manager.states:
                loaded_automata.add_state(st_obj.name, is_accept=st_obj.is_accept)
                if st_obj.is_start:
                    loaded_automata.set_start_state(st_obj.name)

            for gui_tr in self.automata_manager.transitions:
                source = gui_tr.source.name
                target = gui_tr.target.name
                for vec in gui_tr.transition_vectors:
                    sym_vec = SymbolVector(list(vec))
                    for c in vec:
                        loaded_automata.alphabet.add(c)
                    b_tr = Transition(fromState=source, symbols_vector=sym_vec, targetState=target)
                    loaded_automata.add_transition(b_tr)

            manager_data = automata_data.get('manager', None)
            if manager_data:
                self.manager = deserialize_manager(manager_data, loaded_automata)
            else:
                self.manager = None
                self.running = False

            # Reset transitions color
            for tr in self.automata_manager.transitions:
                if self.canvas:
                    tr.set_color(self.canvas, COLOR_BLACK)
                tr.requires_update = False

            self.running = (self.app_mode == AppMode.RUNNING)
            operation_logger.info("Run history loaded successfully.")


        except Exception as e:
            messagebox.showerror("Error", f"Failed to load run history: {e}")
            error_logger.error(f"Error loading run: {e}")
