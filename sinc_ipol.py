# File: sinc_ipol.py
# Used at crashPython.py
import numpy as np
def sinc_ipol(Fs, fL, k):
	"""
	sinc interpolation function, cutoff frequency fL, taillength k/(2*fL) seconds
	>>>>> tth, ht = sinc_ipol(Fs, fL, k) <<<<<
	where Fs sampling rate
	      fL cutoff frequency in Hz
	      k taillength in terms of zero crossings of sinc
	      tth time axis for h(t)
	      ht truncated sinc pulse h(t)
	"""
	# create time axis
	ixk = int(np.round(Fs*k/float(2*fL)))
	tth = np.arange(-ixk, ixk+1)/float(Fs)
	# sinc pulse
	ht = 2*fL*np.sinc(2*fL*tth)
	return tth, ht

