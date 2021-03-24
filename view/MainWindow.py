# https://jakirkpatrick.wordpress.com/2012/02/01/making-a-hovering-box-in-tkinter/
# https://codeloop.org/how-to-create-textbox-in-python-tkinter/

import random
import tkinter as tk
from threading import Thread
from tkinter import ttk
from view.SimulatorWindow import SimulatorWindow


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        x = self.winfo_screenwidth() / 3.25  # width of the screen / 3.25
        y = self.winfo_screenheight() / 4  # height of the screen / 4
        self.geometry('%dx%d+%d+%d' % (720, 480, x, y))
        self.title("Learning Simulation Initialisation")
        self.simulators = []

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1, uniform="factors")
        container.grid_columnconfigure(0, weight=1, uniform="factors")
        container.grid_columnconfigure(1, weight=1, uniform="factors")

        neural_network_factors = tk.Frame(container)
        neural_network_factors.config(bg="white")
        neural_network_factors.grid(row=0, column=0, sticky="nsew")
        neural_network_factors.grid_columnconfigure(0, weight=1)
        neural_network_factors.grid_columnconfigure(3, weight=1)

        aged_brain_factors = tk.Frame(container)
        aged_brain_factors.config(bg="black")
        aged_brain_factors.grid(row=0, column=1, sticky="nsew")
        aged_brain_factors.grid_columnconfigure(0, weight=1)
        aged_brain_factors.grid_columnconfigure(3, weight=1)

        window_toolbar = tk.Frame(self)
        window_toolbar.pack(side="bottom", fill="both")

        generate_model_btn = tk.Button(window_toolbar, text="Generate Aged Model", command=self.generateAgedModel)
        generate_model_btn.pack(side="right")
        generate_model_btn = tk.Button(window_toolbar, text="Generate Young Model", command=self.generateYoungModel)
        generate_model_btn.pack(side="right")

        exit_button = tk.Button(window_toolbar, text="Exit", command=self.exitCommand)
        exit_button.pack(side="left")

        self.neural_network_factors_title = tk.Label(neural_network_factors, text="Neuron Network Factors")
        self.neural_network_factors_title.grid(column=1, row=0, columnspan=2)

        self.no_input_neu = tk.IntVar(value=10)
        self.makeLabelAndEntry(neural_network_factors, "Number of Input Neurons", self.no_input_neu, 1, 1)

        self.no_output_neu = tk.IntVar(value=10)
        self.makeLabelAndEntry(neural_network_factors, "Number of Output Neurons", self.no_output_neu, 1, 2)

        self.neu_input_curr = tk.IntVar(value=4)
        self.makeLabelAndEntry(neural_network_factors, "Neuron Input Current (A)", self.neu_input_curr, 1, 3)

        self.neu_input_intervals = tk.IntVar(value=5)
        self.makeLabelAndEntry(neural_network_factors, "Input Intervals (ms)", self.neu_input_intervals, 1, 4)

        self.sim_end_time = tk.IntVar(value=500)
        self.makeLabelAndEntry(neural_network_factors, "Simulation End Time (ms)", self.sim_end_time, 1, 5)

        self.mem_capacity = tk.IntVar(value=100)
        self.makeLabelAndEntry(neural_network_factors, "Memory Capacity (%)", self.mem_capacity, 1, 6)

        self.aged_brain_factors_title = tk.Label(aged_brain_factors, text="Aged Brain Factors")
        self.aged_brain_factors_title.grid(column=1, row=0, columnspan=2)

        self.dec_synaptic_str = tk.IntVar()
        self.makeLabelAndCheckbutton(aged_brain_factors, "Decrease Synaptic Strength", self.dec_synaptic_str, 1, 1)

        self.inc_neurodegen = tk.IntVar()
        self.makeLabelAndCheckbutton(aged_brain_factors, "Increased Neurodegeneration", self.inc_neurodegen, 1, 2)

        self.inhibited_LTP = tk.IntVar()
        self.makeLabelAndCheckbutton(aged_brain_factors, "Inhibited LTP", self.inhibited_LTP, 1, 3)

    def makeLabelAndEntry(self, master, text, text_variable, column, row):
        tk.Label(master, text=text).grid(column=column, row=row)
        tk.Entry(master, textvariable=text_variable).grid(column=(column + 1), row=row)

    def makeLabelAndCheckbutton(self, master, text, variable, column, row):
        tk.Label(master, text=text).grid(column=column, row=row)
        tk.Checkbutton(master, variable=variable).grid(column=(column + 1), row=row)

    def generateYoungModel(self):
        self.toggleSimulations(None)
        young_brain = SimulatorWindow(self.sim_end_time.get(), 0, self.no_input_neu.get(),
                                      self.no_output_neu.get(), self.mem_capacity.get(), 0,
                                      0, self.neu_input_intervals.get(), self.neu_input_curr.get(), "Young Brain",
                                      toggleSimulations=self.toggleSimulations)
        self.simulators.append(young_brain)
        young_brain.mainloop()

    def generateAgedModel(self):
        self.toggleSimulations(None)
        aged_brain = SimulatorWindow(self.sim_end_time.get(), self.inhibited_LTP.get(), self.no_input_neu.get(),
                                     self.no_output_neu.get(), self.mem_capacity.get(), self.dec_synaptic_str.get(),
                                     self.inc_neurodegen.get(), self.neu_input_intervals.get(),
                                     self.neu_input_curr.get(), "Aged Brain", toggleSimulations=self.toggleSimulations)
        self.simulators.append(aged_brain)
        aged_brain.mainloop()

    def toggleSimulations(self, target_simulator):
        simulators = self.simulators
        for simulator in simulators:
            if (simulator is not target_simulator) and simulator.brain_frame.brain.running:
                simulator.brain_frame.toggleRunSimulation()
        if target_simulator is not None:
            target_simulator.brain_frame.toggleRunSimulation()

    def exitCommand(self):
        self.destroy()

# if __name__ == "__main__":
#     app = InitialisationWindow()
#     app.mainloop()
