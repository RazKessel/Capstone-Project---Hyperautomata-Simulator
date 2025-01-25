import tkinter as tk
import math
from components.utils.constants import COLOR_BLACK, PARALLEL_OFFSET
from components.utils.logger import operation_logger, error_logger

class Transition:
    """
        Represents a GUI transition from a source state to a target state,
        with one or more condition vectors.
        Handles drawing of arrows and labels.
    """

    def __init__(self, source, target, transition_vectors):
        self.source = source
        self.target = target
        self.transition_vectors = transition_vectors
        self.canvas_ids = []
        self.offset_index = 0
        
        self.color = COLOR_BLACK
        
        self.requires_update = False

        source.outgoing_transitions.append(self)
        target.incoming_transitions.append(self)
        operation_logger.info(f"Transition created: {source.name} -> {target.name}")
        
    def set_color(self, canvas, color=COLOR_BLACK):
        """ Updates color for arrows and self loops. """
        self.color = color
        for cid in self.canvas_ids:
            item_type = canvas.type(cid)
            if item_type in "line":
                canvas.itemconfig(cid, fill=color)
            elif item_type == "arc":
                canvas.itemconfig(cid, outline=color)
        operation_logger.info(f"Transition color set to {color}: {self.source.name} -> {self.target.name}")

    def get_color(self):
        return self.color
    
    def draw(self, canvas):
        """ Draw the transition on the canvas. """
        self.clear(canvas)
        if not canvas:
            return
        if self.source == self.target:
            self.draw_loop(canvas)
        else:
            self.draw_arrow(canvas)

    def redraw(self, canvas):
        """ Redraw the transition (useful after moving states) """
        self.draw(canvas)

    def draw_loop(self, canvas):
        """ Draw a loop transition for transitions from a state to itself. """
        r = self.source.radius
        cx = self.source.x
        cy = self.source.y - (r + 30)
        try:
            arc_id = canvas.create_arc(
                cx - r, cy - r,
                cx + r, cy + r,
                start=290, extent=320, style="arc",
                outline=self.get_color(), width=2
            )
            self.canvas_ids.append(arc_id)

            lbl = canvas.create_text(cx, cy - (r + 10), text=self.label_text())
            self.canvas_ids.append(lbl)
        except Exception as e:
            error_logger.error(f"Failed to draw loop transition: {e}")

    def draw_arrow(self, canvas):
        """
            Draw an arrow from the source state to the target state,
            handling parallel transitions by offsetting them.
        """
        sx, sy = self.source.x, self.source.y
        tx, ty = self.target.x, self.target.y
        dx, dy = (tx - sx), (ty - sy)
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        
        # Unit vector components
        ux, uy = dx / dist, dy / dist

        # Calculate offset for parallel transitions to handle q0-q1 q1-q0 transitions
        sign = -1 if self.offset_index % 2 == 0 else 1
        steps = (self.offset_index // 2) + 1
        offset = sign * steps * PARALLEL_OFFSET
        perp_x, perp_y = -uy, ux

        # Adjusted start and end points
        sx_e = sx + ux * self.source.radius + perp_x * offset
        sy_e = sy + uy * self.source.radius + perp_y * offset
        tx_e = tx - ux * self.target.radius + perp_x * offset
        ty_e = ty - uy * self.target.radius + perp_y * offset

        try:
            line_id = canvas.create_line(
                sx_e, sy_e, tx_e, ty_e,
                arrow=tk.LAST, fill=self.get_color(), width=2
            )
            self.canvas_ids.append(line_id)

            mx, my = (sx_e + tx_e) / 2, (sy_e + ty_e) / 2
            lbl_id = canvas.create_text(mx, my - 10, text=self.label_text())
            self.canvas_ids.append(lbl_id)
        except Exception as e:
            error_logger.error(f"Failed to draw transition arrow: {e}")

    def label_text(self):
        """ Generate the label text based on transition vectors. """
        parts = []
        for vec in self.transition_vectors:
            vs = ",".join(vec)
            parts.append("{" + vs + "}")
        return ", ".join(parts)

    def clear(self, canvas):
        """ Remove all canvas items associated with this transition. """
        try:
            for cid in self.canvas_ids:
                canvas.delete(cid)
            self.canvas_ids.clear()
        except Exception as e:
            error_logger.error(f"Failed to clear transition: {e}")


