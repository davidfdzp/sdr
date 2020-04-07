# File: sine100.py
# Asks for sampling frequency Fs and then generates
# and plots 5 periods of a 100 Hz sinewave
import numpy as np
import matplotlib.pyplot as plt

from ast import literal_eval
fsz = (7,5) # figure size
numPeriods = 5
Fs = int(input('Enter Fs in Hz (3200): '))
f0 = 100 # Frequency of sine
samples_per_period = Fs/f0
numPoints = 1 + numPeriods * samples_per_period
tlen = numPeriods/float(f0) # Signal duration in sec
tt = np.arange(0,np.round(tlen*Fs))/float(Fs) # Time axis
st = np.sin(2*np.pi*f0*tt) # Sinewave, frequency f0
rt = np.sign(st) # Sine -> rectangular
plt.figure(1, figsize=fsz)
plt.plot(tt[:numPoints], st[:numPoints])
plt.plot(tt[:numPoints], rt[:numPoints])
plt.ylim([-1.2, 1.2])
plt.grid()
plt.show()
# derivative of rt
rdt = np.diff(np.hstack((0,rt)))*Fs
# create a labeled graph
plt.figure(2, figsize=fsz)
plt.plot(tt[:numPoints], rdt[:numPoints], '-b')
plt.plot(tt[:numPoints], rdt[:numPoints], 'or', label='rdt values')
# plt.plot(tt[:numPoints], rdt[:numPoints], 'or')
plt.ylabel('$dr(t)/dt$')
plt.xlabel('t [sec]')
strt1 = 'Derivative of Rectangular Wave $r(t)$'
strt1 = strt1 + ', $f_0={}$ Hz, $F_s={}$ Hz'.format(f0, Fs)
plt.title(strt1)
plt.legend()
plt.grid()
plt.show()
# stem plot
plt.figure(3, figsize=fsz)
plt.stem(tt[:numPoints], rdt[:numPoints])
# plt.ylim([-1.2, 1.2])
plt.ylabel('$rd(t)$')
plt.xlabel('t [sec]')
plt.xlim([0, 0.05])
strt2 = 'Stem Plot of Derivative of Rectangular Wave $r(t)$'
strt2 = strt2 + ', $f_0={}$ Hz, $F_s={}$ Hz'.format(f0, Fs)
plt.title(strt2)
plt.grid()
plt.show()
# integral of derivative of rt
rdit = np.cumsum(rdt)/float(Fs)
# create a labeled graph
plt.figure(4, figsize=fsz)
plt.plot(tt[:numPoints], rdit[:numPoints], '-b')
plt.plot(tt[:numPoints], rdit[:numPoints], 'or', label='rdit values')
# plt.plot(tt[:numPoints], rdit[:numPoints], 'or')
plt.ylim([-1.2, 1.2])
plt.ylabel('Integral of $dr(t)/dt$')
plt.xlabel('t [sec]')
strt3 = 'Integral of Derivative of Rectangular Wave $r(t)$'
strt3 = strt3 + ', $f_0={}$ Hz, $F_s={}$ Hz'.format(f0, Fs)
plt.title(strt3)
plt.legend()
plt.grid()
plt.show()
# stem plot
plt.figure(5, figsize=fsz)
plt.stem(tt[:numPoints], rdit[:numPoints])
plt.ylim([-1.2, 1.2])
plt.ylabel('$rdi(t)$')
plt.xlabel('t [sec]')
plt.xlim([0, 0.05])
strt4 = 'Stem Plot of Integral of Derivative of Rectangular Wave $r(t)$'
strt4 = strt4 + ', $f_0={}$ Hz, $F_s={}$ Hz'.format(f0, Fs)
plt.title(strt4)
plt.grid()
plt.show()

