# https://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
# https://stackoverflow.com/questions/4781184/tkinter-displaying-a-square-grid
# https://stackoverflow.com/questions/40843039/how-to-write-a-simple-callback-function

import random
import tkinter as tk
import time as clock
from threading import Thread
from tkinter import ttk
from BrainSimulator import BrainSimulator


class BrainFrame(tk.Frame):
    def __init__(self, brain_args, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        container = self

        # Args ordering defined in SimulatorWindow file.
        self.brain_args = brain_args
        brain = BrainSimulator(brain_args[0], brain_args[1], brain_args[2], brain_args[3], brain_args[4], brain_args[5])
        self.brain = brain

        canvas = tk.Canvas(container, borderwidth=0)
        self.canvas = canvas

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.neuron_width = 40
        self.neuron_height = 40
        self.input_neurons = []
        self.output_neurons = []
        self.connections = []
        self.changed_learned_connections = []

        input_neuron_list = brain.neural_network.getInputNeuronsList()
        output_neuron_list = brain.neural_network.getOutputNeuronList()
        input_centering = 0
        output_centering = 0
        height_diff = ((len(input_neuron_list) - len(output_neuron_list)) * self.neuron_height)
        if height_diff > 0:
            output_centering = height_diff / 2
        elif height_diff < 0:
            input_centering = abs(height_diff / 2)

        oval_spacing = 7
        self.displayNeuronsAsOvals(self.input_neurons, input_neuron_list, oval_spacing, 1, canvas, input_centering,
                                   "blue", "input_neuron")
        self.displayNeuronsAsOvals(self.output_neurons, output_neuron_list, oval_spacing, 10, canvas, output_centering,
                                   "green", "output_neuron")
        self.displayConnectionsAsLines(canvas, brain.neural_network)

        self.run_simulation = tk.Button(canvas, text="Run Simulation", command=self.threadingRunSimulationCommand)
        self.time_stamp = tk.Label(canvas, text="Time Stamp:  " + '{:.5f}'.format((round(self.brain.time, 5))))
        container.pack(side="left", fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.run_simulation.pack(side="top")
        self.time_stamp.pack(side="bottom")

    def displayNeuronsAsOvals(self, neurons, neuron_list, oval_spacing, horizontal_shift, canvas, centering, fill, tag):
        for i, neuron in enumerate(neuron_list):
            x1 = (self.neuron_width * horizontal_shift) + 110
            x2 = x1 + self.neuron_width
            y1 = ((self.neuron_height + oval_spacing) * i) + centering + 40
            y2 = y1 + self.neuron_height
            neurons.append([neuron, canvas.create_oval(x1, y1, x2, y2, fill=fill,
                                                       tags=tag)])

    def displayConnectionsAsLines(self, canvas, neural_network):
        for input_neuron in self.input_neurons:
            input_neuron_coords = canvas.coords(input_neuron[1])
            x1 = input_neuron_coords[2] - ((input_neuron_coords[2] - input_neuron_coords[0]) / 2)
            y1 = input_neuron_coords[3] - ((input_neuron_coords[3] - input_neuron_coords[1]) / 2)
            connections_list = neural_network.getInputNeuronConnections(input_neuron[0])
            for k, connection in enumerate(connections_list):
                output_neuron = connection.getOutputNeuron()
                output_neuron_id = [x[1] for x in self.output_neurons if x[0] == output_neuron][0]
                output_neuron_coords = canvas.coords(output_neuron_id)
                x2 = output_neuron_coords[2] - ((output_neuron_coords[2] - output_neuron_coords[0]) / 2)
                y2 = output_neuron_coords[3] - ((output_neuron_coords[3] - output_neuron_coords[1]) / 2)
                self.connections.append([connection, canvas.create_line(x1, y1, x2, y2, fill="grey",
                                                                        tags="connection")])

    def threadingRunSimulationCommand(self):
        Thread(target=self.runSimulationCommand).start()

    def runSimulationCommand(self):
        if self.brain.running:
            self.run_simulation.config(text="Run Simulation")
            self.brain.running = False
        else:
            self.run_simulation.config(text="Stop Simulation")
            print("Simulation Started")
            if self.brain.learning_type == 'MIS':
                self.brain.runSimulation(self.brain_args[6], self.brain_args[7], updateCanvas=self.updateCanvas,
                                         updateConnections=self.updateConnections)
            else:
                self.brain.runSimulation(self.brain_args[6], self.brain_args[7], updateCanvas=self.updateCanvas)

        if self.brain.running:
            self.run_simulation.config(text="Run Simulation")
            print("Simulation Ended")
        else:
            print("Simulation Stopped")

    def updateConnections(self, new_connection, old_connection):
        canvas = self.canvas
        connections = self.connections

        old_connection = [x for x in connections if x[0] == old_connection][0]
        canvas.delete(old_connection[1])
        connections.remove(old_connection)

        output_neuron_id = [x[1] for x in self.output_neurons if x[0] == new_connection.getOutputNeuron()][0]
        output_neuron_coords = canvas.coords(output_neuron_id)

        input_neuron_id = [x[1] for x in self.input_neurons if x[0] == new_connection.getInputNeuron()][0]
        input_neuron_coords = canvas.coords(input_neuron_id)

        x1 = input_neuron_coords[2] - ((input_neuron_coords[2] - input_neuron_coords[0]) / 2)
        y1 = input_neuron_coords[3] - ((input_neuron_coords[3] - input_neuron_coords[1]) / 2)
        x2 = output_neuron_coords[2] - ((output_neuron_coords[2] - output_neuron_coords[0]) / 2)
        y2 = output_neuron_coords[3] - ((output_neuron_coords[3] - output_neuron_coords[1]) / 2)
        x3 = abs(x2 + x1) / 2 + random.randint(-self.neuron_width, self.neuron_width)
        y3 = abs(y2 + y1) / 2 + random.randint(-self.neuron_height, self.neuron_height)

        connections.append([new_connection, self.canvas.create_line(x1, y1, x3, y3, x2, y2, fill="grey", smooth=1,
                                                                    tags="connection")])

        self.update()

    def updateCanvas(self):
        self.time_stamp.config(text=("Time Stamp: " + '{:.5f}'.format((round(self.brain.time, 5)))))
        canvas = self.canvas
        learned_connections = self.brain.learned_connections
        input_neurons = self.input_neurons
        connections = self.connections
        changed_learned_connections = self.changed_learned_connections
        chosen_input_neuron = self.brain.chosen_input_neuron

        for input_neuron in input_neurons:
            canvas.itemconfig(input_neuron[1], fill="blue")
        output_neurons = self.output_neurons
        for output_neuron in output_neurons:
            canvas.itemconfig(output_neuron[1], fill="green")
        unchanged_learned_connections = [x for x in learned_connections if x not in changed_learned_connections]

        if chosen_input_neuron:
            chosen_input_neuron_id = [x[1] for x in input_neurons if x[0] == chosen_input_neuron][0]
            canvas.itemconfig(chosen_input_neuron_id, fill="orange red")

        for learned_connection in unchanged_learned_connections:
            output_neuron_id = [x[1] for x in output_neurons if x[0] == learned_connection.getOutputNeuron()][0]
            input_neuron_id = [x[1] for x in input_neurons if x[0] == learned_connection.getInputNeuron()][0]
            connection_id = [x[1] for x in connections if x[0] == learned_connection][0]
            canvas.itemconfig(output_neuron_id, fill="red")
            canvas.itemconfig(input_neuron_id, fill="red")
            canvas.itemconfig(connection_id, fill="red", width=2)
            changed_learned_connections.append(learned_connection)
        self.update()

        if unchanged_learned_connections:
            clock.sleep(0.5)
