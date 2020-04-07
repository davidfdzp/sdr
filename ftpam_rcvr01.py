#!/usr/bin/env python

# File: ftpam_rcvr01.py
# Script file that accepts a binary unipolar flat-top PAM
# signal r(t) with bitrate Fb and sampling rate Fs as
# input and decodes it into a received text string.
# The PAM signal r(t) is received from a wav-file with
# sampling rate Fs, generated at ftpamlsb01.py. 
# First r(t) is sampled at the right
# DT sequence sampling times, spaced Tb = 1/Fb apart. The
# result is then quantized to binary (0 or 1) to form the
# estimated received sequence dnhat which is subsequently
# converted to 8-bit ASCII text.
import numpy as np
import ascfun as af
import wavfun as wf
import ptfun as pf

import matplotlib.pyplot as plt
fsz = (7,5) # figure size
# Fs, rt = wf.wavread('MyTest.wav')
Fs, rt = wf.wavread('MyTestWithNoise.wav')
Rf = np.fft.fft(rt)/float(Fs)
Nrf = Rf.size
Drf = Fs/float(Nrf)
ff = Drf*np.arange(Nrf)-Fs/2.0
Rf = np.fft.fftshift(Rf)
Fb = 100 # Data bit rate
Tb = 1/float(Fb) # Time per bit
bits = 8 # Number of bits/char
samples_per_bit = Fs/Fb
N = len(rt)/samples_per_bit # Number of received bits
ttdn = np.arange(0, N)*Tb # Time axis for dn
numSamples = 1 + N * samples_per_bit
ff2 = 6*Fb; ff1 = -ff2
ixdff = np.where(np.logical_and(ff>=ff1, ff<=ff2))

dlyr = 0.0 # sampling delay as fraction of Tb
NSr = Fb/float(Fs)*np.floor(rt.size)
ixsr = np.array(np.round(Fs/float(Fb)*(0.5+np.arange(NSr)+dlyr)),np.int64) # sampling times (n+dlyr)*Tb
ix = np.where(np.logical_and(ixsr>=0, ixsr<rt.size))[0]
ixsr = ixsr[ix] # trim ixsr values to indexes in received signal rt
dnhat = np.around(rt[ixsr])
dnhat = dnhat.astype(np.int8)
# dnhat = np.array(rt[1::samples_per_bit], np.int8) # >>Sample and quantize the received PAM signal here<<

ixL = np.round(-0.5*Fs*Tb) # Left index for time axis
ixR = np.round((N-0.5)*Fs*Tb) # Right index for time axis
ttst = np.arange(ixL,ixR)/float(Fs) # Time axis for s(t)
# create a labeled graph
plt.figure(1, figsize=fsz)
plt.subplot(211)
plt.plot(ttst[:numSamples], rt[:numSamples], '-b')
plt.plot(ttdn[:N], dnhat[:N], 'xr', label='Samples at t=n$T_b$')
plt.ylim([-0.5, 1.5])
plt.ylabel('$s(t)$')
plt.xlabel('t [sec]')
plt.xlim([-Tb, N*Tb])
strt1 = 'Unipolar Binary Flat-Top PAM $s(t)$'
strt1 = strt1 + ', $F_b={}$ bits/s, $F_s={}$ Hz'.format(Fb, Fs)
plt.title(strt1)
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

txthat = af.bin2asc(dnhat) # >>Convert bitstream dnhat to received text string<<
print(txthat) # Print result

ptype,pparms='rect',[10,0]
# ptype,pparms='sinc',[10,0]
ttAs,As=pf.eyediagram(ttst,rt,Fb)
plt.figure(2,figsize=fsz)
plt.plot(ttAs,As[0],'-b')
for i in range(1,As.shape[0]):
    plt.plot(ttAs,As[i],'-b')
strt2 = "Eye Diagram for '{}' PAM $s(t)$".format(ptype)
strt2 = strt2 + ', $F_B$={} Hz'.format(Fb)
strt2 = strt2 + ', $F_s$={} Hz'.format(Fs)
if ptype=='sinc':
    strt2 = strt2 + ', $k$={}, $\\beta$={}'.format(*pparms)
if(ptype=='rcf' or ptype=='rrcf'):
    strt2=strt2 + ', $k$={}, $\\alpha$={}'.format(*pparms)
plt.title(strt2)
plt.ylabel('$s(t)$')
plt.xlabel('$t/T_B$')
plt.grid()
plt.tight_layout()
plt.show()