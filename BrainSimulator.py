import copy

import numpy as np
import random
import math
import time as clock
from pandas import DataFrame
import matplotlib.pyplot as plt

from NeuralNetwork import NeuralNetwork, SynapticConnection


class BrainSimulator:
    def __init__(self, end_time, learning_type, input_neu_size, output_neu_size, mem_capacity,
                 synaptic_strength_factor):
        self.end_time = end_time
        self.time = 0
        self.timestep = 0.0125
        self.learning_type = learning_type
        self.network_structure = NeuralNetwork(input_neu_size, output_neu_size, mem_capacity,
                                               synaptic_strength_factor).getNeuralNetworkStructure()
        self.learned_connections = []
        self.learned_times = []

    def runSimulation(self, input_interval, input_strength, debug=False, callback=None):
        timestep = self.timestep
        time = self.time
        network_structure = self.network_structure
        network = network_structure.getNetwork()
        simulation_time_steps = self.end_time / timestep
        waiting_time = 0.0
        input_time = input_interval
        chosen_input_node = random.choice(list(network)).getInputNeuron()
        learned_connections = self.learned_connections
        learned_times = self.learned_times

        for i in range(int(simulation_time_steps)):
            time += timestep
            if round(waiting_time, 5) > 0.0:
                waiting_time -= timestep

                if round(waiting_time, 5) <= 0.0:
                    input_time = input_interval
                    chosen_input_node = random.choice(list(network)).getInputNeuron()
                    chosen_input_node.updateProperties(time + timestep)

            else:
                input_time -= timestep
                input_fired = chosen_input_node.processInput(input_strength, time, timestep, debug=debug)

                if input_fired:
                    input_connections = network_structure.getInputNeuronConnections(chosen_input_node)
                    for j in range(len(input_connections)):
                        input_connection = input_connections[j]
                        if input_connection not in learned_connections:
                            output_node = input_connection.getOutputNeuron()
                            output_node.updateProperties(time)
                            connection_strength = input_connection.getConnectionStrength()
                            output_fired = output_node.processInput(connection_strength, time, timestep)
                            if output_fired:
                                if self.learning_type == 'LTP':
                                    self.triggerLTP(input_connection, learned_connections, time, learned_times)
                                else:
                                    if random.randint(0, 10) < 5:
                                        self.triggerMIS(input_connection, learned_connections, input_connections,
                                                        time, learned_times)
                                    else:
                                        self.triggerLTP(input_connection, learned_connections, time, learned_times)

                if round(input_time, 5) <= 0.0:
                    waiting_time = input_interval

            if callback is not None:
                callback()


    def triggerLTP(self, input_connection, learned_connections, time, learned_times):
        input_connection.connection_strength = input_connection.getConnectionStrength() * 2
        learned_connections.append(input_connection)
        learned_times.append(time)

    def triggerMIS(self, input_connection, learned_connections, input_connections, time, learned_times):
        possible_connections = [x for x in input_connections if x not in learned_connections]
        if not possible_connections:
            self.triggerLTP(input_connection, learned_connections, time, learned_times)
        else:
            old_connection = random.choice(possible_connections)
            new_connection = SynapticConnection(input_connection.getInputNeuron(), old_connection.getOutputNeuron(),
                                                old_connection.getConnectionStrength())
            self.network_structure.network.remove(old_connection)
            self.network_structure.network.append(new_connection)
            learned_connections.append(input_connection)
            learned_connections.append(new_connection)
            learned_times.append(time)
