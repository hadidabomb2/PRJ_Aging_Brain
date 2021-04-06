import tkinter as tk
from tkinter import ttk

from analysis.BrainAnalysis import getDataFrameLists, getDataFrameGroupedByTimeAndMaximised
from view.NeuralNetworkFrame import NeuralNetworkFrame
import matplotlib.pyplot as plt


# The simulator window that parses in the data received from the MainWindow, initialises the NeuralNetworkFrame class
# with the appropriate arguments and deals with other window logic.
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

        width = 720
        height = 720
        x = (self.winfo_screenwidth() / 2)
        # Place the window more on the left if it is a Young Brain.
        if title == "Young Brain":
            x = (self.winfo_screenwidth() / 2) - width
        y = (self.winfo_screenheight() / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

        # Set the title of the window.
        self.title("Learning Simulator: " + title)
        self.title_text = title

        window_toolbar = ttk.Frame(self)
        window_toolbar.pack(side="bottom", fill="both")
        # Button to close the window.
        exit_button = ttk.Button(window_toolbar, style='Exit.TButton', text="Exit",
                                 command=lambda: self.exitCommand(removeSimulator))
        exit_button.pack(side="left")
        view_properties_button = ttk.Button(window_toolbar, style='RunSimulation.TButton', text="View Properties",
                                       command=lambda: self.viewProperties(simulation_args))
        view_properties_button.pack(side="right")

        # This holds all the arguments that need to be passed to the NeuralNetworkFrame in a certain order. The first
        # element is the end_time.
        simulation_args = [float(end_time)]

        # Learning types
        if learning_type_boolean == 0:  # If 'Inhibited LTP' was selected or not
            simulation_args.append('LTP')
        else:
            simulation_args.append('MIS')

        # Number of input and output neurons
        neu_dec_factor = 0.8
        if inc_neurodegen == 0:  # If 'Increased Neurodegeneration' was selected or not
            simulation_args.append(int(input_neu_size))
            simulation_args.append(int(output_neu_size))
        else:
            simulation_args.append(int(input_neu_size * neu_dec_factor))
            simulation_args.append(int(output_neu_size * neu_dec_factor))

        # Memory Capacity
        simulation_args.append(float(mem_capacity) / 100)

        # Synaptic Strength
        synaptic_strength_dec_factor = 0.6
        if dec_synaptic_strength == 0:  # If 'Decreased Synaptic Stength' was selected or not
            simulation_args.append(float(synaptic_strength))
        else:
            simulation_args.append(float(synaptic_strength) * synaptic_strength_dec_factor)

        # Neuron input current and intervals
        simulation_args.append(float(neu_input_intervals))
        simulation_args.append(float(neu_input_curr))

        # Create frame that will display the neural network.
        self.neural_network_frame = NeuralNetworkFrame(simulation_args, lambda: toggleSimulations(self), self)

    # Closes the window safely. Setting the self.neural_network_frame.simulation.running to False stops the simulation
    # in the backend. Errors in tinker callbacks are raised if the backend is running but the SimulationWindow has been
    # closed, callback in the LearningSimulator.runSimulation(...) method leads to nothing. The removeSimulator
    # callback leads to the MainWindow class.
    def exitCommand(self, removeSimulator):
        if self.neural_network_frame.simulation.running:
            self.neural_network_frame.simulation.running = False
        # Make callback to the main window to remove this simulator from the list of simulators it holds.
        removeSimulator(self)
        # Close the window.
        self.destroy()
        print("Simulation Closed")

    # Displays the properties page of the simulation
    def viewProperties(self, neural_network_args):
        # Plotting the total number of output neurons spiked by the time lapsed.
        simulation = [self.neural_network_frame.simulation]
        df = getDataFrameLists(simulation, "learned_times", getDataFrameGroupedByTimeAndMaximised)
        fig = plt.figure(figsize=(15, 7))
        # Display the model parameters on the right hand side of the graph.
        plt.figtext(0.80, 0.83, "Model Parameters:", horizontalalignment='left', wrap=True, fontsize=15)
        plt.figtext(0.80, 0.53, self.getModelParametersAsString(neural_network_args), horizontalalignment='left', wrap=True,
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
