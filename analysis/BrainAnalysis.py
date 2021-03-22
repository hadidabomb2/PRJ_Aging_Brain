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
    print(values_Vm)
    values_time = [x[1] for x in values]
    df = DataFrame({"Vm": values_Vm, "Time": values_time})
    # print(df)
    return df


def initialiseAndRunBrainSimulation(end_time, learning_type, input_neu_size, output_neu_size,
                                    mem_capacity, synaptic_strength_factor, input_interval, input_strength):
    brain = BrainSimulator(end_time, learning_type, input_neu_size, output_neu_size, mem_capacity,
                           synaptic_strength_factor)
    brain.runSimulation(input_interval, input_strength)
    return brain


def debugNeuron():
    brain = BrainSimulator(1000, 'LTP', 10, 1, 1, 5)
    brain.runSimulation(.05, 3, debug=False)
    d1 = getDataFrameByVm(brain.network_structure.getOutputNeuronList()[0].tracking_Vm)
    # d2 = getDataFrameByVm(brain.network_structure.getOutputNeuronList()[1].tracking_Vm)
    # d3 = getDataFrameByVm(brain.network_structure.getInputNeuronsList()[2].tracking_Vm)
    plt.plot(d1['Time'], d1['Vm'], label="LTP - 100% Memory Capacity")
    # plt.plot(d2['Time'], d2['Vm'], label="LTP - 80% Memory Capacity")
    # plt.plot(d3['Time'], d3['Vm'], label="LTP - 60% Memory Capacity")
    plt.legend(loc="upper left")
    plt.title("Comparing Memory Capacity w/ LTM Mechanisms (LTP & MIS)")
    plt.xlabel("Time (ms)")
    plt.ylabel("No. of Output Nodes Spiked")
    plt.show()


def comparingMemoryMechanismBasic(end_time, input_neu_size, output_neu_size, synaptic_strength_factor, input_interval,
                                  input_strength):
    brain_LTP_m1 = initialiseAndRunBrainSimulation(end_time, 'LTP', input_neu_size, output_neu_size, 1,
                                                   synaptic_strength_factor, input_interval, input_strength)
    df_LTP_m1 = getDataFrameGroupedByTimeAndMaximised(brain_LTP_m1.learned_times)
    brain_LTP_m2 = initialiseAndRunBrainSimulation(end_time, 'LTP', input_neu_size, output_neu_size, .8,
                                                   synaptic_strength_factor, input_interval, input_strength)
    df_LTP_m2 = getDataFrameGroupedByTimeAndMaximised(brain_LTP_m2.learned_times)
    brain_LTP_m3 = initialiseAndRunBrainSimulation(end_time, 'LTP', input_neu_size, output_neu_size, .6,
                                                   synaptic_strength_factor, input_interval, input_strength)
    df_LTP_m3 = getDataFrameGroupedByTimeAndMaximised(brain_LTP_m3.learned_times)

    brain_MIS_m1 = initialiseAndRunBrainSimulation(end_time, 'MIS', input_neu_size, output_neu_size, 1,
                                                   synaptic_strength_factor, input_interval, input_strength)
    df_MIS_m1 = getDataFrameGroupedByTimeAndMaximised(brain_MIS_m1.learned_times)
    brain_MIS_m2 = initialiseAndRunBrainSimulation(end_time, 'MIS', input_neu_size, output_neu_size, .8,
                                                   synaptic_strength_factor, input_interval, input_strength)
    df_MIS_m2 = getDataFrameGroupedByTimeAndMaximised(brain_MIS_m2.learned_times)
    brain_MIS_m3 = initialiseAndRunBrainSimulation(end_time, 'MIS', input_neu_size, output_neu_size, .6,
                                                   synaptic_strength_factor, input_interval, input_strength)
    df_MIS_m3 = getDataFrameGroupedByTimeAndMaximised(brain_MIS_m3.learned_times)

    fig = plt.figure(figsize=(15, 7))
    fig.suptitle("Comparing Memory Capacity w/ LTM Mechanisms (LTP & MIS)", fontsize=20)
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.plot(df_LTP_m1['Time'], df_LTP_m1['No_Spiked'], label="LTP - 100% Memory Capacity")
    ax1.plot(df_LTP_m2['Time'], df_LTP_m2['No_Spiked'], label="LTP - 80% Memory Capacity")
    ax1.plot(df_LTP_m3['Time'], df_LTP_m3['No_Spiked'], label="LTP - 60% Memory Capacity")
    ax1.legend(loc="upper left")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("No. of Output Nodes Spiked")
    ax2.plot(df_MIS_m1['Time'], df_MIS_m1['No_Spiked'], label="MIS - 100% Memory Capacity")
    ax2.plot(df_MIS_m2['Time'], df_MIS_m2['No_Spiked'], label="MIS - 80% Memory Capacity")
    ax2.plot(df_MIS_m3['Time'], df_MIS_m3['No_Spiked'], label="MIS - 60% Memory Capacity")
    ax2.legend(loc="upper left")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("No. of Output Nodes Spiked")
    plt.show()
    # print(np.interp(80, df_LTP_m1['Time'], df_LTP_m1['No_Spiked']))
    # print(np.interp(80, df_MIS_m3['Time'], df_MIS_m3['No_Spiked']))


def comparingSynapticStrengthBasic(end_time, learning_type, input_neu_size, output_neu_size, input_interval,
                                   input_strength):
    brain_s1_m1 = initialiseAndRunBrainSimulation(end_time, learning_type, input_neu_size, output_neu_size, 1, 6,
                                                  input_interval, input_strength)
    df_s1_m1 = getDataFrameGroupedByTimeAndMaximised(brain_s1_m1.learned_times)
    brain_s1_m2 = initialiseAndRunBrainSimulation(end_time, learning_type, input_neu_size, output_neu_size, .8, 6,
                                                  input_interval, input_strength)
    df_s1_m2 = getDataFrameGroupedByTimeAndMaximised(brain_s1_m2.learned_times)
    brain_s1_m3 = initialiseAndRunBrainSimulation(end_time, learning_type, input_neu_size, output_neu_size, .6, 6,
                                                  input_interval, input_strength)
    df_s1_m3 = getDataFrameGroupedByTimeAndMaximised(brain_s1_m3.learned_times)

    brain_s2_m1 = initialiseAndRunBrainSimulation(end_time, learning_type, input_neu_size, output_neu_size, 1, 4,
                                                  input_interval, input_strength)
    df_s2_m1 = getDataFrameGroupedByTimeAndMaximised(brain_s2_m1.learned_times)
    brain_s2_m2 = initialiseAndRunBrainSimulation(end_time, learning_type, input_neu_size, output_neu_size, .8, 4,
                                                  input_interval, input_strength)
    df_s2_m2 = getDataFrameGroupedByTimeAndMaximised(brain_s2_m2.learned_times)
    brain_s2_m3 = initialiseAndRunBrainSimulation(end_time, learning_type, input_neu_size, output_neu_size, .6, 4,
                                                  input_interval, input_strength)
    df_s2_m3 = getDataFrameGroupedByTimeAndMaximised(brain_s2_m3.learned_times)

    fig = plt.figure(figsize=(15, 7))
    fig.suptitle("Comparing Memory Capacity w/ Synaptic Strength (SS)", fontsize=20)
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.plot(df_s1_m1['Time'], df_s1_m1['No_Spiked'], label="SS 6 - 100%")
    ax1.plot(df_s1_m2['Time'], df_s1_m2['No_Spiked'], label="SS 6 - 80%")
    ax1.plot(df_s1_m3['Time'], df_s1_m3['No_Spiked'], label="SS 6 - 60%")
    ax1.legend(loc="upper left")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("No. of Output Nodes Spiked")
    ax2.plot(df_s2_m1['Time'], df_s2_m1['No_Spiked'], label="SS 4 - 100%")
    ax2.plot(df_s2_m2['Time'], df_s2_m2['No_Spiked'], label="SS 4 - 80%")
    ax2.plot(df_s2_m3['Time'], df_s2_m3['No_Spiked'], label="SS 4 - 60%")
    ax2.legend(loc="upper left")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("No. of Output Nodes Spiked")
    plt.show()


def comparingInputAmountNeurons(end_time, learning_type, synaptic_strength_factor, input_interval,
                                input_strength):
    brain_n1_m1 = initialiseAndRunBrainSimulation(end_time, learning_type, 50, 50, 1, synaptic_strength_factor,
                                                  input_interval, input_strength)
    df_n1_m1 = getDataFrameGroupedByTimeAndMaximised(brain_n1_m1.learned_times)
    brain_n1_m2 = initialiseAndRunBrainSimulation(end_time, learning_type, 50, 50, 0.8, synaptic_strength_factor,
                                                  input_interval, input_strength)
    df_n1_m2 = getDataFrameGroupedByTimeAndMaximised(brain_n1_m2.learned_times)
    brain_n1_m3 = initialiseAndRunBrainSimulation(end_time, learning_type, 50, 50, 0.6, synaptic_strength_factor,
                                                  input_interval, input_strength)
    df_n1_m3 = getDataFrameGroupedByTimeAndMaximised(brain_n1_m3.learned_times)

    brain_n2_m1 = initialiseAndRunBrainSimulation(end_time, learning_type, 25, 25, 1, synaptic_strength_factor,
                                                  input_interval, input_strength)
    df_n2_m1 = getDataFrameGroupedByTimeAndMaximised(brain_n2_m1.learned_times)
    brain_n2_m2 = initialiseAndRunBrainSimulation(end_time, learning_type, 25, 25, 0.8, synaptic_strength_factor,
                                                  input_interval, input_strength)
    df_n2_m2 = getDataFrameGroupedByTimeAndMaximised(brain_n2_m2.learned_times)
    brain_n2_m3 = initialiseAndRunBrainSimulation(end_time, learning_type, 25, 25, 0.6, synaptic_strength_factor,
                                                  input_interval, input_strength)
    df_n2_m3 = getDataFrameGroupedByTimeAndMaximised(brain_n2_m3.learned_times)

    fig = plt.figure(figsize=(15, 7))
    fig.suptitle("Comparing Memory Capacity w/ Neuron Amount", fontsize=20)
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.plot(df_n1_m1['Time'], df_n1_m1['No_Spiked'], label="I/O 20 - 100%")
    ax1.plot(df_n1_m2['Time'], df_n1_m2['No_Spiked'], label="I/O 20 - 80%")
    ax1.plot(df_n1_m3['Time'], df_n1_m3['No_Spiked'], label="I/O 20 - 60%")
    ax1.legend(loc="upper left")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("No. of Output Nodes Spiked")
    ax2.plot(df_n2_m1['Time'], df_n2_m1['No_Spiked'], label="I/O 10 - 100%")
    ax2.plot(df_n2_m2['Time'], df_n2_m2['No_Spiked'], label="I/O 10 - 80%")
    ax2.plot(df_n2_m3['Time'], df_n2_m3['No_Spiked'], label="I/O 10 - 60%")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("No. of Output Nodes Spiked")
    ax2.legend(loc="upper left")
    plt.show()


if __name__ == '__main__':
    comparingMemoryMechanismBasic(100, 50, 50, 5, .025, 5)
    comparingSynapticStrengthBasic(100, 'LTP', 50, 50, .025, 5)
    comparingInputAmountNeurons(100, 'LTP', 5, .025, 5)
    # comparingMemoryCapacityBasic('LTP')
    # comparingMemoryCapacityBasic('MIS')
    # comparingSynapticStrengthBasic('LTP')
    # comparingSynapticStrengthBasic('MIS')
    # comparingInputNeuronAmountBasic('LTP')
    # comparingInputNeuronAmountBasic('MIS')
    # comparingOutputNeuronAmountBasic('LTP')
    # comparingOutputNeuronAmountBasic('MIS')
    # comparingOutputNeuronAmountBasic('LTP')
    # comparingOutputNeuronAmountBasic('MIS')
    # debugNeuron()
    print("Ended")
