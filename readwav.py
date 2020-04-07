import numpy as np
import matplotlib.pyplot as plt
from wavfun import wavread

fname = raw_input("Enter filename to read: ")
# print ("type of filename", type(fname))
Fs, st = wavread(fname)
numPoints = len(st)
tlen = numPoints/float(Fs)
# generate time axis
tt = np.arange(np.round(tlen*Fs))/float(Fs)

fsz = (7,5) # figure size
# create a labeled graph
plt.figure(1, figsize=fsz)
plt.plot(tt[:numPoints], st[:numPoints], '-b')
plt.plot(tt[:numPoints], st[:numPoints], 'or', label='samples of a signal')
plt.ylabel('$s(t)$')
plt.xlabel('t [sec]')
strt1 = 'Samples of a signal $s(t)$'
strt1 = strt1 + ', $F_s={}$ Hz'.format(Fs)
plt.title(strt1)
plt.legend()
plt.grid()
plt.show()

