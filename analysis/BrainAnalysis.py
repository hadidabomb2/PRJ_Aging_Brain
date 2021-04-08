from model.LearningSimulator import LearningSimulator
from pandas import DataFrame
import matplotlib.pyplot as plt


# Creates and returns a DataFrame object. Using the list of values, it groups them and gets the max value for each
# grouping. In this case, the values are specifically the times at which learning has occurred.
def getDataFrameGroupedByTimeAndMaximised(values):
    df = DataFrame(values, columns=['Time'])
    df['No_Spiked'] = df.index + 1
    df = df.groupby('Time').max().reset_index()
    return df


# Creates and returns a DataFrame object using the list of values. In this case, the values are specifically a list
# where the first index is the membrane potential of the neuron and the second index is the time at which that membrane
# potential was recorded.
def getDataFrameByVm(values):
    values_Vm = [x[0] for x in values]
    values_time = [x[1] for x in values]
    df = DataFrame({"Vm": values_Vm, "Time": values_time})
    return df


# Creates and returns a list of DataFrame objects. It loops through a list of BrainSimulators, extracting the required
# list name from each simulator and uses a grouping method that have been defined above to create a DataFrame object to
# append to the list of DataFrame objects. getDataFrameGroupedByTimeAndMaximised(...) and getDataFrameByVm(...) are the
# two currently used grouping methods for this function.
def getDataFrameLists(brain_list, list_name, groupingMethod):
    df_list = []
    for brain in brain_list:
        values = getattr(brain, list_name)
        df_list.append(groupingMethod(values))
    return df_list


# Creates, runs and returns a LearningSimulator object using the parameters that have been passed through.
def initialiseAndRunBrainSimulation(end_time, learning_type, input_neu_size, output_neu_size,
                                    mem_capacity, synaptic_strength_factor, input_interval, input_strength):
    brain = LearningSimulator(end_time, learning_type, input_neu_size, output_neu_size, mem_capacity,
                              synaptic_strength_factor, input_interval)
    brain.runSimulation(input_strength)
    return brain


# Creates and returns a list of simulated LearningSimulators. It loops through distinct set of memory capacities
# using the different memory capacity values to initialise and run multiple LearningSimulators and appends them to a
# list.
def runWithDifferentMemoryCapacities(end_time, learning_type, input_neu_size, output_neu_size,
                                     synaptic_strength_factor, input_interval, input_strength, loop_lower_bound=0):
    brain_list = []
    for i in range(100, loop_lower_bound, -20):
        memory_capacity = i / 100
        brain_list.append(initialiseAndRunBrainSimulation(end_time, learning_type, input_neu_size, output_neu_size,
                                                          memory_capacity, synaptic_strength_factor, input_interval,
                                                          input_strength))
    return brain_list


# Plots the results of two brains at different memory capacities with the only difference being the learning type.
# The graph highlights how the total number of fired neurons changes over time and how the difference in total number
# of fired neurons change over time.
def comparingLearningMechanismBasic(end_time, input_neu_size, output_neu_size, synaptic_strength_factor, input_interval,
                                    input_strength, figure_idx):
    brain_LTP = runWithDifferentMemoryCapacities(end_time, 'LTP', input_neu_size, output_neu_size,
                                                 synaptic_strength_factor, input_interval, input_strength)
    brain_MIS = runWithDifferentMemoryCapacities(end_time, 'MIS', input_neu_size, output_neu_size,
                                                 synaptic_strength_factor, input_interval, input_strength)

    df_LTP = getDataFrameLists(brain_LTP, "learned_times", getDataFrameGroupedByTimeAndMaximised)
    df_MIS = getDataFrameLists(brain_MIS, "learned_times", getDataFrameGroupedByTimeAndMaximised)

    # Reference figure
    fig = plt.figure(figsize=(15, 15))
    # Add a title to the graph
    fig.suptitle("Analysing Learning Times w/ LTM Mechanisms (LTP & MIS)", fontsize=20)
    # Add text on the bottom right hand corner of the graph
    plt.figtext(0.99, 0.01, 'MC stands for Memory Capacity', horizontalalignment='right')
    # Create four subplots to fit in the figure and appropriately labelled
    ((ax1, ax2), (ax3, ax4)) = fig.subplots(2, 2)
    ax1.title.set_text("Long Term Potentiation")
    ax2.title.set_text("Multi-Innervated Dendritic Spines")
    ax3.title.set_text("Long Term Potentiation")
    ax4.title.set_text("Multi-Innervated Dendritic Spines")

    # i will decrease by -20 from 100 until it reaches 0, does not include 0
    counter = 0
    for i in range(100, 0, -20):
        label = str(i) + "% MC"
        # Plot the relevant data to the subplot
        ax1.plot(df_LTP[counter]['Time'], df_LTP[counter]['No_Spiked'], label=label)
        ax2.plot(df_MIS[counter]['Time'], df_MIS[counter]['No_Spiked'], label=label)

        # Simple grouping by then maxing to smooth out the line.
        group_by_amount = 15
        grouped_LTP = df_LTP[counter].groupby(df_LTP[counter].index // group_by_amount).max()
        grouped_MIS = df_MIS[counter].groupby(df_MIS[counter].index // group_by_amount).max()
        # The diff(axis=0) gets the difference of each value compared to it's last by row.
        ax3.plot(grouped_LTP['Time'], grouped_LTP.diff(axis=0)['No_Spiked'], label=label)
        ax4.plot(grouped_MIS['Time'], grouped_MIS.diff(axis=0)['No_Spiked'], label=label)
        counter += 1

    # Place legend on the top left of the subplot and set the axis labels of the subplot
    ax1.legend(loc="upper left")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("No. of Output Nodes Spiked")
    ax2.legend(loc="upper left")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("No. of Output Nodes Spiked")
    ax3.legend(loc="upper right")
    ax3.set_xlabel("Time (ms)")
    ax3.set_ylabel("Difference in No. of Output Nodes Spiked")
    # Limit the x-axis because plateauing part of graph is useless
    ax3.set_xlim([0, 150])
    ax4.legend(loc="upper right")
    ax4.set_xlabel("Time (ms)")
    ax4.set_ylabel("Difference in No. of Output Nodes Spiked")
    ax4.set_xlim([0, 150])

    plt.figure(figure_idx)
    figure_idx += 1


# Plots the results of two brains at different memory capacities with the only difference being the synaptic strength.
# The graph highlights how the total number of fired neurons changes over time and how the difference in total number
# # of fired neurons change over time.
def comparingSynapticStrengthBasic(end_time, learning_type, input_neu_size, output_neu_size, input_interval,
                                   input_strength, figure_idx):
    brain_s1 = runWithDifferentMemoryCapacities(end_time, learning_type, input_neu_size, output_neu_size,
                                                6, input_interval, input_strength)
    brain_s2 = runWithDifferentMemoryCapacities(end_time, learning_type, input_neu_size, output_neu_size,
                                                4, input_interval, input_strength)

    df_s1 = getDataFrameLists(brain_s1, "learned_times", getDataFrameGroupedByTimeAndMaximised)
    df_s2 = getDataFrameLists(brain_s2, "learned_times", getDataFrameGroupedByTimeAndMaximised)

    # Same structure as the comparingLearningMechanismBasic(...) method but with different labels
    fig = plt.figure(figsize=(15, 15))
    fig.suptitle("Analysing Learning Times w/ Synaptic Strength (SS)", fontsize=20)
    plt.figtext(0.99, 0.01, 'MC stands for Memory Capacity', horizontalalignment='right')
    ((ax1, ax2), (ax3, ax4)) = fig.subplots(2, 2)
    ax1.title.set_text("Synaptic Strength set to 6")
    ax2.title.set_text("Synaptic Strength set to 4")
    ax3.title.set_text("Synaptic Strength set to 6")
    ax4.title.set_text("Synaptic Strength set to 4")

    counter = 0
    for i in range(100, 0, -20):
        label = str(i) + "% MC"
        # Plot the relevant data to the subplot
        ax1.plot(df_s1[counter]['Time'], df_s1[counter]['No_Spiked'], label=label)
        ax2.plot(df_s2[counter]['Time'], df_s2[counter]['No_Spiked'], label=label)

        # Simple grouping by then maxing to smooth out the line.
        group_by_amount = 15
        grouped_s1 = df_s1[counter].groupby(df_s1[counter].index // group_by_amount).max()
        grouped_s2 = df_s2[counter].groupby(df_s2[counter].index // group_by_amount).max()
        # The diff(axis=0) gets the difference of each value compared to it's last by row.
        ax3.plot(grouped_s1['Time'], grouped_s1.diff(axis=0)['No_Spiked'], label=label)
        ax4.plot(grouped_s2['Time'], grouped_s2.diff(axis=0)['No_Spiked'], label=label)
        counter += 1

    ax1.legend(loc="upper left")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("No. of Output Nodes Spiked")
    ax2.legend(loc="upper left")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("No. of Output Nodes Spiked")
    ax3.legend(loc="upper right")
    ax3.set_xlabel("Time (ms)")
    ax3.set_ylabel("Difference in No. of Output Nodes Spiked")
    # Limit the x-axis because plateauing part of graph is useless
    ax3.set_xlim([0, 150])
    ax4.legend(loc="upper right")
    ax4.set_xlabel("Time (ms)")
    ax4.set_ylabel("Difference in No. of Output Nodes Spiked")
    ax4.set_xlim([0, 150])

    plt.figure(figure_idx)
    figure_idx += 1


# Plots the results of two brains at different memory capacities with the only difference being the number of neurons.
# The graph highlights how the total number of fired neurons changes over time and how the difference in total number
# # of fired neurons change over time.
def comparingNeuronAmountBasic(end_time, learning_type, synaptic_strength_factor, input_interval,
                               input_strength, figure_idx):
    brain_n1 = runWithDifferentMemoryCapacities(end_time, learning_type, 100, 100,
                                                synaptic_strength_factor, input_interval, input_strength)
    brain_n2 = runWithDifferentMemoryCapacities(end_time, learning_type, 70, 70,
                                                synaptic_strength_factor, input_interval, input_strength)

    df_n1 = getDataFrameLists(brain_n1, "learned_times", getDataFrameGroupedByTimeAndMaximised)
    df_n2 = getDataFrameLists(brain_n2, "learned_times", getDataFrameGroupedByTimeAndMaximised)

    # Same structure as the comparingLearningMechanismBasic(...) method but with different labels
    fig = plt.figure(figsize=(15, 15))
    fig.suptitle("Analysing Learning Times w/ Neuron Amount", fontsize=20)
    plt.figtext(0.99, 0.01, 'MC stands for Memory Capacity', horizontalalignment='right')
    ((ax1, ax2), (ax3, ax4)) = fig.subplots(2, 2)
    ax1.title.set_text("100 Input & Output Neurons")
    ax2.title.set_text("70 Input & Output Neurons")
    ax3.title.set_text("100 Input & Output Neurons")
    ax4.title.set_text("70 Input & Output Neurons")

    counter = 0
    for i in range(100, 0, -20):
        label = str(i) + "% MC"
        # Plot the relevant data to the subplot
        ax1.plot(df_n1[counter]['Time'], df_n1[counter]['No_Spiked'], label=label)
        ax2.plot(df_n2[counter]['Time'], df_n2[counter]['No_Spiked'], label=label)

        # Simple grouping by then maxing to smooth out the line.
        group_by_amount = 15
        grouped_n1 = df_n1[counter].groupby(df_n1[counter].index // group_by_amount).max()
        grouped_n2 = df_n2[counter].groupby(df_n2[counter].index // group_by_amount).max()
        # The diff(axis=0) gets the difference of each value compared to it's last by row.
        ax3.plot(grouped_n1['Time'], grouped_n1.diff(axis=0)['No_Spiked'], label=label)
        ax4.plot(grouped_n2['Time'], grouped_n2.diff(axis=0)['No_Spiked'], label=label)
        counter += 1

    ax1.legend(loc="upper left")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("No. of Output Nodes Spiked")
    ax2.legend(loc="upper left")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("No. of Output Nodes Spiked")
    ax3.legend(loc="upper right")
    ax3.set_xlabel("Time (ms)")
    ax3.set_ylabel("Difference in No. of Output Nodes Spiked")
    # Limit the x-axis because plateauing part of graph is useless
    ax3.set_xlim([0, 150])
    ax4.legend(loc="upper right")
    ax4.set_xlabel("Time (ms)")
    ax4.set_ylabel("Difference in No. of Output Nodes Spiked")
    ax4.set_xlim([0, 150])

    plt.figure(figure_idx)
    figure_idx += 1


# Plots the results of a simulation with only 1 output neuron at different memory capacities. How the membrane potential
# of the single output neuron changed over time is plotted on the graph.
def comparingMembranePotentialBasic(end_time, learning_type, input_neu_size, synaptic_strength_factor, input_interval,
                                    input_strength, figure_idx):
    # The lower bound is set to 50 because there is only 1 output neuron. A memory capacity of less than 50%
    # would mean there are no output neurons to make connections to, null errors will be raised.
    loop_lower_bound = 50
    brain_o1 = runWithDifferentMemoryCapacities(end_time, learning_type, input_neu_size, 1, synaptic_strength_factor,
                                                input_interval, input_strength, loop_lower_bound=loop_lower_bound)

    df_o1 = []
    for brain in brain_o1:
        df_o1.append(getDataFrameByVm(brain.neural_network.getOutputNeuronList()[0].tracking_Vm))

    # No need for subplots as only one plot needed
    fig = plt.figure(figsize=(15, 7))
    plt.figtext(0.99, .01, 'MC stands for Memory Capacity', horizontalalignment='right')
    fig.suptitle("Analysing Membrane Potential of Output Neuron", fontsize=20)
    ax1 = fig.add_subplot(111)
    counter = 0
    # i decreased by 20 from 100 until 50 (the lower bound) is crossed
    for i in range(100, loop_lower_bound, -20):
        ax1.plot(df_o1[counter]['Time'], df_o1[counter]['Vm'], label=(str(i) + "% MC"))
        counter += 1
    ax1.legend(loc="upper left")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Membrane Voltage of Neuron (mV)")
    plt.figure(figure_idx)
    figure_idx += 1


# Main function that calls the methods above with the appropriate parameters to construct an analysis.
def main():
    print("Running analysis, please wait...")
    figure_idx = 1
    comparingLearningMechanismBasic(500, 100, 100, 5, .025, 3.5, figure_idx)
    comparingSynapticStrengthBasic(500, 'LTP', 100, 100, .025, 3.5, figure_idx)
    comparingNeuronAmountBasic(500, 'LTP', 5, .025, 3.5, figure_idx)
    comparingMembranePotentialBasic(500, 'LTP', 15, 5, .05, 3.5, figure_idx)
    plt.show()
    print("Analysis has finished.")

# A simple method where the debug is set to True for the runSimulation(...) method. It's use is to debug the
# simulation so it is not of use anymore, however, it is still an helpful function to have if a user wants to change
# bits of code and observe its effects. Would have to be uncommented out and inserted in the main function.
# def debugNeuron():
#     brain = LearningSimulator(1000, 'LTP', 20, 1, 1, 5, 1)
#     brain.runSimulation(3, debug=True)
