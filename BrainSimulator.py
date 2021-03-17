import numpy as np
import random
import math
import time as clock

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

    def runSimulation(self, input_interval, input_strength, debug=False, updateCanvas=None, updateConnections=None):
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
        old_connections = []

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
                    adding_temp = []
                    removing_temp = []
                    for j in range(len(input_connections)):
                        input_connection = input_connections[j]
                        if not ((input_connection in learned_connections) or (input_connection in old_connections)):
                            output_node = input_connection.getOutputNeuron()
                            output_node.updateProperties(time)
                            connection_strength = input_connection.getConnectionStrength()
                            output_fired = output_node.processInput(connection_strength, time, timestep)
                            if output_fired:
                                if self.learning_type == 'LTP':
                                    self.triggerLTP(input_connection, learned_connections, time, learned_times)
                                else:
                                    if random.randint(0, 10) < 10:
                                        input_connections = network_structure.\
                                            getInputNeuronConnections(chosen_input_node)
                                        self.triggerMIS(input_connection, learned_connections, input_connections,
                                                        time, learned_times, old_connections, adding_temp, removing_temp)
                                    else:
                                        self.triggerLTP(input_connection, learned_connections, time, learned_times)

                    if self.learning_type == "MIS":
                        for k in range(len(adding_temp)):
                            self.network_structure.network.append(adding_temp[k])
                            self.network_structure.network.remove(removing_temp[k])
                            updateConnections(new_connection=adding_temp[k], old_connection=removing_temp[k])

                if round(input_time, 5) <= 0.0:
                    waiting_time = input_interval

            if updateCanvas is not None:
                updateCanvas()

    def triggerLTP(self, input_connection, learned_connections, time, learned_times):
        input_connection.connection_strength = input_connection.getConnectionStrength() * 2
        learned_connections.append(input_connection)
        learned_times.append(time)

    def triggerMIS(self, input_connection, learned_connections, input_connections, time, learned_times,
                   old_connections, adding_temp, removing_temp):
        possible_connections = [x for x in input_connections if not ((x in learned_connections)
                                or (x in old_connections) or (x == input_connection))]
        if not possible_connections:
            self.triggerLTP(input_connection, learned_connections, time, learned_times)
        else:
            old_connection = random.choice(possible_connections)
            new_connection = SynapticConnection(input_connection.getInputNeuron(), input_connection.getOutputNeuron(),
                                                old_connection.getConnectionStrength())
            removing_temp.append(old_connection)
            adding_temp.append(new_connection)
            old_connections.append(old_connection)
            learned_connections.append(input_connection)
            learned_connections.append(new_connection)
            learned_times.append(time)
