# https://jakirkpatrick.wordpress.com/2012/02/01/making-a-hovering-box-in-tkinter/
# https://codeloop.org/how-to-create-textbox-in-python-tkinter/

import tkinter as tk
from tkinter import ttk
from view.SimulatorWindow import SimulatorWindow


# The main window of the simulation. This window allows the user to edit the parameters of the model they want
# to generate, and also pick which type of brain to generate. The GUI is structured in a way that allows the user to
# create as many Simulator Windows as they desire so they can make visual comparisons.
class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # The styling of the ttk items in this class.
        s = ttk.Style(self)
        s.configure('Generate.TButton', font='helvetica 14', foreground='black', padding=[10, 10, 10, 5])
        s.configure('Generate2.TButton', font='helvetica 14', foreground='black', padding=[10, 10, 10, 5])
        s.configure('Exit.TButton', font='helvetica 14', foreground='red', padding=[5, 10, 5, 5])
        s.configure('Title.TLabel', font='helvetica 16', foreground='black', padding=[5, 15, 5, 10])
        s.configure('Parameters.TLabel', font='helvetica 12', foreground='black', padding=[5, 17, 5, 17])
        s.configure('Parameters.TEntry', font='helvetica 12', foreground='black', padding=[5, 7, 5, 7])

        width = 720
        height = 480
        # Centers the window
        x = (self.winfo_screenwidth() / 2) - (width / 2)
        y = (self.winfo_screenheight() / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (720, 480, x, y))

        # Set window title.
        self.title("Learning Simulation Initialisation")

        # Holds a list of simulators that are generated.
        self.simulators = []

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        # Uniformly spaces out the two factor frames that will fit this container.
        container.grid_rowconfigure(0, weight=1, uniform="factors")
        container.grid_columnconfigure(0, weight=1, uniform="factors")
        container.grid_columnconfigure(1, weight=1, uniform="factors")

        simulation_factors = ttk.Frame(container)
        simulation_factors.grid(row=0, column=0, sticky="nsew")
        # Evens out any empty space either side of each column.
        simulation_factors.grid_columnconfigure(0, weight=1)
        simulation_factors.grid_columnconfigure(4, weight=1)

        aged_brain_factors = ttk.Frame(container)
        aged_brain_factors.grid(row=0, column=1, sticky="nsew")
        # Evens out any empty space either side of each column.
        aged_brain_factors.grid_columnconfigure(0, weight=1)
        aged_brain_factors.grid_columnconfigure(4, weight=1)

        # Create the window toolbar that will hold the exit button and the two generate model buttons.
        window_toolbar = ttk.Frame(self)
        window_toolbar.pack(side="bottom", fill="both")

        # Generate aged model button.
        generate_aged_model_btn = ttk.Button(window_toolbar, text="Generate Aged Model", style='Generate.TButton',
                                             command=self.generateAgedModel)
        generate_aged_model_btn.pack(side="right")
        # Generate young model button.
        generate_young_model_btn = ttk.Button(window_toolbar, text="Generate Young Model", style='Generate.TButton',
                                              command=self.generateYoungModel)
        generate_young_model_btn.pack(side="right")
        # Exit button.
        exit_button = ttk.Button(window_toolbar, text="Exit", style='Exit.TButton', command=self.exitCommand)
        exit_button.pack(side="left")

        # Simulation factors frame title - label.
        self.simulation_factors_title = ttk.Label(simulation_factors, style='Title.TLabel',
                                                  text="Simulation Factors")
        self.simulation_factors_title.grid(column=1, row=0, columnspan=3)

        # Number of input neurons - label and entry field.
        self.no_input_neu = tk.IntVar(value=10)
        self.makeLabelAndEntry(simulation_factors, "Number of Input Neurons", self.no_input_neu, 1, 1)

        # Number of output neurons - label and entry field.
        self.no_output_neu = tk.IntVar(value=10)
        self.makeLabelAndEntry(simulation_factors, "Number of Output Neurons", self.no_output_neu, 1, 2)

        # The strength of the input current being fed to an input neuron - label and entry field.
        self.neu_input_curr = tk.StringVar(value=4)
        self.makeLabelAndEntry(simulation_factors, "Neuron Input Current (A)", self.neu_input_curr, 1, 3)

        # The intervals of the input current being supplied to an input neuron - label and entry field.
        self.neu_input_intervals = tk.StringVar(value=5)
        self.makeLabelAndEntry(simulation_factors, "Input Intervals (ms)", self.neu_input_intervals, 1, 4)

        # The total time the simulation will run for - label and entry field.
        self.sim_end_time = tk.StringVar(value=500)
        self.makeLabelAndEntry(simulation_factors, "Simulation End Time (ms)", self.sim_end_time, 1, 5)

        # The memory capacity of the neural network - label and entry field.
        self.mem_capacity = tk.StringVar(value=100)
        self.makeLabelAndEntry(simulation_factors, "Memory Capacity (%)", self.mem_capacity, 1, 6)

        # The synaptic strength of the connections in the neural network - label and entry field.
        self.synaptic_strength = tk.StringVar(value=7)
        self.makeLabelAndEntry(simulation_factors, "Synaptic Strength", self.synaptic_strength, 1, 7)

        # Aged brain factors frame title - label.
        self.aged_brain_factors_title = ttk.Label(aged_brain_factors, style='Title.TLabel', text="Aged Brain Factors")
        self.aged_brain_factors_title.grid(column=1, row=0, columnspan=2)

        # Decrease synaptic strength of the connections in the neural network - label and checkbutton.
        self.dec_synaptic_strength = tk.IntVar()
        self.makeLabelAndCheckbutton(aged_brain_factors, "Decrease Synaptic Strength", self.dec_synaptic_strength, 1, 1)

        # Increase neurodegeneration in the neural network - label and checkbutton.
        self.inc_neurodegen = tk.IntVar()
        self.makeLabelAndCheckbutton(aged_brain_factors, "Increased Neurodegeneration", self.inc_neurodegen, 1, 2)

        # Inhibit LTP in the neural network - label and checkbutton.
        self.inhibited_LTP = tk.IntVar()
        self.makeLabelAndCheckbutton(aged_brain_factors, "Inhibited LTP", self.inhibited_LTP, 1, 3)

    # Makes a label and entry side by side using the variables provided from the parameters.
    def makeLabelAndEntry(self, master, text, text_variable, column, row):
        ttk.Label(master, style='Parameters.TLabel', text=text).grid(column=column, columnspan=2, row=row)
        ttk.Entry(master, style='Parameters.TEntry', textvariable=text_variable).grid(column=(column + 2), row=row)

    # Makes a label and checkbutton side by side using the variables provided from the parameters.
    def makeLabelAndCheckbutton(self, master, text, variable, column, row):
        ttk.Label(master, style='Parameters.TLabel', text=text).grid(column=column, columnspan=2, row=row)
        tk.Checkbutton(master, highlightbackground='black', highlightcolor='pink', selectcolor="red",
                       activeforeground="red", activebackground="red",
                       disabledforeground="white", background="white", indicatoron=False, padx=11, pady=2,
                       variable=variable).grid(column=(column + 2), row=row)

    # Turn off all the simulations that are running or are not the target_simulator before turning on the
    # target_simulator (if provided). This makes sure multiple different simulations are not running at the same time
    # that can lead to freezes, large long memory tasks and more possible bugs. Threading was tried to be implemented
    # but it quickly led to segmentation faults when more than 2 simulations ran simultaneously and could not find a
    # solution as tkinter is not very thread friendly. Queues are possible workarounds but even they are just a way
    # to communicate between threads. Different operating systems allocate different amounts of memory to programs.
    # As a single simulation already takes a lot of processing power, it was decided to not implement
    # threading as it was a more reliable way for the application to run as it will lead to less computer freezes. So
    # instead, when the user decides to run a simulator when a different simulation is already running, the
    # running simulation is stopped before the former simulator is run.
    def toggleSimulations(self, target_simulator):
        simulators = self.simulators
        for simulator in simulators:
            if (simulator is not target_simulator) and simulator.brain_frame.brain.running:
                simulator.brain_frame.toggleRunSimulation()
        if target_simulator is not None:
            target_simulator.brain_frame.toggleRunSimulation()

    # Removes a simulator from the list of simulators.
    def removeSimulator(self, simulator):
        self.simulators.remove(simulator)

    # Closes all simulations then closes the window.
    def exitCommand(self):
        simulators = self.simulators[:]
        for simulator in simulators:
            simulator.exitCommand(self.removeSimulator)
        self.destroy()

    # Generate a young brain model. The young brain model is exactly like the aged brain model but any of the aged
    # brain factors are set to 0 meaning False.
    def generateYoungModel(self):
        # Stops simulations before generation of a new one so no inappropriate overlapping of methods occur.
        self.toggleSimulations(None)
        young_brain = SimulatorWindow(self.sim_end_time.get(), 0, self.no_input_neu.get(),
                                      self.no_output_neu.get(), self.mem_capacity.get(), self.synaptic_strength.get(),
                                      0, 0, self.neu_input_intervals.get(), self.neu_input_curr.get(), "Young Brain",
                                      toggleSimulations=self.toggleSimulations, removeSimulator=self.removeSimulator)
        # Add the simulator to the list of simulators.
        self.simulators.append(young_brain)

    # Generate an aged brain model. Act's similarly to the generateYoungModel(...) function but does not set the aged
    # brain factors to 0.
    def generateAgedModel(self):
        self.toggleSimulations(None)
        aged_brain = SimulatorWindow(self.sim_end_time.get(), self.inhibited_LTP.get(), self.no_input_neu.get(),
                                     self.no_output_neu.get(), self.mem_capacity.get(), self.synaptic_strength.get(),
                                     self.dec_synaptic_strength.get(), self.inc_neurodegen.get(),
                                     self.neu_input_intervals.get(), self.neu_input_curr.get(), "Aged Brain",
                                     toggleSimulations=self.toggleSimulations, removeSimulator=self.removeSimulator)
        self.simulators.append(aged_brain)

# if __name__ == "__main__":
#     app = InitialisationWindow()
#     app.mainloop()
