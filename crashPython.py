import numpy as np
import matplotlib.pyplot as plt

from sinc_ipol import sinc_ipol

# Matplotlib notebook from lab01.pdf
fsz = (7,5) # figure size
fsz2 = (fsz[0], fsz[1]/2.0) # half high figure
# initial parameters
Fs = 8000 # sampling rate
fm = 1000 # frequency of sinusoid
samples_per_period = Fs/fm
phi = 30 # phase in degrees
A = 1.2 # Amplitude
tlen = 1.0 # length in seconds
# generate time axis
tt = np.arange(np.round(tlen*Fs))/float(Fs)
# generate sine
x1t = np.sin(2*np.pi*fm*tt)
# generate complex exponential
x2t = A*np.exp(1j*(2*np.pi*fm*tt + np.pi/180*phi))
# print the first 12 values of x1(t)
print('x1t = {}'.format(x1t[:12]))
# plot x1t
plt.figure(1, figsize=fsz)
plt.plot(tt[:24], x1t[:24])
plt.grid()
plt.show()
# create a labeled graph
plt.figure(2, figsize=fsz)
plt.plot(tt[:24], x1t[:24], '-b')
plt.plot(tt[:24], x1t[:24], 'or', label='x1t values')
# plt.plot(tt[:24], x1t[:24], label='x1t values')
plt.ylabel('$x1(t)$')
plt.xlabel('t [sec]')
strt2 = 'Sinusoidal Waveform $x1(t)$'
strt2 = strt2 + ', $f_m={}$ Hz, $F_s={}$ Hz'.format(fm, Fs)
plt.title(strt2)
plt.legend()
plt.grid()
plt.show()
# stem plot of sinusoidal
plt.figure(3, figsize=fsz)
plt.stem(tt[:24], x1t[:24])
plt.ylim([-1.2, 1.2])
plt.ylabel('$x1(t)$')
plt.xlabel('t [sec]')
strt3 = 'Stem Plot of Sinusoidal Waveform $x1(t)$'
strt3 = strt3 + ', $f_m={}$ Hz, $F_s={}$ Hz'.format(fm, Fs)
plt.title(strt3)
plt.grid()
plt.show()
# expand x1t 3-fold inserting two zeros after each sample by constructing a 2-dimensional array whose first row is x1t and whose remaining two rows are all zeros.
N = 3 # upsampling factor
xNt = np.vstack((x1t, np.zeros((N-1, x1t.size)))) # expand N times
xNt = np.reshape(xNt, -1, order='F') # reshape into 1-dimensional array reading columns first. F stands for Fortran.
print('xNt = {}'.format(xNt[:24])) # check readout order
FsN = N*Fs # new sampling rate
ttN = np.arange(xNt.size)/float(FsN) # new time axis
# new stem plot of sinusoidal
plt.figure(4, figsize=fsz)
plt.stem(ttN[:N*24], xNt[:N*24])
plt.ylim([-1.2, 1.2])
plt.ylabel('$xN(t)$')
plt.xlabel('t [sec]')
strt4 = 'Expanded by $N={}$ Sinusoidal Waveform $xN(t)$'.format(N)
strt4 = strt4 + ', $f_m={}$ Hz, $F_s={{sN}}={}$ Hz'.format(fm, FsN)
plt.title(strt4)
plt.grid()
plt.show()
# plot of interpolation waveform
fL = 3000 # cutoff frequency
k = 10 # sinc pulse truncation
tth, ht = sinc_ipol(FsN, fL, k)
plt.figure(5, figsize=fsz)
plt.plot(tth, ht, '-m')
plt.ylabel('$h(t)$')
plt.xlabel('t [sec]')
strt5 = "'sinc' Pulse for Interpolation"
strt5 = strt5 + ', $F_s={}$ Hz, $f_L={}$ Hz, $k={}$'.format(FsN, fL, k)
plt.title(strt5)
plt.grid()
plt.show()
# convolve expanded sine sequence with interpolation waveform to obtain upsampled (by N) sequence yNt with sampling rate FsN
yNt = np.convolve(xNt, ht, 'same')/float(Fs)
# stem plot of upsampled sequence
plt.figure(6, figsize=fsz)
plt.stem(ttN[:N*24], yNt[:N*24])
plt.ylim([-1.2, 1.2])
plt.ylabel('$yN(t)$')
plt.xlabel('t [sec]')
strt6 = 'Sine Waveform $yN(t)$, Upsampled $N={}$'.format(N)
strt6 = strt6 + ', $f_m={}$ Hz, $F_s={{sN}}={}$ Hz'.format(fm, FsN)
plt.title(strt6)
plt.grid()
plt.show()
# plot a complex exponential
plt.figure(7, figsize=fsz)
plt.plot(tt[:48], x2t[:48].real, '-b', label='x2t.real')
plt.plot(tt[:48], x2t[:48].imag, '--r', label='x2t.imag')
plt.ylim([-1.5, 1.5])
plt.ylabel('Re[x2t], Im[x2t]')
plt.xlabel('t [sec]')
strt1 = 'Real/Imaginary Parts of Complex Exponential $x2(t)$'
strt1 = strt1 + ', $f_m={}$ Hz, $F_s={}$ Hz'.format(fm, Fs)
plt.title(strt1)
plt.legend(loc=1)
plt.grid()
plt.show()

