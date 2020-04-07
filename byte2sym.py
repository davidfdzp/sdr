#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Byte to Float Symbols
# Author: Peter Mathys
# Description: Conversion from bytes to M-ary symbols
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

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import pmt
from gnuradio import qtgui

class byte2sym(gr.top_block, Qt.QWidget):

    def __init__(self, bit_endianess=1, bits_to_use_per_byte_mask=255, gain=1):
        gr.top_block.__init__(self, "Byte to Float Symbols")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Byte to Float Symbols")
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

        self.settings = Qt.QSettings("GNU Radio", "byte2sym")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.bit_endianess = bit_endianess
        self.bits_to_use_per_byte_mask = bits_to_use_per_byte_mask
        self.gain = gain

        ##################################################
        # Variables
        ##################################################
        self.bits_per_symbol = bits_per_symbol = 1
        self.tag = tag = gr.tag_utils.python_to_tag((0, pmt.intern("Z"), pmt.intern("0x5a"), pmt.intern("Vsrc")))
        self.samp_rate = samp_rate = 32000
        self.polar = polar = 1
        self.invert = invert = 0
        self.baud_delay = baud_delay = 0
        self.M = M = 2**bits_per_symbol

        ##################################################
        # Blocks
        ##################################################
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
        # Create the options list
        self._invert_options = (0, 1, )
        # Create the labels list
        self._invert_labels = ('No Invert', 'Invert', )
        # Create the combo box
        self._invert_tool_bar = Qt.QToolBar(self)
        self._invert_tool_bar.addWidget(Qt.QLabel('Invert Bits' + ": "))
        self._invert_combo_box = Qt.QComboBox()
        self._invert_tool_bar.addWidget(self._invert_combo_box)
        for _label in self._invert_labels: self._invert_combo_box.addItem(_label)
        self._invert_callback = lambda i: Qt.QMetaObject.invokeMethod(self._invert_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._invert_options.index(i)))
        self._invert_callback(self.invert)
        self._invert_combo_box.currentIndexChanged.connect(
            lambda i: self.set_invert(self._invert_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._invert_tool_bar)
        self._bits_per_symbol_range = Range(1, 256, 1, 1, 256)
        self._bits_per_symbol_win = RangeWidget(self._bits_per_symbol_range, self.set_bits_per_symbol, 'Bits per symbol', "counter_slider", int)
        self.top_grid_layout.addWidget(self._bits_per_symbol_win)
        self._baud_delay_range = Range(0, 8, 1, 0, 8)
        self._baud_delay_win = RangeWidget(self._baud_delay_range, self.set_baud_delay, 'Baud delay', "counter_slider", int)
        self.top_grid_layout.addWidget(self._baud_delay_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "Z")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
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


        for i in range(1):
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
        self.digital_map_bb_1_0 = digital.map_bb(invert*list(2**8-1-i for i in range(2**8))+(1-invert)*list(range(2**8)))
        self.digital_map_bb_1 = digital.map_bb(invert*list(2**8-1-i for i in range(2**8))+(1-invert)*list(range(2**8)))
        self.blocks_vector_source_x_0 = blocks.vector_source_b(list(ord(i) for i in 'Zombie'), True, 1, [tag])
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(bits_per_symbol, gr.GR_LSB_FIRST)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(bits_per_symbol, gr.GR_LSB_FIRST)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(gain)
        self.blocks_float_to_char_0 = blocks.float_to_char(1, polar*0.5+(1-polar))
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/dev/pts/1', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, baud_delay)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, polar*0.5+(1-polar))
        self.blocks_and_const_xx_0_0 = blocks.and_const_bb(bits_to_use_per_byte_mask)
        self.blocks_and_const_xx_0 = blocks.and_const_bb(bits_to_use_per_byte_mask)
        self.blocks_add_const_vxx_1 = blocks.add_const_ff(polar*(M-1)-(1-polar)*0)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(-polar*(M-1)+(1-polar)*0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_float_to_char_0, 0))
        self.connect((self.blocks_and_const_xx_0, 0), (self.digital_map_bb_1, 0))
        self.connect((self.blocks_and_const_xx_0_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.blocks_float_to_char_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.digital_map_bb_1_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_and_const_xx_0, 0))
        self.connect((self.digital_map_bb_1, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.digital_map_bb_1_0, 0), (self.blocks_and_const_xx_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "byte2sym")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_bit_endianess(self):
        return self.bit_endianess

    def set_bit_endianess(self, bit_endianess):
        self.bit_endianess = bit_endianess

    def get_bits_to_use_per_byte_mask(self):
        return self.bits_to_use_per_byte_mask

    def set_bits_to_use_per_byte_mask(self, bits_to_use_per_byte_mask):
        self.bits_to_use_per_byte_mask = bits_to_use_per_byte_mask
        self.blocks_and_const_xx_0.set_k(self.bits_to_use_per_byte_mask)
        self.blocks_and_const_xx_0_0.set_k(self.bits_to_use_per_byte_mask)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.blocks_multiply_const_vxx_0.set_k(self.gain)

    def get_bits_per_symbol(self):
        return self.bits_per_symbol

    def set_bits_per_symbol(self, bits_per_symbol):
        self.bits_per_symbol = bits_per_symbol
        self.set_M(2**self.bits_per_symbol)

    def get_tag(self):
        return self.tag

    def set_tag(self, tag):
        self.tag = tag
        self.blocks_vector_source_x_0.set_data(list(ord(i) for i in 'Zombie'), [self.tag])

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_polar(self):
        return self.polar

    def set_polar(self, polar):
        self.polar = polar
        self._polar_callback(self.polar)
        self.blocks_add_const_vxx_0.set_k(-self.polar*(self.M-1)+(1-self.polar)*0)
        self.blocks_add_const_vxx_1.set_k(self.polar*(self.M-1)-(1-self.polar)*0)
        self.blocks_char_to_float_0.set_scale(self.polar*0.5+(1-self.polar))
        self.blocks_float_to_char_0.set_scale(self.polar*0.5+(1-self.polar))

    def get_invert(self):
        return self.invert

    def set_invert(self, invert):
        self.invert = invert
        self._invert_callback(self.invert)

    def get_baud_delay(self):
        return self.baud_delay

    def set_baud_delay(self, baud_delay):
        self.baud_delay = baud_delay
        self.blocks_delay_0.set_dly(self.baud_delay)

    def get_M(self):
        return self.M

    def set_M(self, M):
        self.M = M
        self.blocks_add_const_vxx_0.set_k(-self.polar*(self.M-1)+(1-self.polar)*0)
        self.blocks_add_const_vxx_1.set_k(self.polar*(self.M-1)-(1-self.polar)*0)


def argument_parser():
    description = 'Conversion from bytes to M-ary symbols'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--bit-endianess", dest="bit_endianess", type=intx, default=1,
        help="Set LSB first [default=%(default)r]")
    parser.add_argument(
        "--bits-to-use-per-byte-mask", dest="bits_to_use_per_byte_mask", type=intx, default=255,
        help="Set Bits to use per byte mask [default=%(default)r]")
    parser.add_argument(
        "--gain", dest="gain", type=intx, default=1,
        help="Set Gain [default=%(default)r]")
    return parser


def main(top_block_cls=byte2sym, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(bit_endianess=options.bit_endianess, bits_to_use_per_byte_mask=options.bits_to_use_per_byte_mask, gain=options.gain)
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
