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

def createNeuron(canvas, x, y, r, neuron):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        canvas.create_oval(x0, y0, x1, y1, fill='#fff')

root = tk.Tk()
root.geometry("1080x720")
container = ttk.Frame(root)
canvas = tk.Canvas(container)
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

brain = BrainSimulator(50, 'MIS', 15, 10, 1, 5)
network = brain.network_structure.network
for i, inputNeuron in enumerate(brain.network_structure.getInputNeuronsList()):
    createNeuron(canvas, 40, 40 + 45 * i, 20, inputNeuron)
    for j, outputNeuron in enumerate(brain.network_structure.getOutputNeuronList()):
        createNeuron(canvas, 200, 40 + 45 * j, 20, outputNeuron)
        canvas.create_arc(100, 100 + 10, 200, 100 - 10, extent=180, style=tk.ARC)


# for i in range(50):
#     ttk.Label(scrollable_frame, text="Sample scrolling label").pack()

container.pack(side="left", fill="both", expand=True)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()