import brian2 as b2
import numpy as np
from neurodynex.tools import input_factory
from neurodynex.tools import input_factory, plot_tools
import matplotlib as ply
class adexpLIF:
	def __init__(self):
		b2.defaultclock.dt = 0.01 * b2.ms
		self.time_scale=5*b2.ms #
		self.reset_pot=-51*b2.mV#
		self.rest_pot=-70*b2.mV #
		self.resistance=500*b2.Mohm#
		self.threshold=-30*b2.mV#
		self.rheo_threshold=-50*b2.mV#
		self.delta_t=2.0*b2.mV#
		self.adapt_volt_c=0.5 * b2.nS#
		self.adapt_tau=100.0 * b2.ms#
		self.adapt_incr=7.0 * b2.pA#
	def simulate(self,current=input_factory.get_zero_current(),time=10*b2.ms,rheo_threshold=None,v_rest=None,v_reset=None,delta_t=None,time_scale=None,resistance=None,threshold=None,adapt_volt_c=None,adapt_tau=None,adapt_incr=None):
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
		if(adapt_volt_c==None):
			adapt_volt_c=self.adapt_volt_c
		if(adapt_tau==None):
			adapt_tau=self.adapt_tau
		if(adapt_incr==None):
			adapt_incr=self.adapt_incr
		v_spike_str = "v>{:f}*mvolt".format(threshold / b2.mvolt)
		eqs = """
  			dv/dt = (-(v-v_rest) +delta_t*exp((v-rheo_threshold)/delta_t)+ resistance * current(t,i) - resistance * w)/(time_scale) : volt
        	dw/dt=(adapt_volt_c*(v-v_rest)-w)/adapt_tau : amp
        	"""
		neuron = b2.NeuronGroup(1, model=eqs, threshold=v_spike_str, reset="v=v_reset;w+=adapt_incr", method="euler")
		neuron.v = v_rest
		neuron.w = 0.0 * b2.pA
		state_monitor = b2.StateMonitor(neuron, ["v", "w"], record=True)
		spike_monitor = b2.SpikeMonitor(neuron)
		b2.run(time)
		return state_monitor, spike_monitor
lif_neuron=adexpLIF()

current = input_factory.get_step_current(10, 250, 1. * b2.ms, 30.0 * b2.pA)
state_monitor, spike_monitor = lif_neuron.simulate(current=current, time=400 * b2.ms)
plot_tools.plot_voltage_and_current_traces(state_monitor, current)
print('No  spike : current=30pA')
print("nr of spikes: {}".format(spike_monitor.count[0]))