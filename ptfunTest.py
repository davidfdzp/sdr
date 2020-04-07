#!/usr/bin/env python3

# File: ptfunTest.py
import ptfun as pf
import numpy as np
import matplotlib.pyplot as plt

fsz = (7,5) # figure size

# Samples per symbol = Fs/Fb
Fs = 8000 # samples per symbol
Fb = 100 # baud rate: 1 symbol per second

a_sps = 20 # Fs/Fb

# Pulse type
# b_ptype = 'rect'
# b_ptype = 'tri'
# b_ptype = 'man'
# b_ptype = 'msin'
# b_ptype = 'rcf'
# b_ptype = 'rrcf'

# alpha parameter for bandwidth limitation
c_alpha = 0.2

# k parameter for pulse duration
d_k = 5

pt_taps = pf.pampt(a_sps,b_ptype,[d_k,c_alpha])
# pt_taps = pf.pam_pt(Fs,Fb,b_ptype,[d_k,c_alpha])
print("Number of pulse taps: "+"{}".format(len(pt_taps)))

# c_alpha = 0
if b_ptype == 'rcf':
    pt_taps0 = pf.pampt(a_sps,b_ptype,[d_k,c_alpha])
    # pt_taps0 = pf.pam_pt(Fs,Fb,b_ptype,[d_k,c_alpha])

c_alpha = 0.3
pt_taps03 = pf.pampt(a_sps,b_ptype,[d_k,c_alpha])
# pt_taps03 = pf.pam_pt(Fs,Fb,b_ptype,[d_k,c_alpha])

c_alpha = 0.5
pt_taps05 = pf.pampt(a_sps,b_ptype,[d_k,c_alpha])
# pt_taps05 = pf.pam_pt(Fs,Fb,b_ptype,[d_k,c_alpha])

nt = np.arange((-len(pt_taps)/2), (len(pt_taps)/2))
tt = nt/float(a_sps)
nk = round(d_k*a_sps)
nn = np.arange(-nk, nk)
# tt = np.arange(-d_k, d_k)
pt = np.sinc(nn/float(a_sps))

Pf=np.fft.fft(np.fft.fftshift(pt))/float(a_sps) # FT approximation
Pf=np.fft.fftshift(Pf)
NPf=Pf.size
DPf=a_sps/float(NPf)
ffPf=DPf*np.arange(NPf)-a_sps/2.0

Pf02=np.fft.fft(np.fft.fftshift(pt_taps))/float(a_sps) # FT approximation
Pf02=np.fft.fftshift(Pf02)
if b_ptype == 'rcf':
    Pf00=np.fft.fft(np.fft.fftshift(pt_taps0))/float(a_sps) # FT approximation
    Pf00=np.fft.fftshift(Pf00)
Pf03=np.fft.fft(np.fft.fftshift(pt_taps03))/float(a_sps) # FT approximation
Pf03=np.fft.fftshift(Pf03)
Pf05=np.fft.fft(np.fft.fftshift(pt_taps05))/float(a_sps) # FT approximation
Pf05=np.fft.fftshift(Pf05)

# create a labeled graph
plt.figure(1, figsize=fsz)
plt.subplot(211)
plt.plot(tt, pt_taps, '-b', label='alpha = 0.2')
if b_ptype == 'rcf':
    plt.plot(tt, pt_taps0, '-r', label='alpha = 0')
plt.plot(tt, pt_taps03, '-g', label='alpha = 0.3')
plt.plot(tt, pt_taps05, '-c', label='alpha = 0.5')
# plt.plot(tt, pt, '-m', label='sinc')
if b_ptype == 'rcf' or b_ptype == 'rrcf':
    plt.ylim([-0.4, 1.2])
plt.ylabel('$p(t)$')
plt.xlabel('t/T_B')
if b_ptype == 'rcf' or b_ptype == 'rrcf':
    plt.xlim([-d_k, d_k])
# plt.xlim([-nk, nk])
strt1="PAM Pulse $p(t)$ '{}'".format(b_ptype)
plt.title(strt1)
plt.legend()
plt.grid()

if b_ptype != 'rect' and b_ptype != 'tri' and b_ptype != 'man' and b_ptype != 'msin':
    plt.subplot(212)
    # plt.plot(ffPf,20*np.log10(np.abs(Pf)),'-m',label='$|P(f)|$ sinc')
    plt.plot(ffPf,20*np.log10(np.abs(Pf02)),'-b',label='$|P(f)|$ alpha = 0.2')
    if b_ptype == 'rcf':
        plt.plot(ffPf,20*np.log10(np.abs(Pf00)),'-r',label='$|P(f)|$ alpha = 0')
    plt.plot(ffPf,20*np.log10(np.abs(Pf03)),'-g',label='$|P(f)|$ alpha = 0.3')
    plt.plot(ffPf,20*np.log10(np.abs(Pf05)),'-c',label='$|P(f)|$ alpha = 0.5')
    # plt.ylim([-20,40])
    plt.legend()
    plt.grid()
    plt.tight_layout()
plt.show()