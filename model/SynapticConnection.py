# A class that represents a synaptic connection in our simulation. It stored the values of the input neuron it is
# connected from, the output neuron it is connected to and the strength/weight of the connection. Making the connection
# an object itself allows us to make further specific changes to the synaptic connection in the future and also makes
# representing a connection in the GUI easier.
class SynapticConnection:
    def __init__(self, input_neuron, output_neuron, connection_strength):
        self.input_neuron = input_neuron
        self.output_neuron = output_neuron
        self.connection_strength = connection_strength
        # This factor is the amount to increase the connection strength by if strengthenConnection(...) is called.
        # It can be modified in the future for different research projects or deeper analysis but is arbitrarily
        # assigned the value 3 for now because it is not relevant for my research.
        self.strengthen_factor = 3

    def getInputNeuron(self):
        return self.input_neuron

    def getOutputNeuron(self):
        return self.output_neuron

    def getConnectionStrength(self):
        return self.connection_strength

    # Increases the strength of the connection by the strengthen factor.
    def strengthenConnection(self):
        self.connection_strength = self.getConnectionStrength() * self.strengthen_factor
