import brian2 as b2
import numpy as np
from neurodynex.tools import input_factory
from neurodynex.tools import input_factory, plot_tools
import matplotlib as ply
class expLIF:
    def __init__(self):
        
        b2.defaultclock.dt = 0.05 * b2.ms
        self.time_scale=12.*b2.ms
        self.reset_pot=-60*b2.mV
        self.rest_pot=-65*b2.mV
        self.resistance=20.*b2.Mohm
        self.threshold=-30*b2.mV
        self.rheo_threshold=-55.0*b2.mV
        self.delta_t=2.0*b2.mV
    def simulate(self,current=input_factory.get_zero_current(),time=10*b2.ms,rheo_threshold=None,v_rest=None,v_reset=None,delta_t=None,time_scale=None,resistance=None,threshold=None):
        if(v_rest==None):
            v_rest=self.rest_pot
        if(v_reset==None):
            v_reset=self.reset_pot
        if(rheo_threshold==None):
            rheo_threshold=self.rheo_threshold
        if(delta_t==None):
            delta_t=self.delta_t
        if(time_scale==None):
            time_scale=self.time_scale
        if(resistance==None):
            resistance=self.resistance
        if(threshold==None):
            threshold=self.threshold
        eqs = "dv/dt = (-(v-v_rest) +delta_t*exp((v-rheo_threshold)/delta_t)+ resistance * current(t,i))/(time_scale) : volt"
        neuron = b2.NeuronGroup(1, model=eqs, reset="v=v_reset", threshold="v>threshold", method="euler")
        neuron.v = v_rest 
        voltage_monitor = b2.StateMonitor(neuron, ["v"], record=True)
        spike_monitor = b2.SpikeMonitor(neuron)
        net = b2.Network(neuron, voltage_monitor, spike_monitor)
        net.run(time)
        return voltage_monitor, spike_monitor
lif_neuron=expLIF()
print('7 repetitive spikes : current = 0.8 nA')
input_current = input_factory.get_step_current(t_start=20, t_end=120, unit_time=b2.ms, amplitude=0.8 * b2.namp)
state_monitor, spike_monitor = lif_neuron.simulate(current=input_current,time=200*b2.ms)
plot_tools.plot_voltage_and_current_traces(state_monitor, input_current,title="step current",firing_threshold=lif_neuron.threshold)
print("nr of spikes: {}".format(spike_monitor.count[0]))