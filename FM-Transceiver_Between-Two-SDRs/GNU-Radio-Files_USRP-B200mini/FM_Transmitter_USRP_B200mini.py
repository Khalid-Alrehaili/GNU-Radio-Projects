#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FM_Transmitter_USRP-B200mini
# Author: Khalid Alrehaili
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from math import pi
import threading



class FM_Transmitter_USRP_B200mini(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FM_Transmitter_USRP-B200mini", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FM_Transmitter_USRP-B200mini")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "FM_Transmitter_USRP_B200mini")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = int(48e3)
        self.interpolation = interpolation = 4
        self.quad_rate = quad_rate = samp_rate*interpolation
        self.freq_Tx = freq_Tx = int(1.59e9)
        self.audio_filter = audio_filter = firdes.low_pass(interpolation, quad_rate, quad_rate/(interpolation*2), quad_rate/(interpolation*4), window.WIN_HAMMING, 6.76)
        self.Gain = Gain = 0.5

        ##################################################
        # Blocks
        ##################################################

        self._freq_Tx_range = qtgui.Range(47e6, 6e9, 25e6, int(1.59e9), 200)
        self._freq_Tx_win = qtgui.RangeWidget(self._freq_Tx_range, self.set_freq_Tx, "freq_Tx", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq_Tx_win)
        self._Gain_range = qtgui.Range(0, 1, 0.01, 0.5, 200)
        self._Gain_win = qtgui.RangeWidget(self._Gain_range, self.set_Gain, "Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Gain_win)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(quad_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0.set_center_freq(freq_Tx, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(160e3, 0)
        self.uhd_usrp_sink_0.set_normalized_gain(Gain, 0)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(interpolation, audio_filter)
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('audio.mp3', True)
        self.blocks_vco_c_0_0 = blocks.vco_c(quad_rate, (2*pi*75e3), 1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vco_c_0_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_vco_c_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "FM_Transmitter_USRP_B200mini")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_quad_rate(self.samp_rate*self.interpolation)

    def get_interpolation(self):
        return self.interpolation

    def set_interpolation(self, interpolation):
        self.interpolation = interpolation
        self.set_audio_filter(firdes.low_pass(self.interpolation, self.quad_rate, self.quad_rate/(self.interpolation*2), self.quad_rate/(self.interpolation*4), window.WIN_HAMMING, 6.76))
        self.set_quad_rate(self.samp_rate*self.interpolation)

    def get_quad_rate(self):
        return self.quad_rate

    def set_quad_rate(self, quad_rate):
        self.quad_rate = quad_rate
        self.set_audio_filter(firdes.low_pass(self.interpolation, self.quad_rate, self.quad_rate/(self.interpolation*2), self.quad_rate/(self.interpolation*4), window.WIN_HAMMING, 6.76))
        self.uhd_usrp_sink_0.set_samp_rate(self.quad_rate)

    def get_freq_Tx(self):
        return self.freq_Tx

    def set_freq_Tx(self, freq_Tx):
        self.freq_Tx = freq_Tx
        self.uhd_usrp_sink_0.set_center_freq(self.freq_Tx, 0)

    def get_audio_filter(self):
        return self.audio_filter

    def set_audio_filter(self, audio_filter):
        self.audio_filter = audio_filter
        self.interp_fir_filter_xxx_0.set_taps(self.audio_filter)

    def get_Gain(self):
        return self.Gain

    def set_Gain(self, Gain):
        self.Gain = Gain
        self.uhd_usrp_sink_0.set_normalized_gain(self.Gain, 0)




def main(top_block_cls=FM_Transmitter_USRP_B200mini, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
