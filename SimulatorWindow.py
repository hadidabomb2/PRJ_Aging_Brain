# from tkinter import *
# from BrainSimulator import BrainSimulator
#
#
# class Application(Canvas):
#     def say_hi(self):
#         print("hi there, everyone!")
#
#     def createWidgets(self):
#         self.QUIT = Button(self)
#         self.QUIT["text"] = "QUIT"
#         self.QUIT["fg"] = "red"
#         self.QUIT["command"] = self.quit
#
#         self.QUIT.pack({"side": "bottom"})
#
#         self.hi_there = Button(self)
#         self.hi_there["text"] = "Hello",
#         self.hi_there["command"] = self.say_hi
#
#         self.hi_there.pack({"side": "top"})
#
#     def createScrollableContainer():
#         cTableContainer.config(xscrollcommand=sbHorizontalScrollBar.set, yscrollcommand=sbVerticalScrollBar.set,
#                                highlightthickness=0)
#         sbHorizontalScrollBar.config(orient=tk.HORIZONTAL, command=cTableContainer.xview)
#         sbVerticalScrollBar.config(orient=tk.VERTICAL, command=cTableContainer.yview)
#
#         sbHorizontalScrollBar.pack(fill=tk.X, side=tk.BOTTOM, expand=tk.FALSE)
#         sbVerticalScrollBar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
#         cTableContainer.pack(fill=tk.BOTH, side=tk.LEFT, expand=tk.TRUE)
#         cTableContainer.create_window(0, 0, window=fTable, anchor=tk.NW)
#
#     def createNeuron(self, canvas, x, y, r, neuron):
#         x0 = x - r
#         y0 = y - r
#         x1 = x + r
#         y1 = y + r
#         canvas.create_oval(x0, y0, x1, y1)
#
#     def __init__(self, master=None):
#         Canvas.__init__(self, master, bg='#FFFFFF', scrollregion=self.bbox("all"))
#         fTable = Frame(self)
#         sbVerticalScrollBar = Scrollbar(master)
#
#         self.pack(expand=True, fill=BOTH)  # .grid(row=0,column=0)
#         vbar = Scrollbar(self, orient=VERTICAL)
#         vbar.pack(side=RIGHT, fill=Y, expand=False)
#         vbar.config(command=self.yview)
#         self.config(yscrollcommand=vbar.set)
#         self.pack(side=LEFT, expand=True, fill=BOTH)
#
#         self.brain = BrainSimulator(50, 'MIS', 50, 10, 1, 5)
#         network = self.brain.network_structure.network
#         for i in range(len(list(network))):
#             self.createNeuron(self, 40, 20 + 45 * i, 20, list(network)[i])
#         # self.createWidgets()
#
#
# root = Tk()
# root.geometry("1080x720")
# app = Application(master=root)
# app.mainloop()
# root.destroy()

import tkinter as tk
from tkinter import ttk

from BrainSimulator import BrainSimulator


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1080x720")
        container = ttk.Frame(self)
        canvas = tk.Canvas(container, width=540, height=1080, borderwidth=0)
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

        brain = BrainSimulator(50, 'MIS', 15, 10, .5, 5)
        input_neuron_list = brain.network_structure.getInputNeuronsList()
        output_neuron_list = brain.network_structure.getOutputNeuronList()
        input_centering = 0
        output_centering = 0
        height_diff = ((len(input_neuron_list) - len(output_neuron_list)) * self.cellheight)
        if height_diff > 0:
            output_centering = height_diff / 2
        elif height_diff < 0:
            input_centering = abs(height_diff / 2)

        network = brain.network_structure.network

        oval_spacing = 7
        for i, input_neuron in enumerate(input_neuron_list):
            x1 = self.cellwidth
            x2 = x1 + self.cellwidth - oval_spacing
            y1 = i * (self.cellheight + 10) + input_centering + 20
            y2 = y1 + self.cellheight - oval_spacing
            self.input_neurons.append((input_neuron, canvas.create_oval(x1, y1, x2, y2, fill="blue",
                                                                        tags="input_neuron")))
        for j, output_neuron in enumerate(output_neuron_list):
            x1 = 10 * self.cellwidth
            x2 = x1 + self.cellwidth - oval_spacing
            y1 = j * (self.cellheight + 10) + output_centering + 20
            y2 = y1 + self.cellheight - oval_spacing
            self.output_neurons.append((output_neuron, canvas.create_oval(x1, y1, x2, y2, fill="green",
                                                                          tags="output_neuron")))

        for input_neuron_canvas in self.input_neurons:
            input_neuron_coords = canvas.coords(input_neuron_canvas[1])
            x1 = input_neuron_coords[2] - ((input_neuron_coords[2] - input_neuron_coords[0]) / 2)
            y1 = input_neuron_coords[3] - ((input_neuron_coords[3] - input_neuron_coords[1]) / 2)
            connections_list = brain.network_structure.getInputNeuronConnections(input_neuron_canvas[0])
            for l, connection in enumerate(connections_list):
                output_neuron = connection[0]
                output_neuron_id = [x[1] for x in self.output_neurons if x[0] == output_neuron][0]
                output_neuron_coords = canvas.coords(output_neuron_id)
                x2 = output_neuron_coords[2] - ((output_neuron_coords[2] - output_neuron_coords[0]) / 2)
                y2 = output_neuron_coords[3] - ((output_neuron_coords[3] - output_neuron_coords[1]) / 2)
                canvas.create_line(x1, y1, x2, y2, fill="black", width=1)

        container.pack(side="left", fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


if __name__ == "__main__":
    app = App()
    app.mainloop()
