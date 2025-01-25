import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from components.utils.popup_helper import centered_popup
from components.utils.logger import error_logger
from components.utils.constants import (
    IMG_SIZE, HELP_WIDTH, HELP_HEIGHT, 
    SAVE_WIDTH, SAVE_HEIGHT, POP_WIDTH, POP_HEIGHT
)

class HelpButton(ttk.Button):
    """
        Help button with explanation about usage of the program.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, command=self._on_help, **kwargs)

    def _on_help(self):
        """ Open help window. """
        root = self.winfo_toplevel()
        show_help_window(
            parent_window=root,

        )


def show_help_window(parent_window):
    help_win = tk.Toplevel(parent_window)
    help_win.title("Help page")
    help_win.geometry(f"{HELP_WIDTH}x{HELP_HEIGHT}")
    centered_popup(parent_window, help_win)

    help_win.icon_cache = {}

    canvas = tk.Canvas(help_win, borderwidth=0, highlightthickness=0)
    scrollbar = ttk.Scrollbar(help_win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    content_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    content_frame.bind("<Configure>", on_frame_configure)

    ttk.Label(
        content_frame, 
        text="HyperAutomata Simulator User Help\nMade by Raz Kessel & Nevo Gottlieb",
        font=("Arial", 16, "bold")
    ).pack(pady=5)

    explanation = (
        """
        This Simulator allows you to design and simulate run on hyperautomata with any number of tapes.
        
        MAIN PARTS OF THE APPLICATION:
        1) Drawing Board (Canvas) - used to create automata, click with activated tool to add new element
        2) Tools Panel - all the available tools
        3) Run Tools Panel - run operation to utilize BFS and find accepting/rejecting run for current automata
        4) Words Window - window with clickable words to add/remove/change words
        5) Current Setup Frame - current run representation. Current position in word is colored in red, when ended read word - colors it green.

        TWO APPLICATION STAGES:
         - DRAWING: Add/edit states, transitions, or words.
         - RUNNING: utilize BFS to find accepting/rejecting run.

        HOW TO USE:
        1) Draw your automaton:
           - 'Add State' -> click canvas -> name your state.
           - 'Add Transition' -> click two states -> define conditions.
        2) Add words:
           - Use the Words Window to add input words.
           - If BFS was running, transitions become out-of-date.
        3) Press 'Run' or 'Step':
           - BFS processes each word. The Current Setup frame updates.
        4) Save/Load (Optional)
           - Save the current run with a name and description.
           - Load previously saved runs from the database.
        """
    )
    explanation_label = ttk.Label(
        content_frame,
        text=explanation,
        wraplength=850, 
        justify="left"
    )
    explanation_label.pack(padx=10, pady=(5, 10))

    icons_map = {
        "run":              __load_icon("assets/run.png"),
        "pause":            __load_icon("assets/pause.png"),
        "step":             __load_icon("assets/step.png"),
        "stop":             __load_icon("assets/stop.png"),
        "reload":           __load_icon("assets/reload.png"),
        "save":             __load_icon("assets/save.png"),
        "story":            __load_icon("assets/story.png"),
        "add_state":        __load_icon("assets/circle.png"),
        "add_transition":   __load_icon("assets/arrow.png"),
        "select":           __load_icon("assets/arrow_select.png"),
        "undo":             __load_icon("assets/arrow_back.png"),
        "redo":             __load_icon("assets/arrow_forward.png"),
        "zoom_in":          __load_icon("assets/zoom_in.png"),
        "zoom_out":         __load_icon("assets/zoom_out.png"),
    }

    # Save icons for further usage
    for key, val in icons_map.items():
        help_win.icon_cache[key] = val

    features = [
        ("Run",         "run",       
         "Starts simulation run.", 
         lambda: show_additional_info(help_win, "Run", "Utilizes BFS to find if accepting/rejecting words and step-by-step showing returned result.")),
        ("Pause",       "pause",     
         "Pauses a running simulation.", 
         lambda: show_additional_info(help_win, "Pause", "Pause the current run.")),
        ("Step",        "step",      
         "Advances simulation one step.", 
         lambda: show_additional_info(help_win, "Step", "Perform one step in current simulation.")),
        ("Stop",        "stop",      
         "Stops and resets all.", 
         lambda: show_additional_info(help_win, "Stop", "Stops current simulation, removing the history and returning to drawing stage.")),
        ("Reload",      "reload",    
         "Clears everything.", 
         lambda: show_additional_info(help_win, "Reload", "Completly resets the application, removing all words, transitions and states.")),
        ("Save",        "save",      
         "Saves current state of application to db.", 
         lambda: show_save_popup(help_win)),
        ("Load",        "story",     
         "Loads a saved state from database.", 
         lambda: show_load_popup(help_win)),
        ("Add State",   "add_state", 
         "Adds new state.", 
         lambda: show_add_state_popup(help_win)),
        ("Add Transition","add_transition", 
         "Adds new transition.", 
         lambda: show_add_transition_popup(help_win)),
        ("Selection Tool","select",  
         "Selects/edits states or transitions.", 
         lambda: show_additional_info(help_win, "Selection Tool", 
                "Left-click state/transition to edit it, will open separate window. Right-click+drag state to move.")),
        ("Undo",        "undo",      
         "Undos the last action.", 
         lambda: show_additional_info(help_win, "Undo", "Revert the most recent change.")),
        ("Redo",        "redo",      
         "Re-applys the last undone action.", 
         lambda: show_additional_info(help_win, "Redo", "Re-apply the last undone action.")),
        ("Zoom In",     "zoom_in",   
         "Enlarges the canvas view.", 
         lambda: show_additional_info(help_win, "Zoom In", "Increase canvas scale for closer view.")),
        ("Zoom Out",    "zoom_out",  
         "Shrinks the canvas view.", 
         lambda: show_additional_info(help_win, "Zoom Out", "Decrease canvas scale for a broader view.")),
        ("Add Word",    None,        
         "Adds new word to simulation.", 
         lambda: show_add_word_popup(help_win)),
    ]

    for (title, icon_key, short_desc, popup_callback) in features:
        row_fr = ttk.Frame(content_frame)
        row_fr.pack(anchor="w", fill=tk.X, pady=3)

        icon_img = help_win.icon_cache.get(icon_key, None) if icon_key else None
        if icon_img:
            ttk.Label(row_fr, image=icon_img).pack(side=tk.LEFT, padx=5)
        else:
            ttk.Label(row_fr, text="").pack(side=tk.LEFT, padx=5)

        text_str = f"{title} - {short_desc}"
        lbl = ttk.Label(row_fr, text=text_str, wraplength=700, justify="left")
        lbl.pack(side=tk.LEFT, padx=5)

        # Open additional explanation
        ttk.Button(row_fr, text="?", width=2, command=popup_callback).pack(side=tk.LEFT, padx=5)

    usage_info = (
        "Click the '?' button next to each tool to see more details.\n"
        "Enjoy your Automata building!"
    )
    ttk.Label(content_frame, text=usage_info, foreground="gray").pack(pady=5)
    
    def bind_mousewheel_recursive(widget):
        """ Recursively bind MouseWheel events on widget and all children. """
        widget.bind("<MouseWheel>", lambda e: _on_mousewheel(canvas, e), add="+")
        widget.bind("<Button-4>", lambda e: _on_mousewheel(canvas, e), add="+")
        widget.bind("<Button-5>", lambda e: _on_mousewheel(canvas, e), add="+") 
        for child in widget.winfo_children():
            bind_mousewheel_recursive(child)

    bind_mousewheel_recursive(help_win)


def __load_icon(path):
    """ Load and resize an icon image, returning PhotoImage or None on error. """
    try:
        img = Image.open(path)
        img = img.resize(IMG_SIZE)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        error_logger.error(f"Failed to load icon {path}: {e}")
        return None


def _on_mousewheel(canvas, event):
    if event.num == 4 or event.delta > 0:
        direction = -1
    elif event.num == 5 or event.delta < 0:
        direction = 1
    else:
        direction = -1 if event.delta > 0 else 1
    canvas.yview_scroll(direction, "units")


def show_additional_info(parent, title, description):
    """ Generic popup with additional explanation about tool. """
    sub = tk.Toplevel(parent)
    sub.title(f"Help: {title}")
    sub.geometry(f"{POP_WIDTH}x{POP_HEIGHT}")
    centered_popup(parent, sub)

    ttk.Label(sub, text=title, font=("Arial", 12, "bold")).pack(pady=5)
    ttk.Label(sub, text=description, wraplength=POP_WIDTH-20 , justify="left").pack(padx=10, pady=5)


def show_save_popup(parent):
    """ 'Save Run' window. """
    sub = tk.Toplevel(parent)
    sub.title("Save Window")
    sub.geometry(f"{SAVE_WIDTH}x{SAVE_HEIGHT}")
    centered_popup(parent, sub)

    msg = "Window to save the run. Enter a name for the save, optional description and the OK to save."
    ttk.Label(sub, text=msg, wraplength=SAVE_WIDTH-20, justify="left").pack(pady=5)

    ttk.Label(sub, text="Run Name:", font=("Arial", 10)).pack(pady=3)
    ent_name = ttk.Entry(sub, justify="center")
    ent_name.insert(0, "MyAutomata")
    ent_name.pack(pady=3)

    ttk.Label(sub, text="Description (optional):").pack()
    desc_txt = tk.Text(sub, width=30, height=4)
    desc_txt.pack(pady=5)

    bf = ttk.Frame(sub)
    bf.pack(pady=5)
    ttk.Button(bf, text="OK").pack(side=tk.LEFT, padx=5)
    ttk.Button(bf, text="Cancel").pack(side=tk.LEFT, padx=5)


def show_load_popup(parent):
    """  'Load Run' window. """
    sub = tk.Toplevel(parent)
    sub.title("Load Window")
    sub.geometry(f"{SAVE_WIDTH}x{SAVE_HEIGHT}")
    centered_popup(parent, sub)

    msg = "List of all saved runs, choose save and then double click to load it."
    ttk.Label(sub, text=msg, wraplength=460, justify="left").pack(pady=5)

    ttk.Label(sub, text="Select a snapshot:", font=("Arial", 10)).pack()
    lb = tk.Listbox(sub, width=40, height=6)
    lb.pack(pady=5)
    lb.insert(tk.END, "ID=1: MyAutomata1 ...")
    lb.insert(tk.END, "ID=2: MyAutomata2 ...")

    ttk.Label(sub, text="(Double-click to load)", foreground="gray").pack(pady=5)


def show_add_state_popup(parent):
    """ 'Add State' window. """
    sub = tk.Toplevel(parent)
    sub.title("Add State ")
    sub.geometry(f"{POP_WIDTH}x{POP_HEIGHT}")
    centered_popup(parent, sub)

    msg = "When using 'Add State' and clicking on canvas, opens the window to create new state, if clicked on existing state will open edit window"
    ttk.Label(sub, text=msg, wraplength=380).pack(pady=5)

    ttk.Label(sub, text="Name:", font=("Arial", 10)).pack(pady=2)
    e_name = ttk.Entry(sub, justify='center')
    e_name.insert(0, "q0")
    e_name.pack(pady=2)

    v_start = tk.BooleanVar(value=False)
    v_accept = tk.BooleanVar(value=False)
    ttk.Checkbutton(sub, text="Start", variable=v_start).pack(pady=2)
    ttk.Checkbutton(sub, text="Accept", variable=v_accept).pack(pady=2)

    bf = ttk.Frame(sub)
    bf.pack(pady=5)
    ttk.Button(bf, text="Save").pack(side=tk.LEFT, padx=5)
    ttk.Button(bf, text="Delete", style="Danger.TButton").pack(side=tk.LEFT, padx=5)


def show_add_transition_popup(parent):
    """ 'Add Transition' window. """
    sub = tk.Toplevel(parent)
    sub.title("Add Transition")
    sub.geometry(f"{POP_WIDTH}x{POP_HEIGHT}")
    centered_popup(parent, sub)

    msg = "After clicking on two states, for transition creation will open add window, if transition exists will open edit window."
    ttk.Label(sub, text=msg, wraplength=POP_WIDTH-20, justify="left").pack(pady=5)

    ttk.Label(sub, text="Transition Condition(s):", font=("Arial", 10, "bold")).pack(pady=3)
    fr = ttk.Frame(sub)
    fr.pack(pady=5)

    e1 = ttk.Entry(fr, width=6, justify='center')
    e1.insert(0, "a")
    e1.grid(row=0, column=0, padx=3)

    btn_remove = ttk.Button(fr, text="X", style="Danger.TButton")
    btn_remove.grid(row=0, column=1, padx=3)

    ttk.Button(sub, text="Add Condition").pack(pady=5)

    bf = ttk.Frame(sub)
    bf.pack(pady=5)
    ttk.Button(bf, text="Save").pack(side=tk.LEFT, padx=5)
    ttk.Button(bf, text="Delete", style="Danger.TButton").pack(side=tk.LEFT, padx=5)


def show_add_word_popup(parent):
    """ 'Add Word' window. """
    sub = tk.Toplevel(parent)
    sub.title("Add Word")
    sub.geometry(f"{POP_WIDTH}x{POP_HEIGHT}")
    centered_popup(parent, sub)

    msg = "When you click 'Add Word' in the Words Window, this popup appears to type a new input. After adding the word will update word_count variable, and update transitions(if new value higher then previous)"
    ttk.Label(sub, text=msg, wraplength=380).pack(pady=5)

    ttk.Label(sub, text="Enter a new word:").pack()
    ent_word = ttk.Entry(sub, justify='center')
    ent_word.pack(pady=3)

    bf = ttk.Frame(sub)
    bf.pack(pady=5)
    ttk.Button(bf, text="Add").pack(side=tk.LEFT, padx=5)
    ttk.Button(bf, text="Cancel").pack(side=tk.LEFT, padx=5)
