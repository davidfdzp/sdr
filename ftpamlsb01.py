#!/usr/bin/env python

# File: ftpamlsb01.py
# Script file that accepts a text string as input and
# produces a corresponding binary unipolar flat-top PAM signal
# s(t) with bit rate Fb and sampling rate Fs.
# The text string uses character to byte encoding and LSB-first
# conversion to a bitstream dn. At every index value
# n=0,1,2,..., dn is either 0 or 1. To convert dn to a
# flat-top PAM CT signal approximation s(t), the formula
# s(t) = dn, (n-1/2)*Tb <= t < (n+1/2)*Tb,
# is used.
# The generated signal is stored in a WAV file.
# It can be read with ftpamrcvr01.py
# See also: http://ecee.colorado.edu/~mathys/ecen4242/classnotes.html

import numpy as np
import matplotlib.pyplot as plt
import ascfun as af

fsz = (7,5) # figure size

Fs = 44100 # Sampling rate for s(t) in Hz (samples per second)
Fb = 100 # Bit rate for dn sequence (bits/s)

samples_per_bit = Fs/Fb

txt = 'MyTest' # Input text string

bits = 8 # Number of bits per character (it could be -8 for MSB first or 7...)

dn = af.asc2bin(txt, bits) # >> Conversion from txt to bitstream dn here
N = len(dn) # Total number of bits. Upsampling factor.
numSamples = 1 + N * samples_per_bit
Tb = 1/float(Fb) # Time per bit
ttdn = np.arange(0, N)*Tb # Time axis for dn
plt.figure(1, figsize=fsz)
plt.stem(ttdn[:N], dn[:N])
plt.ylim([-0.1, 1.1])
plt.ylabel('$dn(t)$')
plt.xlabel('t [sec]')
plt.xlim([-Tb, N*Tb])
strt1 = 'Stem Plot of bit encoded text $dn(t)$'
strt1 = strt1 + ', $F_b={}$ bits/s'.format(Fb)
plt.title(strt1)
plt.grid()
plt.show()

ixL = np.round(-0.5*Fs*Tb) # Left index for time axis
ixR = np.round((N-0.5)*Fs*Tb) # Right index for time axis
ttst = np.arange(ixL,ixR)/float(Fs) # Time axis for s(t)
# Differentiate dn
# ddnt = np.diff(np.hstack((0,dn)))*Fb
ddnt = np.diff(np.hstack((0,dn)))
# In order to place the resulting impulses spaced apart by Tb at t=-Tb/2, Tb/2, 3Tb/2, 5Tb/2... in st,
# expand ddnt inserting samples_per_bit-1 zeros after each sample, by constructing a 2-dimensional array whose first row is ddnt and whose remaining samples_per_bit-1 rows are all zeros.
ddNt = np.vstack((ddnt, np.zeros((samples_per_bit-1, ddnt.size)))) # expand samples_per_bit times
ddNt = np.reshape(ddNt, -1, order='F') # reshape into 1-dimensional array reading columns first. F stands for Fortran.
# print('ddNt = {}'.format(ddNt[:24])) # check readout order
# create a labeled graph
plt.figure(2, figsize=fsz)
# plt.plot(ttdn[:N], ddnt[:N], '-b')
# plt.plot(ttdn[:N], ddnt[:N], 'or', label='ddnt values')
plt.plot(ttst[:numSamples], ddNt[:numSamples], '-b')
plt.plot(ttst[:numSamples], ddNt[:numSamples], 'or', label='ddNt values')
plt.ylabel('$dn(t)/dt$')
# plt.ylim([-Fb*1.1, Fb*1.1])
plt.ylim([-1.1, 1.1])
plt.xlabel('t [sec]')
plt.xlim([-Tb, (N+1)*Tb])
strt2 = 'Derivative of bit encoded text wave $ddn(t)/dt$'
strt2 = strt2 + ', $F_b={}$ bits/s, $F_s={}$ Hz'.format(Fb, Fs)
plt.title(strt2)
plt.legend()
plt.grid()
plt.show()
# integral of derivative of dn
# ddntit = np.cumsum(ddnt)/float(Fb)
# ddntit = np.cumsum(ddnt)
ddNtit = np.cumsum(ddNt)
st = ddNtit # >> Generate flat-top PAM signal s(t) here <<
Sf = np.fft.fft(st)/float(Fs)
Nsf = Sf.size
Dsf = Fs/float(Nsf)
ff = Dsf*np.arange(Nsf)-Fs/2.0
Sf = np.fft.fftshift(Sf)
ff2 = 6*Fb; ff1 = -ff2
ixdff = np.where(np.logical_and(ff>=ff1, ff<=ff2))

# create a labeled graph
plt.figure(3, figsize=fsz)
plt.subplot(211)
# plt.plot(ttdn[:N], ddntit[:N], '-b')
# plt.plot(ttdn[:N], ddntit[:N], 'xr', label='ddntit values')
plt.plot(ttst[:numSamples], st[:numSamples], '-b')
plt.plot(ttdn[:N], dn[:N], 'xr', label='Samples at t=n$T_b$')
# plt.plot(ttst[:numSamples], ddNtit[:numSamples], 'xr', label='ddNtit values')
plt.ylim([-0.5, 1.5])
# plt.ylabel('Integral of $ddN(t)/dt$')
plt.ylabel('$s(t)$')
plt.xlabel('t [sec]')
plt.xlim([-Tb, N*Tb])
# strt3 = 'Integral of Derivative of bit encoded text wave $ddN(t)/dt$'
strt3 = 'Unipolar Binary Flat-Top PAM $s(t)$'
strt3 = strt3 + ', $F_b={}$ bits/s, $F_s={}$ Hz'.format(Fb, Fs)
plt.title(strt3)
plt.legend()
plt.grid()
plt.subplot(212)
plt.plot(ff[ixdff], 20*np.log10(np.abs(Sf[ixdff])), '-m', label='$|S(f)|$')
plt.ylim([-80, 20])
plt.ylabel('$|S(f)|$ [dB]')
plt.xlabel('$f$ [Hz]')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

import wavfun as wf
wf.wavwrite('MyTest.wav', Fs, st/float(max(abs(st)))) # Write wav-file

# From http://ecee.colorado.edu/~mathys/ecen4242/classnotes/python/PAM_007.pdf
SNRdB = 20 # signal-to-noise ratio
# Generate Gaussian noise
nt=np.random.randn(st.size)
P_nt=np.mean(np.power(nt,2.0)) # generated randn noise power
SNR=10**(SNRdB/10.0)
Ps=np.mean(np.power(st,2.0)) # signal power
An=np.sqrt(Ps/(SNR*P_nt)) # Noise amplitude
Ant = An*nt # noise to add to st to get the selected SNR
P_Ant=np.mean(np.power(An*nt,2.0)) # Noise power
print('Ps={:4.3f}, Pn={:5.4f}'.format(Ps,P_Ant))
wf.wavwrite('MyTestNoise.wav', Fs, Ant/float(max(abs(Ant)))) # Write wav-file

plt.figure(4, figsize=fsz)
plt.plot(ttst[:numSamples], Ant[:numSamples], '-b')
plt.ylabel('$An(t)$')
plt.xlabel('t [sec]')
plt.xlim([-Tb, N*Tb])
strt4 = 'Random Noise $An(t)$'
strt4 = strt4 + ', $F_b={}$ bits/s, $F_s={}$ Hz'.format(Fb, Fs)
plt.title(strt4)
plt.grid()
plt.show()

# Signal plus noise
rt = st + Ant
Rf = np.fft.fft(rt)/float(Fs)
Nrf = Rf.size
Drf = Fs/float(Nrf)
ff = Drf*np.arange(Nrf)-Fs/2.0
Rf = np.fft.fftshift(Rf)
ff2 = 6*Fb; ff1 = -ff2
ixdff = np.where(np.logical_and(ff>=ff1, ff<=ff2))
# create a labeled graph
plt.figure(5, figsize=fsz)
plt.subplot(211)
plt.plot(ttst[:numSamples], rt[:numSamples], '-b')
plt.ylim([-0.5, 1.5])
plt.ylabel('$r(t)$')
plt.xlabel('t [sec]')
plt.xlim([-Tb, N*Tb])
strt5 = 'Unipolar Binary Flat-Top PAM $s(t) with noise$'
strt5 = strt5 + ', $F_b={}$ bits/s, $F_s={}$ Hz'.format(Fb, Fs)
strt5 = strt5 + ', SNR={} dB'.format(SNRdB)
plt.title(strt5)
plt.legend()
plt.grid()
plt.subplot(212)
plt.plot(ff[ixdff], 20*np.log10(np.abs(Rf[ixdff])), '-m', label='$|R(f)|$')
plt.ylim([-80, 20])
plt.ylabel('$|R(f)|$ [dB]')
plt.xlabel('$f$ [Hz]')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

wf.wavwrite('MyTestWithNoise.wav', Fs, rt/float(max(abs(rt)))) # Write wav-file