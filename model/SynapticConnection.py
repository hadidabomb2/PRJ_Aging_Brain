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
