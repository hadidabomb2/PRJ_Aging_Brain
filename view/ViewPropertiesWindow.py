"""
The code that displays the generated matplotlib figure has been learnt and adpated from the Eric Levieil answer in
the July 15, 2015 stack overflow post 'Placing plot on Tkinter main window in Python':
https://stackoverflow.com/questions/31440167/placing-plot-on-tkinter-main-window-in-python
"""
import tkinter as tk
from tkinter import ttk, messagebox
from analysis.BrainAnalysis import getDataFrameLists, getDataFrameGroupedByTimeAndMaximised
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
import glob
matplotlib.use('TkAgg')


# The view properties window that displays the simulations parameters and a quick analysis plot. The user can also
# save the results of the simulation from this window as a .csv file in the analysis folder.
class ViewPropertiesWindow(tk.Tk):
    def __init__(self, simulation, neural_network_args, title_text, removePropertiesWindow, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Get the simulation results as a dataframe using methods from the BrainAnalysis.py file in the analysis
        # folder.
        df = getDataFrameLists(simulation, "learned_times", getDataFrameGroupedByTimeAndMaximised)[0]
        self.df = df
        self.title_text = title_text

        # The styling of the ttk items in this class.
        s = ttk.Style(self)
        s.configure('Save.TButton', font='helvetica 14', foreground='black', padding=[10, 10, 10, 5])
        s.configure('Exit.TButton', font='helvetica 14', foreground='red', padding=[5, 10, 5, 5])
        s.configure('ParametersTitle.TLabel', font='helvetica 14', foreground='black', padding=[10, 10, 10, 5])
        s.configure('Parameters.TLabel', font='helvetica 12', foreground='black', padding=[10, 5, 10, 17])

        self.title("Properties of the " + title_text)

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        # Create the window toolbar that will hold the exit button and the save results buttons.
        window_toolbar = ttk.Frame(self)
        window_toolbar.pack(side="bottom", fill="both")

        # Save the results button.
        save_results_btn = ttk.Button(window_toolbar, text="Save Results", style='Save.TButton',
                                      command=self.saveResults)
        save_results_btn.pack(side="right")

        # Exit button.
        exit_button = ttk.Button(window_toolbar, text="Exit", style='Exit.TButton',
                                 command=lambda: self.exitCommand(removePropertiesWindow))
        exit_button.pack(side="left")

        # Display simulation parameters title.
        ttk.Label(container, style='ParametersTitle.TLabel', text="Model Parameters").pack(side="top")

        # Display simulation parameters.
        model_parameters_text = self.getModelParametersAsString(neural_network_args)
        ttk.Label(container, style='Parameters.TLabel', text=model_parameters_text).pack(side="top")

        # Plotting the total number of output neurons spiked by the time lapsed and saving it on a figure.
        fig = plt.figure(figsize=(7, 5))
        ax = fig.add_subplot(111)
        ax.set_title("Analysing Learning Times w/ " + title_text, fontsize=20)
        ax.scatter(df['Time'], df['No_Spiked'], linewidth=1)
        ax.plot(df['Time'], df['No_Spiked'], linewidth=3)
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("No. of Output Nodes Spiked")

        # Displaying the figure.
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.get_tk_widget().pack(side="top")
        canvas.draw()

    # Closes the window.
    def exitCommand(self, removePropertiesWindow):
        # Callback to remove this window from the list of properties windows in the SimulatorWindow class.
        removePropertiesWindow(self)
        self.destroy()

    # Saves the results in the analysis folder as a .csv. If a file is present in that folder, meaning results of
    # this brain type have been saved before, a confirmation box appears before continuing.
    def saveResults(self):
        # File name is based off if it is a young or aged brain.
        filename = "./analysis/Results" + self.title_text.replace(" ", "") + ".csv"
        warning_msg = "There is already a results file of this type present in the analysis folder. Continuing would" \
                      " overwrite this results file, do you still want to continue?"
        # Check if the file already exists in the analysis folder.
        file_exists = glob.glob(filename)
        # If file exists, go through confirmation box logic. Otherwise, save the file.
        if file_exists:
            answer = messagebox.askyesno("File Already Exists", warning_msg, parent=self)
            # If user pressed yes, continue to save overwriting the file present in the analysis folder.
            if answer:
                self.df.to_csv(filename)
                # Display appropriate information to the user.
                messagebox.showinfo("File Overwritten", "The results at " + filename + " have been overwritten.",
                                    parent=self)
        else:
            self.df.to_csv(filename)
            # Display appropriate information to the user.
            messagebox.showinfo("File Saved", "The results have been saved at " + filename + ".", parent=self)

    # Returns the model parameters as a string with appropriate formatting.
    def getModelParametersAsString(self, brain_args):
        text = "Simulation End Time (ms): " + str(brain_args[0]) + "   |   " + \
               "Learning Type: " + str(brain_args[1]) + "   |   " + \
               "No. of Input Neurons: " + str(brain_args[2]) + "   |   \n" + \
               "No. of Output Neurons: " + str(brain_args[3]) + "   |   " + \
               "Memory Capacity (%): " + str(brain_args[4] * 100) + "   |   " + \
               "Synaptic Strength: " + str(brain_args[5]) + "   |   \n" + \
               "Input Intervals (ms): " + str(brain_args[6]) + "   |   " + \
               "Neuron Input Current (A): " + str(brain_args[7])
        return text
