# https://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
# https://stackoverflow.com/questions/4781184/tkinter-displaying-a-square-grid
# https://stackoverflow.com/questions/40843039/how-to-write-a-simple-callback-function

import random
import tkinter as tk
import time as clock
from tkinter import ttk
from BrainSimulator import BrainSimulator


# This class is inherits from a tk.Frame object and is responsible for displaying and running the main neural network
# in this simulation
class BrainFrame(ttk.Frame):
    def __init__(self, brain_args, toggleSimulations, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

        # A common variable name referencing itself to fit the more standard practice of coding GUIs.
        container = self
        # Args ordering defined in SimulatorWindow file.
        self.brain_args = brain_args
        brain = BrainSimulator(brain_args[0], brain_args[1], brain_args[2], brain_args[3], brain_args[4], brain_args[5],
                               brain_args[6])
        self.brain = brain

        # The canvas that holds the neuron and connection representations. When the 'Run Simulation' button is pressed,
        # the canvas focuses, I have removed the highlight thickness so it does not show it being focused.
        canvas = tk.Canvas(container, highlightthickness=0)
        self.canvas = canvas

        # A scrollbar to scroll down when the amount of neurons is large enough to go off screen.
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Scrollbar configuration defining the scroll region of the scrollbar.
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Default neuron width and height, editing these will change the shape of the ovals that represent the
        # neurons.
        self.neuron_width = 40
        self.neuron_height = 40
        # Lists that hold references to all of the appropriate item id's and item objects. This is needed to keep track
        # of which elements in the brain reference which objects created to represent them in the canvas.
        self.input_neurons = []
        self.output_neurons = []
        self.connections = []
        # This list is needed so we do not keep needlessly highlighting connections that underwent learning at older
        # timesteps. It holds the list of connections that have been changed/highlighted at previous timesteps.
        self.changed_learned_connections = []

        brain_input_neurons = brain.neural_network.getInputNeuronsList()
        brain_output_neurons = brain.neural_network.getOutputNeuronList()

        # Adjusts the height of the neurons when the number of input and output neurons are uneven. Without this,
        # there would always be trailing ovals at the end of the longer section. The centering balances it so the
        # smaller section is appropriately vertically spaced.
        input_centering = 0
        output_centering = 0
        height_diff = ((len(brain_input_neurons) - len(brain_output_neurons)) * self.neuron_height)
        if height_diff > 0:
            output_centering = height_diff / 2
        elif height_diff < 0:
            input_centering = abs(height_diff / 2)

        # The oval spacing defines how vertically spaced out each neuron is in each column.
        oval_spacing = 7
        # Display the neurons and connections.
        self.displayNeuronsAsOvals(self.input_neurons, brain_input_neurons, oval_spacing, 1, canvas, input_centering,
                                   "blue", "input_neuron")
        self.displayNeuronsAsOvals(self.output_neurons, brain_output_neurons, oval_spacing, 10, canvas,
                                   output_centering,
                                   "green", "output_neuron")
        self.displayConnectionsAsLines(self.input_neurons, self.output_neurons, self.connections, canvas,
                                       brain.neural_network)

        # Run simulation button which makes the callback to the MainWindow to call the toggleSimulations function.
        self.run_simulation = ttk.Button(canvas, style='RunSimulation.TButton', text="Run Simulation", command=toggleSimulations)
        # A time stamp telling the user the current time of the simulation.
        self.time_stamp = ttk.Label(canvas, style='Timestamp.TLabel', text=self.getTimeStampText())
        container.pack(side="left", fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.run_simulation.pack(side="top")
        self.time_stamp.pack(side="bottom")

    # Takes in a neuron list of the canvas, a neuron list of the brain and other configuration parameters to display
    # each neuron as an oval in a single column. It also appends the neuron and the item id of the created oval
    # belonging to the neuron to the neuron list of the canvas.
    def displayNeuronsAsOvals(self, neuron_list_canvas, neuron_list_brain, oval_spacing, horizontal_shift, canvas,
                              centering, fill, tag):
        for i, neuron in enumerate(neuron_list_brain):
            # Added margins to position the column of neurons appropriately in the window
            x_margin = 110
            y_margin = 40
            # The horizontal shift controls how far the column should be shifted in the x-axis.
            x1 = (self.neuron_width * horizontal_shift) + x_margin
            x2 = x1 + self.neuron_width
            # Multiplying by 'i' during the loop so each neuron is positioned below the previous neuron created.
            y1 = ((self.neuron_height + oval_spacing) * i) + centering + y_margin
            y2 = y1 + self.neuron_height
            # Add a reference of the neuron and oval object (item id) created for it.
            neuron_list_canvas.append([neuron, canvas.create_oval(x1, y1, x2, y2, fill=fill,
                                                                  tags=tag)])

    # Works similarly to the displayNeuronsAsOvals(...) method but displays connections as lines instead.
    # Lists of the input and output neurons are required to find which object in the canvas belongs to which neuron
    # that is involved in the connection.
    def displayConnectionsAsLines(self, input_neurons, output_neurons, connections, canvas, neural_network):
        for input_neuron in input_neurons:
            # Find mid point of the input neuron of the connection to draw the line from.
            input_neuron_coords = canvas.coords(input_neuron[1])
            x1 = (input_neuron_coords[2] + input_neuron_coords[0]) / 2
            y1 = (input_neuron_coords[3] + input_neuron_coords[1]) / 2
            connections_list = neural_network.getInputNeuronConnections(input_neuron[0])
            for k, connection in enumerate(connections_list):
                output_neuron = connection.getOutputNeuron()
                # Find the item id of the object in the canvas the output neuron represents.
                output_neuron_id = [x[1] for x in output_neurons if x[0] == output_neuron][0]
                # Find mid point of the output neuron of the connection to draw the line to.
                output_neuron_coords = canvas.coords(output_neuron_id)
                x2 = (output_neuron_coords[2] + output_neuron_coords[0]) / 2
                y2 = (output_neuron_coords[3] + output_neuron_coords[1]) / 2
                # Add a reference of the connection and line object (item id) created for it.
                connections.append([connection, canvas.create_line(x1, y1, x2, y2, fill="grey",
                                                                   tags="connection")])

    # Called by the MainWindow class. It stops the simulation by setting the running variable in the BrainSimulator to
    # False and starts it again by calling the runSimulation(...) method in the BrainSimulator.
    def toggleRunSimulation(self):
        if self.brain.running:
            self.brain.running = False
            # Update the run_simulation button to say Run Simulation once you stop it.
            self.run_simulation.config(text="Run Simulation")
            print("Simulation Stopped")
        else:
            # Update the run_simulation button to say Stop Simulation once you start it.
            self.run_simulation.config(text="Stop Simulation")
            print("Simulation Started")
            # The connections only change in MIS so we call updateConnections only when the learning type is 'MIS'.
            if self.brain.learning_type == 'MIS':
                self.brain.runSimulation(self.brain_args[7], updateCanvas=self.updateCanvas,
                                         updateConnections=self.updateConnections)
            else:
                self.brain.runSimulation(self.brain_args[7], updateCanvas=self.updateCanvas)

        # Once the simulation is over, set the running value to False and update the GUI again.
        if self.brain.running:
            self.brain.running = False
            self.run_simulation.config(text="Run Simulation")
            print("Simulation Ended")

    # This method removes an old connection and adds a new connection to the GUI. Only happens during MIS and if it
    # is passed through by parameters to the runSimulation(...) method (check toggleRunSimulation(...) method.
    def updateConnections(self, new_connection, old_connection):
        canvas = self.canvas
        connections = self.connections

        # Find the object that represents the old connection and remove it.
        old_connection = [x for x in connections if x[0] == old_connection][0]
        canvas.delete(old_connection[1])
        connections.remove(old_connection)

        # Find the coordinates of the output neuron of the new connection.
        output_neuron_id = [x[1] for x in self.output_neurons if x[0] == new_connection.getOutputNeuron()][0]
        output_neuron_coords = canvas.coords(output_neuron_id)

        # Find the coordinates of the input neuron of the new connection.
        input_neuron_id = [x[1] for x in self.input_neurons if x[0] == new_connection.getInputNeuron()][0]
        input_neuron_coords = canvas.coords(input_neuron_id)

        # Find mid point of the input and output neuron coordinates
        x1 = (input_neuron_coords[2] + input_neuron_coords[0]) / 2
        y1 = (input_neuron_coords[3] + input_neuron_coords[1]) / 2
        x2 = (output_neuron_coords[2] + output_neuron_coords[0]) / 2
        y2 = (output_neuron_coords[3] + output_neuron_coords[1]) / 2
        # Finds the mid point between the input and output neurons and add a random appropriate value. This is
        # Necessary as otherwise, the new connection would simply overlap the already connected connection present,
        # showing no indication of a new connection.
        x3 = abs(x2 + x1) / 2 + random.randint(-self.neuron_width, self.neuron_width)
        y3 = abs(y2 + y1) / 2 + random.randint(-self.neuron_height, self.neuron_height)

        # The line is smoothed out looking like a curve.
        connections.append([new_connection, self.canvas.create_line(x1, y1, x3, y3, x2, y2, fill="grey", smooth=1,
                                                                    tags="connection")])
        # Update GUI
        self.update()

    # This method highlights the connection and neurons that undergo learning at a specific timestep. Once a connection
    # is highlighted, it stays highlighted but the neurons reset their colour. It is called at the end of the
    # runSimulation(...) if passed through by parameters (check toggleRunSimulation(...) method).
    def updateCanvas(self):
        # Update time_stamp label to display current time in the simulation.
        self.time_stamp.config(text=self.getTimeStampText())
        canvas = self.canvas
        learned_connections = self.brain.learned_connections
        input_neurons = self.input_neurons
        connections = self.connections
        changed_learned_connections = self.changed_learned_connections
        chosen_input_neuron = self.brain.chosen_input_neuron

        # Reset all neuron colours.
        for input_neuron in input_neurons:
            canvas.itemconfig(input_neuron[1], fill="blue")
        output_neurons = self.output_neurons
        for output_neuron in output_neurons:
            canvas.itemconfig(output_neuron[1], fill="green")

        # Get the connections that got added to the learned_connections list at the current timestamp. They are the
        # unchanged connections we need to highlight as they are currently undergoing learning according to our
        # simulation.
        unchanged_learned_connections = [x for x in learned_connections if x not in changed_learned_connections]

        # Highlight the neuron that is being current is being supplied to.
        if chosen_input_neuron:
            chosen_input_neuron_id = [x[1] for x in input_neurons if x[0] == chosen_input_neuron][0]
            canvas.itemconfig(chosen_input_neuron_id, fill="orange red")

        # Highlight all the connections in the unchanged_learned_connections list and append the connection to the
        # changed_learned_connections list.
        for learned_connection in unchanged_learned_connections:
            output_neuron_id = [x[1] for x in output_neurons if x[0] == learned_connection.getOutputNeuron()][0]
            input_neuron_id = [x[1] for x in input_neurons if x[0] == learned_connection.getInputNeuron()][0]
            connection_id = [x[1] for x in connections if x[0] == learned_connection][0]
            canvas.itemconfig(output_neuron_id, fill="red")
            canvas.itemconfig(input_neuron_id, fill="red")
            canvas.itemconfig(connection_id, fill="red", width=2)
            changed_learned_connections.append(learned_connection)
        # Update GUI
        self.update()

        # If there has been learning at this timestep, meaning unchanged_learned_connections is not empty, make the
        # whole simulation sleep for a very short time so the user can see the changes before the next iteration.
        if unchanged_learned_connections:
            clock.sleep(0.5)

    # Returns the time of the simulation in a viewable format. It is formatted to always be adjusted
    # to 5 decimal places.
    def getTimeStampText(self):
        return "Time Stamp: " + '{:.5f}'.format((round(self.brain.time, 5))) + ' ms'
