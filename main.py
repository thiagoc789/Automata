import tkinter as tk

class Automaton:
    def __init__(self, num_cells, transition_rule):
        # Initialize the cells and their states
        self.num_cells = num_cells
        self.transition_rule = transition_rule
        self.cells = [0] * num_cells
        self.history = []
        self.buttons = []

    def update_cells(self):
        # Update the states of the cells based on the transition rule
        new_states = [0] * self.num_cells
        for i in range(self.num_cells):
            # Get the states of the current cell and its neighbors
            left_state = self.cells[i-1] if i > 0 else 0
            right_state = self.cells[i+1] if i < self.num_cells-1 else 0
            current_state = self.cells[i]
            # Use the transition rule to determine the new state of the cell
            new_state = self.transition_rule(left_state, current_state, right_state)
            new_states[i] = new_state
        self.history.append(self.cells)
        self.cells = new_states
        self.update_buttons()

    def update_buttons(self):
        # Update the colors of the buttons based on the states of the cells
        for i in range(self.num_cells):
            if self.cells[i] == 0:
                color = "white"
            else:
                color = "black"
            self.buttons[i].config(bg=color)

def main():
    # Define the transition rules
    def game_of_life(left_state, current_state, right_state):
        # Conway's Game of Life rule
        num_live_neighbors = left_state + right_state
        if current_state == 1:
            if num_live_neighbors == 2 or num_live_neighbors == 3:
                return 1
            else:
                return 0
        else:
            if num_live_neighbors == 3:
                return 1
            else:
                return 0

    def rule_30(left_state, current_state, right_state):
        # Rule 30 rule
        num_live_neighbors = left_state + right_state
        if current_state == 1:
            if num_live_neighbors % 2 == 1:
                return 1
            else:
                return 0
        else:
            if num_live_neighbors % 2 == 1:
                return 1
            else:
                return 0

    def rule_90(left_state, current_state, right_state):
    # Rule 90 rule
        if left_state == 1:
            return 1
        else:
            return 0

    # Create the window and the automaton
    window = tk.Tk()
    global automaton
    automaton = Automaton(100, game_of_life)
# Create a frame for the controls
    controls_frame = tk.Frame(window)
    controls_frame.pack(side="top")

    # Create a label for the dropdown menu
    label = tk.Label(controls_frame, text="Transition rule:")
    label.pack(side="left")

    # Create a dropdown menu for selecting the transition rule
    transition_rule_var = tk.StringVar(controls_frame)
    transition_rule_var.set("Game of Life") # default value
    menu = tk.OptionMenu(controls_frame, transition_rule_var, "Game of Life", "Rule 30", "Rule 90")
    menu.pack(side="left")

    # Update the automaton's transition function when the selection changes
    def update_transition_rule(*args):
        selected_rule = transition_rule_var.get()
        if selected_rule == "Game of Life":
            automaton.transition_rule = game_of_life
        elif selected_rule == "Rule 30":
            automaton.transition_rule = rule_30
        elif selected_rule == "Rule 90":
            automaton.transition_rule = rule_90
    transition_rule_var.trace("w", update_transition_rule)

    # Create a button for stepping through the generations
    step_button = tk.Button(controls_frame, text="Step", command=automaton.update_cells)
    step_button.pack(side="left")

    # Create a frame for the cells
    cells_frame = tk.Frame(window)
    cells_frame.pack(side="top")

    # Create buttons for each cell
    for i in range(automaton.num_cells):
        def toggle_cell(i):
            # Change the state of the cell at index i
            if automaton.cells[i] == 0:
                automaton.cells[i] = 1
            else:
                automaton.cells[i] = 0
            # Update the button to reflect the new state of the cell
            if automaton.cells[i] == 0:
                color = "white"
            else:
                color = "black"
            automaton.buttons[i].config(bg=color)
        button = tk.Button(cells_frame, bg="white", command=lambda i=i: toggle_cell(i))
        button.pack(side="left")
        automaton.buttons.append(button)

    window.mainloop()
    
if __name__ == "__main__":
    main()
