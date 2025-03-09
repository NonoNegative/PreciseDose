import tkinter as tk

class ResuscitationGraph:
    def __init__(self, root):
        self.root = root
        self.root.title("Cardiac Arrest Resuscitation Flowchart")

        # Increased canvas size
        self.canvas = tk.Canvas(root, width=1600, height=1000, bg="white")
        self.canvas.pack()

        # Define graph structure
        self.node_width = 180
        self.node_height = 60
        self.graph = {
            "Start CPR": {"pos": (850, 50), "text": "Start CPR\nGive oxygen\nAttach monitor/defibrillator", "color": "lightblue", "next": [("Rhythm shockable?", "")]},
            "Rhythm shockable?": {"pos": (850, 150), "text": "Rhythm shockable?", "color": "#FF9999", "next": [("VF/VT", "Yes"), ("Asystole/PEA", "No")]},

            # VF/VT Path
            "VF/VT": {"pos": (600, 250), "text": "VF/VT\nGive shock", "color": "lightblue", "next": [("CPR 2 min (VF/VT)", "")]},
            "CPR 2 min (VF/VT)": {"pos": (600, 350), "text": "CPR 2 min (VF/VT)\nIO/IV access", "color": "lightblue", "next": [("Rhythm shockable? (VF)", "")]},
            "Rhythm shockable? (VF)": {"pos": (600, 450), "text": "Rhythm shockable?", "color": "#FF9999", "next": [("Shock (again)", "Yes"), ("CPR 2 min (Epinephrine)", "No")]},
            "Shock (again)": {"pos": (300, 520), "text": "Shock (again)\nGive shock", "color": "lightblue", "next": [("CPR 2 min (Epinephrine)", "")]},
            "CPR 2 min (Epinephrine)": {"pos": (600, 570), "text": "CPR 2 min\nEpinephrine (Every 3-5 min)\nConsider advanced airway", "color": "lightblue", "next": [("Rhythm shockable? (VF2)", "")]},
            "Rhythm shockable? (VF2)": {"pos": (600, 680), "text": "Rhythm shockable?", "color": "#FF9999", "next": [("Shock (third time)", "Yes"), ("CPR 2 min (Amiodarone)", "No")]},
            "Shock (third time)": {"pos": (850, 750), "text": "Shock (third time)\nGive shock", "color": "lightblue", "next": [("CPR 2 min (Amiodarone)", "")]},
            "CPR 2 min (Amiodarone)": {"pos": (600, 830), "text": "CPR 2 min (Amiodarone)\nAmiodarone\nTreat reversible causes", "color": "lightblue", "next": [("Rhythm shockable? (VF3)", "")]},
            "Rhythm shockable? (VF3)": {"pos": (400, 950), "text": "Rhythm shockable?", "color": "#FF9999", "next": [("Shock (again)", "Yes"), ("End", "No")]},

            # Asystole/PEA Path
            "Asystole/PEA": {"pos": (1100, 250), "text": "Asystole/PEA", "color": "lightblue", "next": [("CPR 2 min (PEA)", "")]},
            "CPR 2 min (PEA)": {"pos": (1100, 350), "text": "CPR 2 min (PEA)\nIO/IV access\nEpinephrine (Every 3-5 min)\nConsider advanced airway", "color": "lightblue", "next": [("Rhythm shockable? (PEA)", "")]},
            "Rhythm shockable? (PEA)": {"pos": (1100, 450), "text": "Rhythm shockable?", "color": "#FF9999", "next": [("VF/VT", "Yes"), ("CPR 2 min (Reversible Causes)", "No")]},
            "CPR 2 min (Reversible Causes)": {"pos": (1100, 600), "text": "CPR 2 min (Reversible Causes)\nTreat reversible causes", "color": "lightblue", "next": [("Rhythm shockable? (PEA2)", "")]},
            "Rhythm shockable? (PEA2)": {"pos": (1100, 800), "text": "Rhythm shockable?", "color": "#FF9999", "next": [("VF/VT", "Yes"), ("End", "No")]},

            # End
            "End": {"pos": (850, 950), "text": "End\nCheck pulse\nPost-cardiac arrest care", "color": "lightblue", "next": []}
        }

        self.draw_graph()

    def draw_graph(self):
        """ Draws the nodes and edges on the canvas """
        # Draw edges first so they appear below nodes
        for node, data in self.graph.items():
            for next_node, decision_text in data["next"]:
                self.draw_edge(data["pos"], self.graph[next_node]["pos"], decision_text)

        # Draw nodes on top
        for node, data in self.graph.items():
            self.draw_node(data["text"], data["pos"], data["color"])

    def draw_node(self, text, position, color):
        """ Draws a rectangular node with text inside """
        x, y = position
        width, height = self.node_width, self.node_height

        # Draw rectangle with specified color
        self.canvas.create_rectangle(x - width//2, y - height//2, x + width//2, y + height//2, fill=color, outline="black")

        # Draw node text
        self.canvas.create_text(x, y, text=text, font=("Arial", 8, "bold"), width=width-10)

    def draw_edge(self, start, end, decision_text):
        """ Draws a directed arrow from one node to another, ensuring it starts and ends outside the rectangles """
        x1, y1 = start
        x2, y2 = end
        dx, dy = x2 - x1, y2 - y1

        # Calculate unit vector for the direction of the arrow
        length = (dx**2 + dy**2) ** 0.5
        if length == 0:
            return  # Avoid division by zero if two nodes are at the same location

        ux, uy = dx / length, dy / length  # Unit vector components

        # Adjust start and end points to be just outside the rectangles
        start_x = x1 + ux * (self.node_width//2 + 5)
        start_y = y1 + uy * (self.node_height//2 + 5)
        end_x = x2 - ux * (self.node_width//2 + 5)
        end_y = y2 - uy * (self.node_height//2 + 5)

        # Draw the arrow with corrected positions
        self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, width=2)

        # Draw decision text in a light grey background circle
        if decision_text:
            circle_x = (start_x + end_x) / 2
            circle_y = (start_y + end_y) / 2

            radius = 12
            self.canvas.create_oval(circle_x - radius, circle_y - radius, circle_x + radius, circle_y + radius, fill="lightgrey", outline="black")
            self.canvas.create_text(circle_x, circle_y, text=decision_text, font=("Arial", 8, "bold"))

# Run the Tkinter app
root = tk.Tk()
root.geometry("1600x1000")  # Bigger window
app = ResuscitationGraph(root)
root.mainloop()
