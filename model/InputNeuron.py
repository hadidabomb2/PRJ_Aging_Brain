from model.Neuron import Neuron


class InputNeuron(Neuron):
    def __init__(self):
        super().__init__()

    # Called once on output neurons when current is about to be supplied to them
    def updateProperties(self, sim_time):
        super().updateProperties(sim_time)

    # Called on every time step of the simulation on the neuron that's being supplied
    # an input
    def processInput(self, current_strength, sim_time, sim_time_step, debug=False, fired=False):
        return super().processInput(current_strength, sim_time, sim_time_step, debug=debug, fired=fired)
