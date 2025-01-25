import tkinter as tk
from tkinter import ttk
from components.utils.constants import COLOR_PU_BG

class Tooltip:
    """
    Creates a tooltip for a given widget as the mouse enters.
    Modified so it does not intercept clicks and stays within main window.
    """

    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tooltip_active = False
        self.tooltip_label = None

        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<Motion>", self.move_tooltip)

    def show_tooltip(self, event=None):
        """ Show the tooltip as a label placed over the parent container. """
        if self.tooltip_active or not self.text:
            return

        parent = self.widget.master.master
        self.tooltip_label = ttk.Label(
            parent,
            text=self.text,
            background=COLOR_PU_BG,
            relief='solid',
            borderwidth=1,
            font=("Arial", 10, "normal")
        )

        self.tooltip_label.bind("<Button-1>", lambda e: self.widget.event_generate("<Button-1>"))

        x = event.x_root - parent.winfo_rootx() + 10
        y = event.y_root - parent.winfo_rooty() + 10
        self.tooltip_label.place(x=x, y=y)
        self.tooltip_active = True
        
    def move_tooltip(self, event=None):
        """ Move tooltip along with mouse, if active, and clamp inside main window. """
        if self.tooltip_label and self.tooltip_active:
            parent = self.widget.master.master
            top_level = parent.winfo_toplevel()

            x = event.x_root - parent.winfo_rootx() + 10
            y = event.y_root - parent.winfo_rooty() + 10

            tw = self.tooltip_label.winfo_reqwidth()
            th = self.tooltip_label.winfo_reqheight()

            max_x = top_level.winfo_width() - tw - 5
            max_y = top_level.winfo_height() - th - 5

            if x < 0:
                x = 0
            elif x > max_x:
                x = max_x
            if y < 0:
                y = 0
            elif y > max_y:
                y = max_y

            self.tooltip_label.place(x=x, y=y)

    def hide_tooltip(self, event=None):
        """ Hide and remove the tooltip label. """
        if self.tooltip_active and self.tooltip_label:
            self.tooltip_label.destroy()
            self.tooltip_label = None
        self.tooltip_active = False
