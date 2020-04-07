#!/usr/bin/env python3

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals


import math
import numpy
from gnuradio import gr, digital
from gnuradio import analog
from gnuradio import blocks
import sys

try:
    from scipy.special import erfc
except ImportError:
    print("Error: could not import scipy (http://www.scipy.org/)")
    sys.exit(1)

try:
    from matplotlib import pyplot
except ImportError:
    print("Error: could not from matplotlib import pyplot (http://matplotlib.sourceforge.net/)")
    sys.exit(1)

sym_map = [0, 1, 2, 3, 6, 7, 4, 5, 25, 24, 27, 26, 31, 30, 29, 28, 18, 19, 16, 17, 20, 21, 22, 23, 11, 10, 9, 8, 13, 12, 15, 14]
const_points = [(-7+7j), (-3+7j), (1+7j), (5+7j), (-5+5j), (-1+5j), (3+5j), (7+5j), (-7+3j), (-3+3j), (1+3j), (5+3j), (-5+1j), (-1+1j), (3+1j), (7+1j), (-7-1j), (-3-1j), (1-1j), (5-1j), (-5-3j), (-1-3j), (3-3j), (7-3j), (-7-5j), (-3-5j), (1-5j), (5-5j), (-5-7j), (-1-7j), (3-7j), (7-7j)]
rot_sym = 4
dims = 1

print(len(sym_map))

print(len(const_points))

print(digital.constellation_calcdist(const_points, sym_map, rot_sym, dims))