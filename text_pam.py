#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Pulse Amplitude Modulation
# Author: Peter Mathys
# Description: Text to PAM
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from byte2sym_byte2floatMSB import byte2sym_byte2floatMSB  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import fec
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from pam_xmtr16_ff import pam_xmtr16_ff  # grc-generated hier_block
from pamrcvr216_ff import pamrcvr216_ff  # grc-generated hier_block
from sym2byte_float2byteMSB import sym2byte_float2byteMSB  # grc-generated hier_block
import pmt
from gnuradio import qtgui

class text_pam(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Pulse Amplitude Modulation")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Pulse Amplitude Modulation")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "text_pam")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.bits_per_symbol = bits_per_symbol = 1
        self.tag = tag = gr.tag_utils.python_to_tag((0, pmt.intern("Z"), pmt.intern("0x5a"), pmt.intern("Vsrc")))
        self.sps = sps = 10
        self.samp_rate = samp_rate = 32000
        self.samp_dly = samp_dly = 67
        self.ptype = ptype = 'rect'
        self.polar = polar = 1
        self.baud_delay = baud_delay = 0
        self.alpha = alpha = 0.2
        self.M = M = 2**bits_per_symbol
        self.An = An = 0

        ##################################################
        # Blocks
        ##################################################
        self._samp_dly_range = Range(0, sps*8, 1, 67, 200)
        self._samp_dly_win = RangeWidget(self._samp_dly_range, self.set_samp_dly, 'samp_dly', "counter_slider", int)
        self.top_grid_layout.addWidget(self._samp_dly_win)
        # Create the options list
        self._ptype_options = ["rect", "rcf", "rrcf", "tri", "man" ,"msin"]
        # Create the labels list
        self._ptype_labels = ["rect", "rcf", "rrcf", "tri", "man", "msin"]
        # Create the combo box
        self._ptype_tool_bar = Qt.QToolBar(self)
        self._ptype_tool_bar.addWidget(Qt.QLabel('ptype' + ": "))
        self._ptype_combo_box = Qt.QComboBox()
        self._ptype_tool_bar.addWidget(self._ptype_combo_box)
        for _label in self._ptype_labels: self._ptype_combo_box.addItem(_label)
        self._ptype_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ptype_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._ptype_options.index(i)))
        self._ptype_callback(self.ptype)
        self._ptype_combo_box.currentIndexChanged.connect(
            lambda i: self.set_ptype(self._ptype_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._ptype_tool_bar)
        # Create the options list
        self._polar_options = (1, 1, )
        # Create the labels list
        self._polar_labels = ('unipolar', 'polar', )
        # Create the combo box
        self._polar_tool_bar = Qt.QToolBar(self)
        self._polar_tool_bar.addWidget(Qt.QLabel('polar' + ": "))
        self._polar_combo_box = Qt.QComboBox()
        self._polar_tool_bar.addWidget(self._polar_combo_box)
        for _label in self._polar_labels: self._polar_combo_box.addItem(_label)
        self._polar_callback = lambda i: Qt.QMetaObject.invokeMethod(self._polar_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._polar_options.index(i)))
        self._polar_callback(self.polar)
        self._polar_combo_box.currentIndexChanged.connect(
            lambda i: self.set_polar(self._polar_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._polar_tool_bar)
        self._baud_delay_range = Range(0, 8, 1, 0, 8)
        self._baud_delay_win = RangeWidget(self._baud_delay_range, self.set_baud_delay, 'Baud delay', "counter_slider", int)
        self.top_grid_layout.addWidget(self._baud_delay_win)
        self._alpha_range = Range(0, 1, 0.5, 0.2, 200)
        self._alpha_win = RangeWidget(self._alpha_range, self.set_alpha, 'alpha', "counter_slider", float)
        self.top_grid_layout.addWidget(self._alpha_win)
        self._An_range = Range(0, 1, 0.01, 0, 200)
        self._An_win = RangeWidget(self._An_range, self.set_An, 'An', "counter_slider", float)
        self.top_grid_layout.addWidget(self._An_win)
        self.sym2byte_float2byteMSB_0 = sym2byte_float2byteMSB(
            baud_delay=baud_delay,
            bit_endianess=1,
            bits_per_symbol=bits_per_symbol,
            bits_to_use_per_byte_mask=255,
            gain=1,
            invert=0,
            polar=polar,
        )
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate*sps, #samp_rate
            "", #name
            2 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "Z")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_f(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate*sps, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, 0)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win)
        self.pamrcvr216_ff_0 = pamrcvr216_ff(
            a_sps=sps,
            b_ptype=ptype,
            c_alpha=alpha,
            d_k=5,
            dly=samp_dly,
        )
        self.pam_xmtr16_ff_0 = pam_xmtr16_ff(
            a_sps=sps,
            b_ptype=ptype,
            c_alpha=alpha,
            d_k=5,
        )
        self.fec_ber_bf_0 = fec.ber_bf(False, 100, -7.0)
        self.byte2sym_byte2floatMSB_0 = byte2sym_byte2floatMSB(
            bit_endianess=1,
            bits_per_symbol=bits_per_symbol,
            bits_to_use_per_byte_mask=255,
            invert=0,
            polar=1,
        )
        self.blocks_vector_source_x_0 = blocks.vector_source_b(list(ord(i) for i in 'Zombie'), True, 1, [tag])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/dev/pts/1', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_fastnoise_source_x_0 = analog.fastnoise_source_f(analog.GR_GAUSSIAN, An, 0, 8192)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fastnoise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.pamrcvr216_ff_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.pam_xmtr16_ff_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.byte2sym_byte2floatMSB_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.fec_ber_bf_0, 0))
        self.connect((self.byte2sym_byte2floatMSB_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.fec_ber_bf_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.pam_xmtr16_ff_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.pamrcvr216_ff_0, 2), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.pamrcvr216_ff_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.pamrcvr216_ff_0, 1), (self.sym2byte_float2byteMSB_0, 0))
        self.connect((self.sym2byte_float2byteMSB_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.sym2byte_float2byteMSB_0, 0), (self.fec_ber_bf_0, 1))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "text_pam")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_bits_per_symbol(self):
        return self.bits_per_symbol

    def set_bits_per_symbol(self, bits_per_symbol):
        self.bits_per_symbol = bits_per_symbol
        self.set_M(2**self.bits_per_symbol)
        self.byte2sym_byte2floatMSB_0.set_bits_per_symbol(self.bits_per_symbol)
        self.sym2byte_float2byteMSB_0.set_bits_per_symbol(self.bits_per_symbol)

    def get_tag(self):
        return self.tag

    def set_tag(self, tag):
        self.tag = tag
        self.blocks_vector_source_x_0.set_data(list(ord(i) for i in 'Zombie'), [self.tag])

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.pam_xmtr16_ff_0.set_a_sps(self.sps)
        self.pamrcvr216_ff_0.set_a_sps(self.sps)
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate*self.sps)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate*self.sps)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate*self.sps)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate*self.sps)

    def get_samp_dly(self):
        return self.samp_dly

    def set_samp_dly(self, samp_dly):
        self.samp_dly = samp_dly
        self.pamrcvr216_ff_0.set_dly(self.samp_dly)

    def get_ptype(self):
        return self.ptype

    def set_ptype(self, ptype):
        self.ptype = ptype
        self._ptype_callback(self.ptype)
        self.pam_xmtr16_ff_0.set_b_ptype(self.ptype)
        self.pamrcvr216_ff_0.set_b_ptype(self.ptype)

    def get_polar(self):
        return self.polar

    def set_polar(self, polar):
        self.polar = polar
        self._polar_callback(self.polar)
        self.sym2byte_float2byteMSB_0.set_polar(self.polar)

    def get_baud_delay(self):
        return self.baud_delay

    def set_baud_delay(self, baud_delay):
        self.baud_delay = baud_delay
        self.sym2byte_float2byteMSB_0.set_baud_delay(self.baud_delay)

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.pam_xmtr16_ff_0.set_c_alpha(self.alpha)
        self.pamrcvr216_ff_0.set_c_alpha(self.alpha)

    def get_M(self):
        return self.M

    def set_M(self, M):
        self.M = M

    def get_An(self):
        return self.An

    def set_An(self, An):
        self.An = An
        self.analog_fastnoise_source_x_0.set_amplitude(self.An)



def main(top_block_cls=text_pam, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
