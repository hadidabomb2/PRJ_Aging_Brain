# https://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
# https://stackoverflow.com/questions/4781184/tkinter-displaying-a-square-grid
# https://stackoverflow.com/questions/40843039/how-to-write-a-simple-callback-function

import tkinter as tk

from view.BrainFrame import BrainFrame


class SimulatorWindow(tk.Tk):
    def __init__(self, end_time, learning_type_boolean, input_neu_size, output_neu_size, mem_capacity,
                 dec_synaptic_strength, inc_neurodegen, neu_input_intervals, neu_input_curr, title,
                 toggleSimulations, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("720x720")
        self.title("Learning Simulator: " + title)

        brain_args = []

        # End time
        brain_args.append(end_time)

        # Learning types
        if learning_type_boolean == 0:
            brain_args.append('LTP')
        else:
            brain_args.append('MIS')

        # Number of input and output neurons
        neu_dec_factor = 0.8
        if inc_neurodegen == 0:
            brain_args.append(int(input_neu_size))
            brain_args.append(int(output_neu_size))
        else:
            brain_args.append(int(input_neu_size * neu_dec_factor))
            brain_args.append(int(output_neu_size * neu_dec_factor))

        # Memory Capacity
        brain_args.append(mem_capacity / 100)

        # Synaptic Strength
        synaptic_strength = 6
        synaptic_strength_dec_factor = 0.6
        if dec_synaptic_strength == 0:
            brain_args.append(synaptic_strength)
        else:
            brain_args.append(synaptic_strength * synaptic_strength_dec_factor)

        # Neuron input current and intervals
        brain_args.append(neu_input_intervals)
        brain_args.append(neu_input_curr)

        window_toolbar = tk.Frame(self)
        window_toolbar.pack(side="bottom", fill="both")
        exit_button = tk.Button(window_toolbar, text="Exit", command=self.exitCommand)
        exit_button.pack(side="left")
        self.brain_frame = BrainFrame(brain_args, lambda: toggleSimulations(self), self)

    def exitCommand(self):
        self.destroy()

# if __name__ == "__main__":
#     app = SimulatorWindow()
#     app.mainloop()
