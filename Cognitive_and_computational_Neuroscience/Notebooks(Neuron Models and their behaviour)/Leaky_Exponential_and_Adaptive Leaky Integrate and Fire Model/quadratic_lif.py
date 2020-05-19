from brian2 import *
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

C = 1500*pF #checked for values : 500, 600, 700, 800, 900, 1200, 2000 SPIKES GET LESS FREQUENT.
EL = -70*mV
VT = -60*mV
Vr = -50*mV
Vcut = 40*mV
a = 5*nS/mV
input_current = 550*pA
t_simulation = 160*ms
spike_bins_width = 20*ms

eqs = '''du/dt = (a*(u-EL)*(u-VT) + I)/C : volt
         I : amp'''
G = NeuronGroup(1, eqs,
                    threshold='u > Vcut',
                    reset='u = Vr')
G.I = input_current
M = StateMonitor(G, 'u', record=0)
S = SpikeMonitor(G, 'u')

G.u = EL
print('Before v = %s' % G.u[0])
run(t_simulation)
print('After v = %s' % G.u[0])
spikes = S.all_values()
print(spikes)

spike_cnt_list = list()
spike_timings = sorted(spikes['t'][0])
i = 0
bins = list()
t_start = 0
while i < len(spike_timings):
    start = t_start
    end = t_start + spike_bins_width
    n_spikes = 0
    while i < len(spike_timings) and spike_timings[i] < end:
        n_spikes += 1
        i += 1
    spike_cnt_list.append(n_spikes)
    bins.append((start+end)*1000//2)
    t_start = end
    
plot(M.t/ms, M.u[0])
xlabel('Time (ms)')
ylabel('v')
plt.show()

print(spike_cnt_list)
print(bins)
plt.plot(bins, spike_cnt_list)
plt.xlabel('Time (ms)')
plt.ylabel('Frequency of Spikes (per {}s)'.format(spike_bins_width))
plt.show()