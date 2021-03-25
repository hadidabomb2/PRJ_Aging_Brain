# https://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
# https://stackoverflow.com/questions/4781184/tkinter-displaying-a-square-grid
# https://stackoverflow.com/questions/40843039/how-to-write-a-simple-callback-function

import tkinter as tk
from tkinter import ttk

from analysis.BrainAnalysis import getDataFrameLists, getDataFrameGroupedByTimeAndMaximised
from view.BrainFrame import BrainFrame
import matplotlib.pyplot as plt


# The simulator window that parses in the data received from the MainWindow, initialises the BrainFrame class with
# the appropriate arguments and deals with other window logic.
class SimulatorWindow(tk.Tk):
    def __init__(self, end_time, learning_type_boolean, input_neu_size, output_neu_size, mem_capacity,
                 synaptic_strength, dec_synaptic_strength, inc_neurodegen, neu_input_intervals, neu_input_curr, title,
                 toggleSimulations, removeSimulator, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # The styling of the ttk items in this class.
        s = ttk.Style(self)
        s.configure('RunSimulation.TButton', font='helvetica 14', foreground='black', padding=[10, 10, 10, 5])
        s.configure('Exit.TButton', font='helvetica 14', foreground='red', padding=[5, 10, 5, 5])
        s.configure('Title.TLabel', font='helvetica 16', foreground='black', padding=[5, 15, 5, 10])
        s.configure('Timestamp.TLabel', font='helvetica 14', foreground='black', padding=[5, 17, 5, 17])

        # Call the self.exitCommand method whenever the window is attempted to be closed in other ways than pressing
        # the exit button.
        self.protocol("WM_DELETE_WINDOW", lambda: self.exitCommand(removeSimulator))

        x = self.winfo_screenwidth() / 8  # width of the screen / 8
        # Place the window more on the right if it is an Aged Brain.
        if title == "Aged Brain":
            x = self.winfo_screenwidth() / 2
        y = self.winfo_screenheight() / 6  # height of the screen / 6
        self.geometry('%dx%d+%d+%d' % (720, 720, x, y))

        # Set the title of the window.
        self.title("Learning Simulator: " + title)
        self.title_text = title

        # This holds all the arguments that need to be passed to the BrainFrame in a certain order. The first element
        # is the end_time.
        brain_args = [end_time]

        # Learning types
        if learning_type_boolean == 0:  # If 'Inhibited LTP' was selected or not
            brain_args.append('LTP')
        else:
            brain_args.append('MIS')

        # Number of input and output neurons
        neu_dec_factor = 0.8
        if inc_neurodegen == 0:  # If 'Increased Neurodegeneration' was selected or not
            brain_args.append(int(input_neu_size))
            brain_args.append(int(output_neu_size))
        else:
            brain_args.append(int(input_neu_size * neu_dec_factor))
            brain_args.append(int(output_neu_size * neu_dec_factor))

        # Memory Capacity
        brain_args.append(mem_capacity / 100)

        # Synaptic Strength
        synaptic_strength_dec_factor = 0.6
        if dec_synaptic_strength == 0:  # If 'Decreased Synaptic Stength' was selected or not
            brain_args.append(int(synaptic_strength))
        else:
            brain_args.append(int(synaptic_strength * synaptic_strength_dec_factor))

        # Neuron input current and intervals
        brain_args.append(neu_input_intervals)
        brain_args.append(neu_input_curr)

        window_toolbar = ttk.Frame(self)
        window_toolbar.pack(side="bottom", fill="both")
        # Button to close the window.
        exit_button = ttk.Button(window_toolbar, style='Exit.TButton', text="Exit",
                                 command=lambda: self.exitCommand(removeSimulator))
        exit_button.pack(side="left")
        properties_button = ttk.Button(window_toolbar, style='RunSimulation.TButton', text="View Properties",
                                       command=lambda: self.viewProperties(brain_args))
        properties_button.pack(side="right")
        # Create frame that will display the neural network.
        self.brain_frame = BrainFrame(brain_args, lambda: toggleSimulations(self), self)

    # Closes the window safely. Setting the self.brain_frame.brain.running to False stops the simulation in the backend.
    # Errors in tinker callbacks are raised if the backend is running but the SimulationWindow has been closed, callback
    # in the BrainSimulator.runSimulation(...) method leads to nothing. The removeSimulator callback leads to the
    # MainWindow class.
    def exitCommand(self, removeSimulator):
        if self.brain_frame.brain.running:
            self.brain_frame.brain.running = False
        # Make callback to the main window to remove this simulator from the list of simulators it holds.
        removeSimulator(self)
        # Close the window.
        self.destroy()
        print("Simulation Closed")

    # Displays the properties page of the simulation
    def viewProperties(self, brain_args):
        # Plotting the total number of output neurons spiked by the time lapsed.
        brain = [self.brain_frame.brain]
        df = getDataFrameLists(brain, "learned_times", getDataFrameGroupedByTimeAndMaximised)
        fig = plt.figure(figsize=(15, 7))
        # Display the model parameters on the right hand side of the graph.
        plt.figtext(0.80, 0.83, "Model Parameters:", horizontalalignment='left', wrap=True, fontsize=15)
        plt.figtext(0.80, 0.53, self.getModelParametersAsString(brain_args), horizontalalignment='left', wrap=True,
                    fontsize=12)
        plt.suptitle("Analysing Learning Times w/ " + self.title_text, fontsize=20)
        plt.plot(df[0]['Time'], df[0]['No_Spiked'], linewidth=3)
        plt.xlabel("Time (ms)")
        plt.ylabel("No. of Output Nodes Spiked")
        # Add space on the right side for the model parameters to fit.
        fig.subplots_adjust(right=0.75)
        # Show the graph with the properties on the right hand side.
        plt.show()

    # Returns the model parameters as a string with appropriate formatting.
    def getModelParametersAsString(self, brain_args):
        text = "Simulation End Time (ms): " + str(brain_args[0]) + "\n" + \
               "Learning Type: " + str(brain_args[1]) + "\n" + \
               "No. of Input Neurons: " + str(brain_args[2]) + "\n" + \
               "No. of Output Neurons: " + str(brain_args[3]) + "\n" + \
               "Memory Capacity (%): " + str(brain_args[4] * 100) + "\n" + \
               "Synaptic Strength: " + str(brain_args[5]) + "\n" + \
               "Input Intervals (ms): " + str(brain_args[6]) + "\n" + \
               "Neuron Input Current (A): " + str(brain_args[7])
        return text
