import numpy as np
import matplotlib.pyplot as plt
# Matplotlib notebook from lab01.pdf
fsz = (7,5) # figure size
fsz2 = (fsz[0], fsz[1]/2.0) # half high figure
Fs = 5000 # sampling rate
fo = 100 # frequency of sinusoid
samples_per_period = Fs/fo
tlen = 1.0 # length in seconds
numPeriods = 5
numPoints = 1 + numPeriods * samples_per_period
# generate time axis
tt = np.arange(np.round(tlen*Fs))/float(Fs)
# generate sine
x3t = np.sin(2*np.pi*fo*tt)
plt.figure(8, figsize=fsz)
plt.plot(tt[:numPoints], x3t[:numPoints], '-b')
# plt.plot(tt[:numPoints], x3t[:numPoints], 'or', label='x3t values')
plt.ylabel('$x3(t)$')
plt.xlabel('t [sec]')
plt.xlim([0, 0.05])
strt7 = 'Sinusoidal Waveform $x3(t)$'
strt7 = strt7 + ', $f_o={}$ Hz, $F_s={}$ Hz'.format(fo, Fs)
plt.title(strt7)
plt.legend()
plt.grid()
plt.show()
# stem plot of sinusoidal
plt.figure(9, figsize=fsz)
plt.stem(tt[:numPoints], x3t[:numPoints])
plt.ylim([-1.2, 1.2])
plt.ylabel('$x3(t)$')
plt.xlabel('t [sec]')
plt.xlim([0, 0.05])
strt8 = 'Stem Plot of Sinusoidal Waveform $x3(t)$'
strt8 = strt8 + ', $f_o={}$ Hz, $F_s={}$ Hz'.format(fo, Fs)
plt.title(strt8)
plt.grid()
plt.show()

