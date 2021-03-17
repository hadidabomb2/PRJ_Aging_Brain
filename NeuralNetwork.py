import numpy as np
import random
import math

from InputNeuron import InputNeuron
from OutputNeuron import OutputNeuron


class SynapticConnection:
    def __init__(self, input_neuron, output_neuron, connection_strength):
        self.input_neuron = input_neuron
        self.output_neuron = output_neuron
        self.connection_strength = connection_strength

    def getInputNeuron(self):
        return self.input_neuron

    def getOutputNeuron(self):
        return self.output_neuron

    def getConnectionStrength(self):
        return self.connection_strength


class NeuralNetworkDataStructure:
    def __init__(self, input_neu_size, output_neu_size):
        self.network = []
        self.input_neurons = [InputNeuron() for i in range(input_neu_size)]
        self.output_neurons = [OutputNeuron() for i in range(output_neu_size)]

    def getInputNeuronsList(self):
        return self.input_neurons

    def getOutputNeuronList(self):
        return self.output_neurons

    def addToNetwork(self, input_neuron, output_neuron, connection_strength):
        connection = SynapticConnection(input_neuron, output_neuron, connection_strength)
        network = self.network
        if connection not in network:
            network.append(connection)

    def getInputNeuronConnections(self, input_neuron):
        network = self.getNetwork()
        return [connection for connection in network if connection.getInputNeuron() == input_neuron]

    def getNetwork(self):
        return self.network


class NeuralNetwork:
    def __init__(self, input_neu_size, output_neu_size, mem_capacity, synaptic_strength_factor):
        self.synaptic_strength_factor = synaptic_strength_factor
        connections_per_neu = round(mem_capacity * output_neu_size)
        initial_neu_network = NeuralNetworkDataStructure(input_neu_size, output_neu_size)
        input_neurons = initial_neu_network.getInputNeuronsList()[:]
        output_neurons = initial_neu_network.getOutputNeuronList()[:]
        self.generateNeuralNetwork(initial_neu_network, input_neurons, output_neurons, connections_per_neu)
        self.network_structure = initial_neu_network

    def generateNeuralNetwork(self, initial_neu_network, input_neurons, output_neurons, connections_per_neu):
        all_weights_dist = self.generateSynapticWeights(len(input_neurons), len(output_neurons))
        for input_neu_idx in range(len(input_neurons)):
            weights_dist = all_weights_dist[input_neu_idx].tolist()
            output_neurons_temp = output_neurons[:]
            for i in range(connections_per_neu):
                random_output_neuron = random.choice(output_neurons_temp)
                random_weight = random.choice(weights_dist)
                output_neurons_temp.remove(random_output_neuron)
                weights_dist.remove(random_weight)
                initial_neu_network.addToNetwork(input_neurons[input_neu_idx], random_output_neuron, random_weight)

    def generateSynapticWeights(self, input_neu_size, output_neu_size):
        dirichlet_dist = np.random.dirichlet(np.ones(output_neu_size) * 100)
        return np.random.multinomial(output_neu_size * self.synaptic_strength_factor, dirichlet_dist,
                                     size=input_neu_size)

    def getNeuralNetworkStructure(self):
        return self.network_structure
