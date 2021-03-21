# https://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
# https://stackoverflow.com/questions/4781184/tkinter-displaying-a-square-grid
# https://stackoverflow.com/questions/40843039/how-to-write-a-simple-callback-function

import tkinter as tk

from view.BrainFrame import BrainFrame


class SimulatorWindow(tk.Tk):
    def __init__(self, end_time, learning_type_boolean, input_neu_size, output_neu_size, mem_capacity,
                 dec_synaptic_strength, inc_neurodegen, neu_input_intervals, neu_input_curr, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        normal_brain_args = []
        aged_brain_args = []
        # End time
        normal_brain_args.append(end_time)
        aged_brain_args.append(end_time)
        # Learning types
        normal_brain_args.append('LTP')
        if learning_type_boolean == 0:
            aged_brain_args.append('LTP')
        else:
            aged_brain_args.append('MIS')
        # Number of input and output neurons
        normal_brain_args.append(input_neu_size)
        normal_brain_args.append(output_neu_size)
        neu_dec_factor = 0.8
        if inc_neurodegen == 0:
            aged_brain_args.append(int(input_neu_size))
            aged_brain_args.append(int(output_neu_size))
        else:
            aged_brain_args.append(int(input_neu_size * neu_dec_factor))
            aged_brain_args.append(int(output_neu_size * neu_dec_factor))
        # Memory Capacity
        normal_brain_args.append(mem_capacity / 100)
        aged_brain_args.append(mem_capacity / 100)
        # Synaptic Strength
        synaptic_strength = 6
        synaptic_strength_dec_factor = 0.6
        normal_brain_args.append(synaptic_strength)
        if dec_synaptic_strength == 0:
            aged_brain_args.append(synaptic_strength)
        else:
            aged_brain_args.append(synaptic_strength * synaptic_strength_dec_factor)
        # Neuron input current and intervals
        normal_brain_args.append(neu_input_intervals/1000)
        normal_brain_args.append(neu_input_curr)
        aged_brain_args.append(neu_input_intervals/1000)
        aged_brain_args.append(neu_input_curr)

        self.geometry("1080x720")

        normal_brain = BrainFrame(normal_brain_args, self)
        aged_brain = BrainFrame(aged_brain_args, self)

# if __name__ == "__main__":
#     app = SimulatorWindow()
#     app.mainloop()
