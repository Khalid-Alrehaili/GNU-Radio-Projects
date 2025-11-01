#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: kald0n
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import audio
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
from math import pi
import threading



class testing(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "testing")

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
        self.samp_rate = samp_rate = 48000
        self.interpolation = interpolation = 10
        self.samp_rate_interpolated = samp_rate_interpolated = samp_rate * interpolation
        self.freq1 = freq1 = 0
        self.bandwidth_loob = bandwidth_loob = pi/10
        self.audio_filter_1 = audio_filter_1 = firdes.low_pass(1, samp_rate_interpolated, samp_rate_interpolated/(interpolation*2), samp_rate_interpolated/(interpolation*4), window.WIN_HAMMING, 6.76)
        self.audio_filter = audio_filter = firdes.low_pass(10, samp_rate_interpolated, samp_rate_interpolated/(interpolation*2), samp_rate_interpolated/(interpolation*4), window.WIN_HAMMING, 6.76)
        self.Switch = Switch = 0

        ##################################################
        # Blocks
        ##################################################

        self._bandwidth_loob_range = qtgui.Range(pi/1000, pi, pi/1000, pi/10, 200)
        self._bandwidth_loob_win = qtgui.RangeWidget(self._bandwidth_loob_range, self.set_bandwidth_loob, "bandwidth_loob", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._bandwidth_loob_win)
        self._Switch_range = qtgui.Range(0, 2, 1, 0, 200)
        self._Switch_win = qtgui.RangeWidget(self._Switch_range, self.set_Switch, "Switch", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Switch_win)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(10, audio_filter)
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self._freq1_range = qtgui.Range(-75e3, 75e3, 1, 0, 200)
        self._freq1_win = qtgui.RangeWidget(self._freq1_range, self.set_freq1, "freq1", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq1_win)
        self.fir_filter_xxx_0 = filter.fir_filter_fff(interpolation, audio_filter_1)
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/kald0n/Downloads/gitfiles/GNU-Radio-Projects/FM-Transceiver_Between-Two-SDRs/GNU-Radio-Files_ADALM-PLUTO/audio.mp3', True)
        self.blocks_vco_c_0 = blocks.vco_c((samp_rate*10), (2*pi*75e3), 1)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*1,Switch,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((samp_rate/75e3*1/(2*pi)*10))
        self.audio_sink_0 = audio.sink(samp_rate, 'plughw:1,0', True)
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=samp_rate,
        	quad_rate=samp_rate_interpolated,
        	tau=(75e-6),
        	max_dev=75e3,
        	fh=(-1.0),
        )
        self.analog_pll_freqdet_cf_0 = analog.pll_freqdet_cf(bandwidth_loob, pi, (-pi))
        self.analog_nbfm_rx_0_0 = analog.nbfm_rx(
        	audio_rate=48000,
        	quad_rate=480000,
        	tau=(75e-6),
        	max_dev=75e3,
          )
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=48000,
        	quad_rate=480000,
        	tau=(75e-6),
        	max_dev=75e3,
          )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.analog_nbfm_rx_0_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.analog_pll_freqdet_cf_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_wfm_tx_0, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_vco_c_0, 0), (self.analog_nbfm_rx_0_0, 0))
        self.connect((self.blocks_vco_c_0, 0), (self.analog_pll_freqdet_cf_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.analog_wfm_tx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_selector_0, 2))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_vco_c_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "testing")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_rate_interpolated(self.samp_rate * self.interpolation)
        self.blocks_multiply_const_vxx_0.set_k((self.samp_rate/75e3*1/(2*pi)*10))

    def get_interpolation(self):
        return self.interpolation

    def set_interpolation(self, interpolation):
        self.interpolation = interpolation
        self.set_audio_filter(firdes.low_pass(10, self.samp_rate_interpolated, self.samp_rate_interpolated/(self.interpolation*2), self.samp_rate_interpolated/(self.interpolation*4), window.WIN_HAMMING, 6.76))
        self.set_audio_filter_1(firdes.low_pass(1, self.samp_rate_interpolated, self.samp_rate_interpolated/(self.interpolation*2), self.samp_rate_interpolated/(self.interpolation*4), window.WIN_HAMMING, 6.76))
        self.set_samp_rate_interpolated(self.samp_rate * self.interpolation)

    def get_samp_rate_interpolated(self):
        return self.samp_rate_interpolated

    def set_samp_rate_interpolated(self, samp_rate_interpolated):
        self.samp_rate_interpolated = samp_rate_interpolated
        self.set_audio_filter(firdes.low_pass(10, self.samp_rate_interpolated, self.samp_rate_interpolated/(self.interpolation*2), self.samp_rate_interpolated/(self.interpolation*4), window.WIN_HAMMING, 6.76))
        self.set_audio_filter_1(firdes.low_pass(1, self.samp_rate_interpolated, self.samp_rate_interpolated/(self.interpolation*2), self.samp_rate_interpolated/(self.interpolation*4), window.WIN_HAMMING, 6.76))

    def get_freq1(self):
        return self.freq1

    def set_freq1(self, freq1):
        self.freq1 = freq1

    def get_bandwidth_loob(self):
        return self.bandwidth_loob

    def set_bandwidth_loob(self, bandwidth_loob):
        self.bandwidth_loob = bandwidth_loob
        self.analog_pll_freqdet_cf_0.set_loop_bandwidth(self.bandwidth_loob)

    def get_audio_filter_1(self):
        return self.audio_filter_1

    def set_audio_filter_1(self, audio_filter_1):
        self.audio_filter_1 = audio_filter_1
        self.fir_filter_xxx_0.set_taps(self.audio_filter_1)

    def get_audio_filter(self):
        return self.audio_filter

    def set_audio_filter(self, audio_filter):
        self.audio_filter = audio_filter
        self.interp_fir_filter_xxx_0.set_taps(self.audio_filter)

    def get_Switch(self):
        return self.Switch

    def set_Switch(self, Switch):
        self.Switch = Switch
        self.blocks_selector_0.set_input_index(self.Switch)




def main(top_block_cls=testing, options=None):

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
