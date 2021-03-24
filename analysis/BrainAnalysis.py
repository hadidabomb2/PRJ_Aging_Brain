from BrainSimulator import BrainSimulator
from pandas import DataFrame
import matplotlib.pyplot as plt


def getDataFrameGroupedByTimeAndMaximised(values):
    df = DataFrame(values, columns=['Time'])
    df['No_Spiked'] = df.index + 1
    df = df.groupby('Time').max().reset_index()
    return df


def getDataFrameByVm(values):
    values_Vm = [x[0] for x in values]
    values_time = [x[1] for x in values]
    df = DataFrame({"Vm": values_Vm, "Time": values_time})
    return df


def initialiseAndRunBrainSimulation(end_time, learning_type, input_neu_size, output_neu_size,
                                    mem_capacity, synaptic_strength_factor, input_interval, input_strength):
    brain = BrainSimulator(end_time, learning_type, input_neu_size, output_neu_size, mem_capacity,
                           synaptic_strength_factor, input_interval)
    brain.runSimulation(input_strength)
    return brain


def getDataFrameLists(brain_list, list_name, groupingMethod):
    df_list = []
    for brain in brain_list:
        values = getattr(brain, list_name)
        df_list.append(groupingMethod(values))
    return df_list


def runWithDifferentMemoryCapacities(end_time, learning_type, input_neu_size, output_neu_size,
                                     synaptic_strength_factor, input_interval, input_strength, loop_lower_bound=0):
    brain_list = []
    for i in range(100, loop_lower_bound, -20):
        memory_capacity = i / 100
        brain_list.append(initialiseAndRunBrainSimulation(end_time, learning_type, input_neu_size, output_neu_size,
                                                          memory_capacity, synaptic_strength_factor, input_interval,
                                                          input_strength))
    return brain_list


def debugNeuron():
    brain = BrainSimulator(1000, 'LTP', 20, 1, 1, 5, 1)
    brain.runSimulation(3, debug=False)
    d1 = getDataFrameByVm(brain.neural_network.getOutputNeuronList()[0].tracking_Vm)
    brain2 = BrainSimulator(1000, 'LTP', 20, 1, 0.6, 5, 1)
    brain2.runSimulation(3, debug=False)
    d2 = getDataFrameByVm(brain2.neural_network.getOutputNeuronList()[0].tracking_Vm)
    plt.plot(d1['Time'], d1['Vm'], label="LTP - 100% ")
    plt.plot(d2['Time'], d2['Vm'], label="LTP - 60% ")
    # plt.plot(d2['Time'], d2['Vm'], label="LTP - 80% Memory Capacity")
    # plt.plot(d3['Time'], d3['Vm'], label="LTP - 60% Memory Capacity")
    plt.legend(loc="upper right")
    plt.title("Comparing Memory Capacity w/ LTM Mechanisms (LTP & MIS)")
    plt.xlabel("Time (ms)")
    plt.ylabel("No. of Output Nodes Spiked")
    plt.show()


def comparingLearningMechanismBasic(end_time, input_neu_size, output_neu_size, synaptic_strength_factor, input_interval,
                                    input_strength):
    brain_LTP = runWithDifferentMemoryCapacities(end_time, 'LTP', input_neu_size, output_neu_size,
                                                 synaptic_strength_factor, input_interval, input_strength)
    brain_MIS = runWithDifferentMemoryCapacities(end_time, 'MIS', input_neu_size, output_neu_size,
                                                 synaptic_strength_factor, input_interval, input_strength)

    df_LTP = getDataFrameLists(brain_LTP, "learned_times", getDataFrameGroupedByTimeAndMaximised)
    df_MIS = getDataFrameLists(brain_MIS, "learned_times", getDataFrameGroupedByTimeAndMaximised)

    fig = plt.figure(figsize=(15, 7))
    plt.figtext(0.99, 0.01, 'MC stands for Memory Capacity', horizontalalignment='right')
    fig.suptitle("Analysing Learning Times w/ LTM Mechanisms (LTP & MIS)", fontsize=20)
    ax1 = fig.add_subplot(121)
    ax1.title.set_text("Long Term Potentiation")
    ax2 = fig.add_subplot(122)
    ax2.title.set_text("Multi-Innervated Dendritic Spines")
    counter = 0
    for i in range(100, 0, -20):
        ax1.plot(df_LTP[counter]['Time'], df_LTP[counter]['No_Spiked'], label=(str(i) + "% MC"))
        counter += 1
    ax1.legend(loc="upper left")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("No. of Output Nodes Spiked")
    counter = 0
    for i in range(100, 0, -20):
        ax2.plot(df_MIS[counter]['Time'], df_MIS[counter]['No_Spiked'], label=(str(i) + "% MC"))
        counter += 1
    ax2.legend(loc="upper left")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("No. of Output Nodes Spiked")
    plt.show()


def comparingSynapticStrengthBasic(end_time, learning_type, input_neu_size, output_neu_size, input_interval,
                                   input_strength):
    brain_s1 = runWithDifferentMemoryCapacities(end_time, learning_type, input_neu_size, output_neu_size,
                                                6, input_interval, input_strength)
    brain_s2 = runWithDifferentMemoryCapacities(end_time, learning_type, input_neu_size, output_neu_size,
                                                4, input_interval, input_strength)

    df_s1 = getDataFrameLists(brain_s1, "learned_times", getDataFrameGroupedByTimeAndMaximised)
    df_s2 = getDataFrameLists(brain_s2, "learned_times", getDataFrameGroupedByTimeAndMaximised)

    fig = plt.figure(figsize=(15, 7))
    plt.figtext(0.99, 0.01, 'MC stands for Memory Capacity', horizontalalignment='right')
    fig.suptitle("Analysing Learning Times w/ Synaptic Strength (SS)", fontsize=20)
    ax1 = fig.add_subplot(121)
    ax1.title.set_text("Synaptic Strength set to 6")
    ax2 = fig.add_subplot(122)
    ax2.title.set_text("Synaptic Strength set to 4")
    counter = 0
    for i in range(100, 0, -20):
        ax1.plot(df_s1[counter]['Time'], df_s1[counter]['No_Spiked'], label=(str(i) + "% MC"))
        counter += 1
    ax1.legend(loc="upper left")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("No. of Output Nodes Spiked")
    counter = 0
    for i in range(100, 0, -20):
        ax2.plot(df_s2[counter]['Time'], df_s2[counter]['No_Spiked'], label=(str(i) + "% MC"))
        counter += 1
    ax2.legend(loc="upper left")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("No. of Output Nodes Spiked")
    plt.show()


def comparingNeuronAmountBasic(end_time, learning_type, synaptic_strength_factor, input_interval,
                               input_strength):
    brain_n1 = runWithDifferentMemoryCapacities(end_time, learning_type, 50, 50,
                                                synaptic_strength_factor, input_interval, input_strength)
    brain_n2 = runWithDifferentMemoryCapacities(end_time, learning_type, 25, 25,
                                                synaptic_strength_factor, input_interval, input_strength)

    df_n1 = getDataFrameLists(brain_n1, "learned_times", getDataFrameGroupedByTimeAndMaximised)
    df_n2 = getDataFrameLists(brain_n2, "learned_times", getDataFrameGroupedByTimeAndMaximised)

    fig = plt.figure(figsize=(15, 7))
    plt.figtext(0.99, 0.01, 'MC stands for Memory Capacity', horizontalalignment='right')
    fig.suptitle("Analysing Learning Times w/ Neuron Amount", fontsize=20)
    ax1 = fig.add_subplot(121)
    ax1.title.set_text("50 Input & Output Neurons")
    ax2 = fig.add_subplot(122)
    ax2.title.set_text("25 Input & Output Neurons")
    counter = 0
    for i in range(100, 0, -20):
        ax1.plot(df_n1[counter]['Time'], df_n1[counter]['No_Spiked'], label=(str(i) + "% MC"))
        counter += 1
    ax1.legend(loc="upper left")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("No. of Output Nodes Spiked")
    counter = 0
    for i in range(100, 0, -20):
        ax2.plot(df_n2[counter]['Time'], df_n2[counter]['No_Spiked'], label=(str(i) + "% MC"))
        counter += 1
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("No. of Output Nodes Spiked")
    ax2.legend(loc="upper left")
    plt.show()


def comparingMembranePotentialBasic(end_time, learning_type, input_neu_size, synaptic_strength_factor, input_interval,
                                    input_strength):
    loop_lower_bound = 50
    brain_o1 = runWithDifferentMemoryCapacities(end_time, learning_type, input_neu_size, 1, synaptic_strength_factor,
                                                input_interval, input_strength, loop_lower_bound=loop_lower_bound)

    df_o1 = []
    for brain in brain_o1:
        df_o1.append(getDataFrameByVm(brain.neural_network.getOutputNeuronList()[0].tracking_Vm))

    fig = plt.figure(figsize=(15, 7))
    plt.figtext(0.99, .01, 'MC stands for Memory Capacity', horizontalalignment='right')
    fig.suptitle("Analysing Membrane Potential of Output Neuron", fontsize=20)
    ax1 = fig.add_subplot(111)
    counter = 0
    for i in range(100, loop_lower_bound, -20):
        ax1.plot(df_o1[counter]['Time'], df_o1[counter]['Vm'], label=(str(i) + "% MC"))
        counter += 1
    ax1.legend(loc="upper left")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Membrane Voltage of Neuron (mV)")
    plt.show()


if __name__ == '__main__':
    comparingLearningMechanismBasic(200, 50, 50, 5, .025, 5)
    comparingLearningMechanismBasic(20000, 500, 500, 5, .025, 5)
    # comparingSynapticStrengthBasic(300, 'LTP', 50, 50, .025, 5)
    # comparingNeuronAmountBasic(200, 'LTP', 5, .025, 5)
    # comparingMembranePotentialBasic(500, 'LTP', 30, 5, 1, 5)
    print("Ended")
