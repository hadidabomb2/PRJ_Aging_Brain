# https://stackoverflow.com/questions/59148994/how-to-get-n-random-integer-numbers-whose-sum-is-equal-to-m

import numpy as np
import random
from model.InputNeuron import InputNeuron
from model.OutputNeuron import OutputNeuron
from model.SynapticConnection import SynapticConnection


# A simple data structure specifically designed for the neural network class underneath. This allows for efficient
# data handling and management within our simulation.
class NeuralNetworkDataStructure:
    def __init__(self, input_neu_size, output_neu_size):
        self.connections = []
        # Makes a list of size input_neu_size containing InputNeuron objects
        self.input_neurons = [InputNeuron() for i in range(input_neu_size)]
        # Makes a list of size output_neu_size containing OutputNeuron objects
        self.output_neurons = [OutputNeuron() for i in range(output_neu_size)]

    # Return the list of input neurons
    def getInputNeuronsList(self):
        return self.input_neurons

    # Return the list of output neurons
    def getOutputNeuronList(self):
        return self.output_neurons

    # Takes in an input neuron, an output neuron and a number representing the strength of the connection. Makes a
    # synaptic connection with those parameters and adds it to the list of connections if the connection has not been
    # already added.
    def addToNetwork(self, input_neuron, output_neuron, connection_strength):
        connection = SynapticConnection(input_neuron, output_neuron, connection_strength)
        connections = self.getConnections()
        if connection not in connections:
            connections.append(connection)

    # Same as the method above but takes in a connection directly. This method is only used when the learning type is
    # MIS and a connection needs to be added mid simulation.
    def addConnectionToNetwork(self, connection):
        connections = self.getConnections()
        if connection not in connections:
            connections.append(connection)

    # Removes a connection from the list of connections if it exists. This method is also only used when the learning
    # type is MIS but when a connection needs to be removed mid simulation instead.
    def removeConnectionFromNetwork(self, connection):
        connections = self.getConnections()
        if connection in connections:
            connections.remove(connection)

    # Returns a list of all connections that start from the input neuron specified (passed by parameters).
    def getInputNeuronConnections(self, input_neuron):
        connections = self.getConnections()
        return [connection for connection in connections if connection.getInputNeuron() == input_neuron]

    # Returns the list of connections.
    def getConnections(self):
        return self.connections


# The neural network that represents a neural network using the data structure defined above and further logic.
class NeuralNetwork:
    def __init__(self, input_neu_size, output_neu_size, mem_capacity, synaptic_strength_factor):
        # The synaptic strength factor represents the mean of the connection weights
        self.synaptic_strength_factor = synaptic_strength_factor
        # Calculate the connections per input neuron and round it as we can only have an integer amount of connections
        connections_per_neu = round(mem_capacity * output_neu_size)
        # Generate the initial neural network
        initial_neu_network = NeuralNetworkDataStructure(input_neu_size, output_neu_size)
        # Using [:] after a list creates a shallow copy of the list so any changes we make to this network in methods
        # defined outside of the neural network data structure do not have an actual effect on the neural network.
        # In this case, we only use these lists to iterate and make getter calls so it is not actually necessary here,
        # just for safety in the future.
        input_neurons = initial_neu_network.getInputNeuronsList()[:]
        output_neurons = initial_neu_network.getOutputNeuronList()[:]
        self.neural_network = self.generateNeuralNetwork(initial_neu_network, input_neurons, output_neurons,
                                                         connections_per_neu)

    # Generate the connection weights and use them to populate the neural network then return the populated network.
    def generateNeuralNetwork(self, neural_network, input_neurons, output_neurons, connections_per_neu):
        # A multinomial distribution of all the weights that will be used for defining connection weights.
        all_weights_dist = self.generateSynapticWeights(len(input_neurons), len(output_neurons))
        for input_neu_idx in range(len(input_neurons)):
            weights_dist = all_weights_dist[input_neu_idx].tolist()
            output_neurons_temp = output_neurons[:]
            for i in range(connections_per_neu):
                # Randomly select an output neuron and a connection weight and use these variables to add a connection
                # to the network. If it was not randomly chosen but rather iteratively, then in the case the memory
                # capacity is less than 100%, the output neurons at the bottom of the network would never have any
                # connections leading to it.
                random_output_neuron = random.choice(output_neurons_temp)
                random_weight = random.choice(weights_dist)
                output_neurons_temp.remove(random_output_neuron)
                weights_dist.remove(random_weight)
                neural_network.addToNetwork(input_neurons[input_neu_idx], random_output_neuron, random_weight)
        return neural_network

    # Generate and returns an array of "input neuron size" by "output neuron size" filled with random values
    # that vary around the synaptic strength factor.
    def generateSynapticWeights(self, input_neu_size, output_neu_size):
        # The array of ones is multiplied by a very large number to cause the bins to approach a Poisson distribution
        # with a mean of self.synaptic_strength_factor.
        dirichlet_dist = np.random.dirichlet(np.ones(output_neu_size) * 1000)
        return np.random.multinomial(output_neu_size * self.synaptic_strength_factor, dirichlet_dist,
                                     size=input_neu_size)

    # Return the neural network
    def getNeuralNetwork(self):
        return self.neural_network


if __name__ == '__main__':
    NeuralNetwork(30, 30, 1, 5)
