# https://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
# https://stackoverflow.com/questions/4781184/tkinter-displaying-a-square-grid
# https://stackoverflow.com/questions/40843039/how-to-write-a-simple-callback-function

import random
import tkinter as tk
import time as clock
from tkinter import ttk
from BrainSimulator import BrainSimulator


class BrainFrame(tk.Frame):
    def __init__(self, brain_args, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.brain_args = brain_args
        container = self

        brain = BrainSimulator(brain_args[0], brain_args[1], brain_args[2], brain_args[3], brain_args[4], brain_args[5])
        self.brain = brain
        self.canvas = tk.Canvas(container, width=540, height=1080, borderwidth=0)
        canvas = self.canvas
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

        self.cellwidth = 40
        self.cellheight = 40
        self.input_neurons = []
        self.output_neurons = []
        self.connections = []
        self.changed_learned_connections = []

        input_neuron_list = brain.network_structure.getInputNeuronsList()
        output_neuron_list = brain.network_structure.getOutputNeuronList()
        input_centering = 0
        output_centering = 0
        height_diff = ((len(input_neuron_list) - len(output_neuron_list)) * self.cellheight)
        if height_diff > 0:
            output_centering = height_diff / 2
        elif height_diff < 0:
            input_centering = abs(height_diff / 2)

        oval_spacing = 7
        for i, input_neuron in enumerate(input_neuron_list):
            x1 = self.cellwidth
            x2 = x1 + self.cellwidth
            y1 = i * (self.cellheight + oval_spacing) + input_centering + 10
            y2 = y1 + self.cellheight
            self.input_neurons.append([input_neuron, canvas.create_oval(x1, y1, x2, y2, fill="blue",
                                                                        tags="input_neuron")])
        for j, output_neuron in enumerate(output_neuron_list):
            x1 = 10 * self.cellwidth
            x2 = x1 + self.cellwidth
            y1 = j * (self.cellheight + oval_spacing) + output_centering + 10
            y2 = y1 + self.cellheight
            self.output_neurons.append([output_neuron, canvas.create_oval(x1, y1, x2, y2, fill="green",
                                                                          tags="output_neuron")])

        for input_neuron_canvas in self.input_neurons:
            input_neuron_coords = canvas.coords(input_neuron_canvas[1])
            x1 = input_neuron_coords[2] - ((input_neuron_coords[2] - input_neuron_coords[0]) / 2)
            y1 = input_neuron_coords[3] - ((input_neuron_coords[3] - input_neuron_coords[1]) / 2)
            connections_list = brain.network_structure.getInputNeuronConnections(input_neuron_canvas[0])
            for l, connection in enumerate(connections_list):
                output_neuron = connection.getOutputNeuron()
                output_neuron_id = [x[1] for x in self.output_neurons if x[0] == output_neuron][0]
                output_neuron_coords = canvas.coords(output_neuron_id)
                x2 = output_neuron_coords[2] - ((output_neuron_coords[2] - output_neuron_coords[0]) / 2)
                y2 = output_neuron_coords[3] - ((output_neuron_coords[3] - output_neuron_coords[1]) / 2)
                self.connections.append([connection, canvas.create_line(x1, y1, x2, y2, fill="grey",
                                                                        tags="connection")])

        run_simulation = tk.Button(canvas, text="Run Simulation", command=self.buttonCommand)
        container.pack(side="left", fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        run_simulation.pack(side="top")

    def buttonCommand(self):
        if self.brain.learning_type == 'MIS':
            self.brain.runSimulation(self.brain_args[6], self.brain_args[7], updateCanvas=self.updateCanvas,
                                     updateConnections=self.updateConnections)
        else:
            self.brain.runSimulation(self.brain_args[6], self.brain_args[7], updateCanvas=self.updateCanvas)

        print("Simulation Ended")

    def updateConnections(self, new_connection, old_connection):
        canvas = self.canvas
        connections = self.connections
        old_connection_canvas = [x for x in connections if x[0] == old_connection][0]
        canvas.delete(old_connection_canvas[1])
        connections.remove(old_connection_canvas)
        output_neuron_id = [x[1] for x in self.output_neurons if x[0] == new_connection.getOutputNeuron()][0]
        output_neuron_coords = canvas.coords(output_neuron_id)
        input_neuron_id = [x[1] for x in self.input_neurons if x[0] == new_connection.getInputNeuron()][0]
        input_neuron_coords = canvas.coords(input_neuron_id)
        x1 = input_neuron_coords[2] - ((input_neuron_coords[2] - input_neuron_coords[0]) / 2)
        y1 = input_neuron_coords[3] - ((input_neuron_coords[3] - input_neuron_coords[1]) / 2)
        x2 = output_neuron_coords[2] - ((output_neuron_coords[2] - output_neuron_coords[0]) / 2)
        y2 = output_neuron_coords[3] - ((output_neuron_coords[3] - output_neuron_coords[1]) / 2)
        x3 = abs(x2 + x1) / 2 + random.randint(-self.cellwidth, self.cellwidth)
        y3 = abs(y2 + y1) / 2 + random.randint(-self.cellheight, self.cellheight)

        connections.append([new_connection, self.canvas.create_line(x1, y1, x3, y3, x2, y2, fill="grey", smooth=1,
                                                                    tags="connection")])

        self.update()

    def updateCanvas(self):
        canvas = self.canvas
        learned_connections = self.brain.learned_connections
        input_neurons = self.input_neurons
        for input_neuron in input_neurons:
            canvas.itemconfig(input_neuron[1], fill="blue")
        output_neurons = self.output_neurons
        for output_neuron in output_neurons:
            canvas.itemconfig(output_neuron[1], fill="green")
        connections = self.connections
        changed_learned_connections = self.changed_learned_connections
        unchanged_learned_connections = [x for x in learned_connections if x not in changed_learned_connections]
        changed = False
        if unchanged_learned_connections:
            changed = True

        for learned_connection in unchanged_learned_connections:
            output_neuron_id = [x[1] for x in output_neurons if x[0] == learned_connection.getOutputNeuron()][0]
            input_neuron_id = [x[1] for x in input_neurons if x[0] == learned_connection.getInputNeuron()][0]
            connection_id = [x[1] for x in connections if x[0] == learned_connection][0]
            canvas.itemconfig(output_neuron_id, fill="red")
            canvas.itemconfig(input_neuron_id, fill="red")
            canvas.itemconfig(connection_id, fill="red", width=2)
            changed_learned_connections.append(learned_connection)
        self.update()

        if changed:
            clock.sleep(0.5)
