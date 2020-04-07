#!/usr/bin/env python3
#
# Copyright 2012,2013 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

"""
BER simulation for 16QAM signals, compare to theoretical values.
Change the N_BITS value to simulate more bits per Eb/N0 value,
thus allowing to check for lower BER values.
Lower values will work faster, higher values will use a lot of RAM.
Also, this app isn't highly optimized--the flow graph is completely
reinstantiated for every Eb/N0 value.
Of course, expect the maximum value for BER to be one order of
magnitude below what you chose for N_BITS.
"""

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

# Best to choose powers of 10
N_BITS = 1e7
RAND_SEED = 42

# in order to achieve the same bit-error probability as BPSK, QPSK uses twice the power (since two bits are transmitted simultaneously)
def berawgn16qam(EbN0):
    k = 4 # bits per symbol
    """ Calculates theoretical bit error rate in AWGN (for 16QAM and given Eb/N0) """    
#   http://www.dsplog.com/db-install/wp-content/uploads/2008/06/script_16qam_gray_mapping_bit_error_rate.m
    return (1/k)*3/2*erfc(math.sqrt(k*0.1*(10**(float(EbN0)/10))))

class BitErrors(gr.hier_block2):
    """ Two inputs: true and received bits. We compare them and
    add up the number of incorrect bits. Because integrate_ff()
    can only add up a certain number of values, the output is
    not a scalar, but a sequence of values, the sum of which is
    the BER. """
    def __init__(self, bits_per_byte):
        gr.hier_block2.__init__(self, "BitErrors",
                gr.io_signature(2, 2, gr.sizeof_char),
                gr.io_signature(1, 1, gr.sizeof_int))

        # Bit comparison
        comp = blocks.xor_bb()
        intdump_decim = 100000
        if N_BITS < intdump_decim:
            intdump_decim = int(N_BITS)
        self.connect(self,
                     comp,
                     blocks.unpack_k_bits_bb(bits_per_byte),
                     blocks.uchar_to_float(),
                     blocks.integrate_ff(intdump_decim),
                     blocks.multiply_const_ff(1.0 / N_BITS),
                     self)
        self.connect((self, 1), (comp, 1))

class BERAWGNSimu(gr.top_block):
    " This contains the simulation flow graph "
    def __init__(self, EbN0):
        gr.top_block.__init__(self)
        # By default it creates a 16QAM
        
        # gnuradio.digital.qam.qam_constellation(constellation_points=16, differential=True, mod_code='none', large_ampls_to_corners=False)
        m = 16
        differential = True
        mod_code = digital.mod_codes.GRAY_CODE
        large_ampls_to_corners=True
        # Creates a QAM constellation object.

        # If large_ampls_to_corners=True then sectors that are probably occupied due to a phase offset, are not mapped to the closest constellation point. Rather we take into account the fact that a phase offset is probably the problem and map them to the closest corner point. It’s a bit hackish but it seems to improve frequency locking.

        self.const = digital.qam.qam_constellation(m, differential, mod_code, large_ampls_to_corners)
        # Source is N_BITS bits, non-repeated
        data = list(map(int, numpy.random.randint(0, self.const.arity(), int(N_BITS / self.const.bits_per_symbol()))))
        src   = blocks.vector_source_b(data, False)
        mod   = digital.chunks_to_symbols_bc((self.const.points()), 1)
        add   = blocks.add_vcc()
        noise = analog.noise_source_c(analog.GR_GAUSSIAN,
                                      self.EbN0_to_noise_voltage(EbN0),
                                      RAND_SEED)
        demod = digital.constellation_decoder_cb(self.const.base())
        ber   = BitErrors(self.const.bits_per_symbol())
        self.sink  = blocks.vector_sink_f()
        self.connect(src, mod, add, demod, ber, self.sink)
        self.connect(noise, (add, 1))
        self.connect(src, (ber, 1))

    def EbN0_to_noise_voltage(self, EbN0):
        """ Converts Eb/N0 to a complex noise voltage (assuming unit symbol power) """
        EsN0_dB  = EbN0 + 10*math.log10(self.const.bits_per_symbol());
        return 1.0 / math.sqrt((10**(float(EsN0_dB) / 10)))

def simulate_ber(EbN0):
    """ All the work's done here: create flow graph, run, read out BER """
    print("Eb/N0 = %d dB" % EbN0)
    fg = BERAWGNSimu(EbN0)
    fg.run()
    return numpy.sum(fg.sink.data())

if __name__ == "__main__":
    bits_per_symbol = 4
    EbN0_min = -6
    EbN0_max = 14
    EbN0_range = list(range(EbN0_min, EbN0_max+1))
    EsN0_range  = [x + 10*math.log10(bits_per_symbol) for x in EbN0_range]
    ber_theory_16qam = [berawgn16qam(x)      for x in EbN0_range]
    print("Simulating...")
    ber_simu   = [simulate_ber(x) for x in EbN0_range]

    f = pyplot.figure()
    s = f.add_subplot(1,1,1)
    s.semilogy(EbN0_range, ber_theory_16qam, 'g-.', label="Theoretical 16QAM AWGN")
    s.semilogy(EbN0_range, ber_simu, 'b-o', label="Simulated 16QAM")
    s.set_title('BER Simulation')
    s.set_xlabel('Eb/N0 (dB)')
    s.set_ylabel('BER')
    s.legend()
    s.grid()
    pyplot.show()

    ff = pyplot.figure()
    ss = ff.add_subplot(1,1,1)
    ss.semilogy(EsN0_range, ber_theory_16qam, 'g-.', label="Theoretical 16QAM AWGN")
    ss.semilogy(EsN0_range, ber_simu, 'b-o', label="Simulated 16QAM")
    ss.set_title('BER Simulation')
    ss.set_xlabel('Es/N0 (dB)')
    ss.set_ylabel('BER')
    ss.legend()
    ss.grid()
    pyplot.show()