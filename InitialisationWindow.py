# https://jakirkpatrick.wordpress.com/2012/02/01/making-a-hovering-box-in-tkinter/
# https://codeloop.org/how-to-create-textbox-in-python-tkinter/

import random
import tkinter as tk
from tkinter import ttk
from SimulatorWindow import SimulatorApp


class InitialisationApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1080x720")
        container = ttk.Frame(self)
        neural_network_factors = tk.Frame(container)
        aged_brain_factors = tk.Frame(container)
        neural_network_factors.config(bg="white")
        aged_brain_factors.config(bg="black")

        generate_model_btn = tk.Button(container, text="Generate Model", command=self.generateModel)
        container.pack(fill="both", expand=True)
        generate_model_btn.pack(side="bottom")
        neural_network_factors.pack(side="left", fill="both", expand=True)
        aged_brain_factors.pack(side="right", fill="both", expand=True)

        self.neural_network_factors_title = tk.Label(neural_network_factors, text="Neuron Network Factors")
        self.neural_network_factors_title.grid(column=0, row=0, columnspan=2)
        # self.nnf_title.bind("<Enter>", self.nnfTitleOnEnter)
        # self.nnf_title.bind("<Leave>", self.nnfTitleOnLeave)

        no_input_neu_label = tk.Label(neural_network_factors, text="Number of Input Neurons").grid(column=0, row=1)
        self.no_input_neu = tk.IntVar(value=10)
        no_input_neu_input = tk.Entry(neural_network_factors, width="15", textvariable=self.no_input_neu).grid(column=1,
                                                                                                               row=1)

        no_output_neu_label = tk.Label(neural_network_factors, text="Number of Output Neurons").grid(column=0, row=2)
        self.no_output_neu = tk.IntVar(value=10)
        no_output_neu_input = tk.Entry(neural_network_factors, width="15", textvariable=self.no_output_neu).grid(
            column=1,
            row=2)

        neu_input_curr_label = tk.Label(neural_network_factors, text="Neuron Input Current (A)").grid(column=0, row=3)
        self.neu_input_curr = tk.IntVar(value=5)
        neu_input_curr_input = tk.Entry(neural_network_factors, width="15", textvariable=self.neu_input_curr).grid(
            column=1,
            row=3)

        neu_input_intervals_label = tk.Label(neural_network_factors, text="Input Intervals (ms)").grid(column=0, row=4)
        self.neu_input_intervals = tk.IntVar(value=500)
        neu_input_intervals_input = tk.Entry(neural_network_factors, width="15",
                                             textvariable=self.neu_input_intervals).grid(column=1, row=4)

        sim_end_time_label = tk.Label(neural_network_factors, text="Simulation End Time (s)").grid(column=0, row=5)
        self.sim_end_time = tk.IntVar(value=30)
        sim_end_time_input = tk.Entry(neural_network_factors, width="15",
                                      textvariable=self.sim_end_time).grid(column=1, row=5)

        mem_capacity_label = tk.Label(neural_network_factors, text="Memory Capacity (%)").grid(column=0, row=6)
        self.mem_capacity = tk.IntVar(value=80)
        mem_capacity_input = tk.Entry(neural_network_factors, width="15", textvariable=self.mem_capacity).grid(column=1,
                                                                                                           row=6)

        self.aged_brain_factors_title = tk.Label(aged_brain_factors, text="Aged Brain Factors")
        self.aged_brain_factors_title.grid(column=0, row=0, columnspan=2)

        dec_synaptic_str_label = tk.Label(aged_brain_factors, text="Decrease Synaptic Strength").grid(column=0, row=1)
        self.dec_synaptic_str = tk.IntVar()
        dec_synaptic_str_input = tk.Checkbutton(aged_brain_factors, variable=self.dec_synaptic_str).grid(column=1,
                                                                                                         row=1)

        inc_neurodegen_label = tk.Label(aged_brain_factors, text="Increased Neurodegeneration").grid(column=0, row=2)
        self.inc_neurodegen = tk.IntVar()
        inc_neurodegen_input = tk.Checkbutton(aged_brain_factors, variable=self.inc_neurodegen).grid(column=1, row=2)

        inhibited_LTP_label = tk.Label(aged_brain_factors, text="Inhibited LTP").grid(column=0, row=3)
        self.inhibited_LTP = tk.IntVar()
        inhibited_LTP_input = tk.Checkbutton(aged_brain_factors, variable=self.inhibited_LTP).grid(column=1, row=3)

    # def nnfTitleOnEnter(self, event):
    #     self.nnf_title.configure(text="Hello world")
    #
    # def nnfTitleOnLeave(self, enter):
    #     self.nnf_title.configure(text="")

    def generateModel(self):
        SimulatorApp(self.sim_end_time.get(), self.inhibited_LTP.get(), self.no_input_neu.get(),
                     self.no_output_neu.get(), self.mem_capacity.get(), self.dec_synaptic_str.get(),
                     self.inc_neurodegen.get(), self.neu_input_intervals.get(), self.neu_input_curr.get())
        self.destroy()


if __name__ == "__main__":
    app = InitialisationApp()
    app.mainloop()
