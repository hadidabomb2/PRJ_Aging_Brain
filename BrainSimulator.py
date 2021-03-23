import random
from model.NeuralNetwork import NeuralNetwork, SynapticConnection


# This class is responsible for running the simulation. It consists of majority of the logic that runs the simulation
# and keeps track of important simulation variables to be passed to the elements in the model folder.
class BrainSimulator:
    def __init__(self, end_time, learning_type, input_neu_size, output_neu_size, mem_capacity,
                 synaptic_strength_factor):
        self.end_time = end_time  # The end time of the simulation (ms)
        self.time = 0  # The starting time of the simulation (ms)
        self.timestep = 0.0125  # The timestep of our simulation (ms)
        self.learning_type = learning_type  # The learning type could be either 'LTP' or 'MIS'
        self.waiting_time = 0.0  # The time to wait before the input current can be supplied to a neuron again
        self.neural_network = NeuralNetwork(input_neu_size, output_neu_size, mem_capacity,
                                            synaptic_strength_factor).getNeuralNetwork()
        # Important lists to keep track of learned connections, times learning has been undertaken and old connections
        # that have been removed from the network.
        self.learned_connections = []
        self.learned_times = []
        self.old_connections = []
        # Boolean which determines if the simulation should keep running
        self.running = False
        # A global reference to the input neuron that is chosen at every input interval
        self.chosen_input_neuron = None

    def runSimulation(self, input_interval, input_strength, debug=False, updateCanvas=None, updateConnections=None):
        # Simulation initialisation of starting variables
        timestep = self.timestep
        neural_network = self.neural_network
        connections = neural_network.getConnections()
        waiting_time = self.waiting_time
        learned_connections = self.learned_connections
        learned_times = self.learned_times
        old_connections = self.old_connections
        learning_type = self.learning_type
        # Create temporary lists that hold which neurons have to be added or removed. This is only
        # relevant with the learning type is 'MIS' but is defined here once because of possible compilation errors.
        adding_temp = []
        removing_temp = []
        # The number of steps in the simulation
        no_steps = self.end_time / timestep
        # An input neuron is chosen by random
        self.chosen_input_neuron = random.choice(list(connections)).getInputNeuron()
        input_time = input_interval

        # Start the simulation
        self.running = True
        for i in range(int(no_steps)):
            if not self.running:
                # Stop the simulation
                break

            self.time += timestep
            # It is rounded to 5 decimal places because floats can become infinitely closer to 0 and not actually
            # equal 0. This stops numbers like 0.0000000001 to not be counted as 0 when they practically are.
            # If there is waiting time, then deduct a timestep from the waiting time. Otherwise, deduct a timestep
            # from the input time.
            if round(waiting_time, 5) > 0.0:
                waiting_time -= timestep

                # If the waiting time is now less or equal to 0 after the deducted timestep, that means the simulation
                # will supply a current in the next round. In this case, randomly choose an input node to supply
                # current to for the next round, update it's properties based off the next rounds time and update the
                # time the input current should run for.
                if round(waiting_time, 5) <= 0.0:
                    self.chosen_input_neuron = random.choice(list(connections)).getInputNeuron()
                    self.chosen_input_neuron.updateProperties(self.time + timestep)
                    input_time = input_interval

            else:
                input_time -= timestep
                # Supplying current to the chosen input neuron and recording if it has been fired or not.
                input_fired = self.chosen_input_neuron.processInput(input_strength, self.time, timestep, debug=debug)

                # If it has been fired, then cycle through the output neurons that have a connection with
                # the fired input neuron, update their properties and supply a current to them based off their
                # respective connection strengths.
                if input_fired:
                    input_connections = neural_network.getInputNeuronConnections(self.chosen_input_neuron)
                    for j in range(len(input_connections)):
                        input_connection = input_connections[j]
                        # If the current connection that is being processed is already a learned connection or an
                        # old connection, then skip it. This is because in our simulation, we are not interested in
                        # strengthening already strengthened/learned connections. As for old connections,
                        # there's a possibility that because of MIS, a connection in the list of input connections
                        # gets removed and does not exist anymore.
                        if not ((input_connection in learned_connections) or (input_connection in old_connections)):
                            output_neuron = input_connection.getOutputNeuron()
                            output_neuron.updateProperties(self.time)
                            connection_strength = input_connection.getConnectionStrength()
                            # Record if output neuron has been fired.
                            output_fired = output_neuron.processInput(connection_strength, self.time, timestep)
                            if output_fired:
                                if learning_type == 'MIS':
                                    # Total LTP inhibition is almost never the case, normally, MIS just becomes more
                                    # common. Therefore, it would be more accurate to trigger MIS based of a random
                                    # probability instead of always triggering MIS. However, just to stress on the
                                    # impact of MIS and minimize the magnitude of randomness and variance in our
                                    # results, we made it so it always triggers if the learning type is 'MIS'.
                                    self.triggerMIS(input_connection, learned_connections, input_connections,
                                                    self.time, learned_times, old_connections, adding_temp,
                                                    removing_temp)
                                else:
                                    self.triggerLTP(input_connection, learned_connections, self.time, learned_times)

                    # Because editing the list of input connections while iterating through it is a bad practice
                    # that can lead to many bugs, we are adding and removing all the connections that need to be added
                    # and removed from the network after the loop ends.
                    if learning_type == "MIS":
                        for k in range(len(adding_temp)):
                            new_connection = adding_temp[k]
                            old_connection = removing_temp[k]
                            neural_network.addConnectionToNetwork(new_connection)
                            neural_network.removeConnectionFromNetwork(old_connection)
                            # Callback to the GUI to display the newly added and removed connections.
                            if updateConnections is not None:
                                updateConnections(new_connection=new_connection, old_connection=old_connection)
                        # Reinitialise the temporary lists
                        adding_temp = []
                        removing_temp = []

                # If input time is now less than 0, that means the simulation should wait in the next round so the
                # waiting_time is updated.
                if round(input_time, 5) <= 0.0:
                    waiting_time = input_interval
                    self.chosen_input_neuron = None

            # Callback to the GUI to correctly highlight learned and unlearned connections in this round.
            if updateCanvas is not None:
                updateCanvas()

    # In LTP, the weight of the connection (connection strength) is increased and the connection is added to the list
    # of learned connections. The list of learned times is also appropriately updated.
    def triggerLTP(self, input_connection, learned_connections, time, learned_times):
        input_connection.strengthenConnection()
        learned_connections.append(input_connection)
        learned_times.append(time)

    # In MIS, the synaptic density is increased between two neurons. It does this by looking at the other neurons
    # the input neuron is connected to, and 'rewiring' another connection to a different output neuron to the output
    # neuron who's synaptic density is to be increased. It would be more accurate to implement an actual measure of
    # distance between neurons and use the closest neuron to rewire it to but for the sake of simplicity, this is
    # more than sufficient.
    def triggerMIS(self, input_connection, learned_connections, input_connections, time, learned_times,
                   old_connections, adding_temp, removing_temp):
        # Get a list of possible connections that can be removed from the network. These are any input connections that
        # have not gone through learning, have not become old connections and are not the part of the connection itself
        # that needs to be 'strengthened'.
        possible_connections = [connection for connection in input_connections if not (
                (connection in learned_connections)
                or (connection in old_connections)
                or (connection == input_connection))]

        # If there are no possible connections, simply undergo LTP. It is possible to simply ignore the learning and
        # say that connection cannot be learned, but it can be argued it is better to make it undergo some sort of
        # learning because it would be already highly unlikely for the simulation to reach this point in the first
        # place so it would possibly allow for some sort of activity at the end of a long simulation.
        if not possible_connections:
            self.triggerLTP(input_connection, learned_connections, time, learned_times)
        else:
            # Choose a random connection out of the list of possible connections to 'rewire' and create an
            # appropriate new connection.
            old_connection = random.choice(possible_connections)
            new_connection = SynapticConnection(input_connection.getInputNeuron(), input_connection.getOutputNeuron(),
                                                old_connection.getConnectionStrength())
            # Update the appropriate lists with the appropriate connections to later be handled by the main
            # runSimulation(...) function.
            removing_temp.append(old_connection)
            old_connections.append(old_connection)
            adding_temp.append(new_connection)
            learned_connections.append(new_connection)
            learned_connections.append(input_connection)
            learned_times.append(time)
