#!/usr/bin/env python3

# File: ptfunTest.py
import ptfun as pf
import numpy as np
import matplotlib.pyplot as plt

fsz = (7,5) # figure size

# Samples per symbol = Fs/Fb
Fs = 8000 # samples per symbol
Fb = 100 # baud rate: 1 symbol per second

# b_ptype = 'rcf'

b_ptype = 'rrcf'

# alpha parameter for bandwidth limitation
# c_alpha = 0.2
c_alpha = 0.0001

# k parameter for pulse duration
d_k = 5

pt_taps = pf.pam_pt(Fs,Fb,b_ptype,[d_k,c_alpha])
print("Number of pulse taps: "+"{}".format(len(pt_taps)))
