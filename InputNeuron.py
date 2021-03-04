"""
Create a basic LIF neuron class
Based on http://neurdon.wpengine.com/2011/01/19/neural-modeling-with-python-part-1/
- Some changes to the original model:
- This class models the state of the neuron over time
- The values have been modified to make the simulation work better (not based on any biological plausability)
- Debugging has been added
Requires Python 3.x and Numpy
"""
import numpy as np
import random
import math


class InputNeuron:
    def __init__(self):
        self.tau_ref = random.uniform(3, 4)  # Average neuronal refractory period (ms)
        self.resting_Vm = 0  # Neuron resting membrane potential (mV)
        self.Rm = 10  # Specific membrane resistivity (k*omega*cm2)
        self.Cm = random.uniform(0.84, 1)  # Specific membrane capacitance (*mu*F/cm2)
        self.tau_m = self.Rm * self.Cm  # Time constant (ms)
        self.Vth = 15  # Neuron membrane threshold potential (mV)

        self.Vm = self.resting_Vm  # Neuron membrane potential (mV)
        self.t_ref = 0  # Neuron refractory time left (ms)
        self.t = 0  # Neuron last updated time (ms)
        self.firedArray = []

    # Called once on all input neurons when current is about to be supplied to them
    def updateProperties(self, sim_time):
        delta_time = sim_time - self.t  # Time passed since last update
        self.Vm = self.Vm * math.exp(-delta_time / self.tau_m)  # Update new membrane potential
        self.t_ref -= delta_time  # Update refractory time left yet
        self.t = sim_time  # Update last updated time

    # Called on every time step of the simulation on the neuron that's being supplied
    # an input
    def processInput(self, input_current, sim_time, sim_time_step, fired=False):
        self.t = sim_time
        # Check if during refractory period
        if self.t_ref > 0:
            self.t_ref -= sim_time_step
        else:
            self.Vm += (-self.Vm + self.Rm * input_current) / self.tau_m
            # Check if membrane potential is higher than threshold potential
            if self.Vm >= self.Vth:
                # Fire neuron spike
                fired = True
                self.t_ref = self.tau_ref
                self.Vm = self.resting_Vm
                self.firedArray.append(self.t)
        return fired


# if __name__ == '__main__':
#     n = InputNeuron()
#     n.updateProperties(1)
#     n.processInput(20, 1, 0.0125)
#     n.updateProperties(4.5)
#     print(n.processInput(20, 6, 0.0125), n.firedArray, n.Vm)
