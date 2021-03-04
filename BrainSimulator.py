import numpy as np
import random
import math
import time as clock
from threading import Thread
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

    def runSimulation(self, input_interval, input_strength):
        timestep = self.timestep
        time = self.time
        network = self.network_structure.network
        simulation_time_steps = self.end_time / timestep
        waiting_time = 0.0
        input_time = input_interval
        chosen_input_node = random.choice(list(network))
        learned_connections = self.learned_connections

        for i in range(int(simulation_time_steps)):
            if round(waiting_time, 5) > 0.0:
                time += timestep
                waiting_time -= timestep

                if round(waiting_time, 5) <= 0.0:
                    input_time = input_interval
                    chosen_input_node = random.choice(list(network))
                    chosen_input_node.updateProperties(time + timestep)

            else:
                time += timestep
                input_time -= timestep
                input_fired = chosen_input_node.processInput(input_strength, time, timestep)

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
                                    self.triggerLTP(output_connection, learned_connections)
                                else:
                                    if random.randint(0, 10) < 5:
                                        self.triggerMIS(output_connection, learned_connections, output_connections)
                                    else:
                                        self.triggerLTP(output_connection, learned_connections)

                if round(input_time, 5) <= 0.0:
                    waiting_time = input_interval

            # clock.sleep(0.1)

    def triggerLTP(self, output_connection, learned_connections):
        output_connection[1] = output_connection[1] * 2
        learned_connections.append(output_connection)

    def triggerMIS(self, output_connection, learned_connections, output_connections):
        possible_connections = [x for x in output_connections if x not in learned_connections]
        if not possible_connections:
            self.triggerLTP(output_connection, learned_connections)
        else:
            old_connection = random.choice(possible_connections)
            new_connection = [output_connection[0], old_connection[1]]
            output_connections.remove(old_connection)
            output_connections.append(new_connection)
            learned_connections.append(output_connection)
            learned_connections.append(new_connection)


if __name__ == '__main__':
    brain = BrainSimulator(20, 'MIS', 20, 20, .8, 5)
    brain.runSimulation(.1, 40)
    print(len(brain.learned_connections))
    # x = [x for x in range(10)]
    # y = [y for y in range(10)]
    # print([z for z in x if z not in y])
