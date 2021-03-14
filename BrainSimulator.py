import numpy as np
import random
import math
import time as clock
from pandas import DataFrame
import matplotlib.pyplot as plt

from NeuralNetwork import NeuralNetwork


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

    def runSimulation(self, input_interval, input_strength, debug=False):
        timestep = self.timestep
        time = self.time
        network = self.network_structure.network
        simulation_time_steps = self.end_time / timestep
        waiting_time = 0.0
        input_time = input_interval
        chosen_input_node = random.choice(list(network))
        learned_connections = self.learned_connections
        learned_times = self.learned_times

        for i in range(int(simulation_time_steps)):
            time += timestep
            if round(waiting_time, 5) > 0.0:
                waiting_time -= timestep

                if round(waiting_time, 5) <= 0.0:
                    input_time = input_interval
                    chosen_input_node = random.choice(list(network))
                    chosen_input_node.updateProperties(time + timestep)

            else:
                input_time -= timestep
                input_fired = chosen_input_node.processInput(input_strength, time, timestep, debug=debug)

                if input_fired:
                    output_connections = (network[chosen_input_node])
                    for j in range(len(output_connections)):
                        output_connection = output_connections[j]
                        if output_connection not in learned_connections:
                            output_node = output_connection[0]
                            output_node.updateProperties(time)
                            connection_strength = output_connection[1]
                            output_fired = output_node.processInput(connection_strength, time, timestep)
                            if output_fired:
                                if self.learning_type == 'LTP':
                                    self.triggerLTP(output_connection, learned_connections, time, learned_times)
                                else:
                                    if random.randint(0, 10) < 5:
                                        self.triggerMIS(output_connection, learned_connections, output_connections,
                                                        time, learned_times)
                                    else:
                                        self.triggerLTP(output_connection, learned_connections, time, learned_times)

                if round(input_time, 5) <= 0.0:
                    waiting_time = input_interval

            # clock.sleep(0.1)

    def triggerLTP(self, output_connection, learned_connections, time, learned_times):
        output_connection[1] = output_connection[1] * 2
        learned_connections.append(output_connection)
        learned_times.append(time)

    def triggerMIS(self, output_connection, learned_connections, output_connections, time, learned_times):
        possible_connections = [x for x in output_connections if x not in learned_connections]
        if not possible_connections:
            self.triggerLTP(output_connection, learned_connections, time, learned_times)
        else:
            old_connection = random.choice(possible_connections)
            new_connection = [output_connection[0], old_connection[1]]
            output_connections.remove(old_connection)
            output_connections.append(new_connection)
            learned_connections.append(output_connection)
            learned_connections.append(new_connection)
            learned_times.append(time)
