#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: AM_Transmitter_ADALM_PLUTO
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
from gnuradio import iio
import sip
import threading



class AM_Transmitter_ADALM_PLUTO(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "AM_Transmitter_ADALM_PLUTO", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("AM_Transmitter_ADALM_PLUTO")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "AM_Transmitter_ADALM_PLUTO")

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
        self.interpolation = interpolation = 2
        self.samp_rate = samp_rate = int(48e3*interpolation)
        self.freq_Tx = freq_Tx = (1.234e9)
        self.adjust = adjust = 0
        self.Tx_Attenuation = Tx_Attenuation = 10

        ##################################################
        # Blocks
        ##################################################

        self._freq_Tx_range = qtgui.Range(47e6, 6e9, 1e6, (1.234e9), 200)
        self._freq_Tx_win = qtgui.RangeWidget(self._freq_Tx_range, self.set_freq_Tx, "freq_Tx", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq_Tx_win)
        self._Tx_Attenuation_range = qtgui.Range(0, 89, 1, 10, 200)
        self._Tx_Attenuation_win = qtgui.RangeWidget(self._Tx_Attenuation_range, self.set_Tx_Attenuation, "'Tx_Attenuation'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Tx_Attenuation_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Transmitted Signal", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.qtgui_sink_x_0.set_block_alias("Transmitted Signal")
        self.low_pass_filter_0 = filter.interp_fir_filter_fff(
            interpolation,
            firdes.low_pass(
                2,
                (samp_rate/2),
                10e3,
                1e3,
                window.WIN_HAMMING,
                6.76))
        self.iio_pluto_sink_0 = iio.fmcomms2_sink_fc32('' if '' else iio.get_pluto_uri(), [True, True], 32768, False)
        self.iio_pluto_sink_0.set_len_tag_key('')
        self.iio_pluto_sink_0.set_bandwidth(int(20e6))
        self.iio_pluto_sink_0.set_frequency(int(freq_Tx))
        self.iio_pluto_sink_0.set_samplerate(samp_rate)
        self.iio_pluto_sink_0.set_attenuation(0, Tx_Attenuation)
        self.iio_pluto_sink_0.set_filter_params('Auto', '', 0, 0)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('audio.mp3', True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(0.1)
        self._adjust_range = qtgui.Range(-100e3, 100e3, 0.1, 0, 200)
        self._adjust_win = qtgui.RangeWidget(self._adjust_range, self.set_adjust, "adjust", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._adjust_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_const_vxx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "AM_Transmitter_ADALM_PLUTO")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_interpolation(self):
        return self.interpolation

    def set_interpolation(self, interpolation):
        self.interpolation = interpolation
        self.set_samp_rate(int(48e3*self.interpolation))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.iio_pluto_sink_0.set_samplerate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(2, (self.samp_rate/2), 10e3, 1e3, window.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_freq_Tx(self):
        return self.freq_Tx

    def set_freq_Tx(self, freq_Tx):
        self.freq_Tx = freq_Tx
        self.iio_pluto_sink_0.set_frequency(int(self.freq_Tx))

    def get_adjust(self):
        return self.adjust

    def set_adjust(self, adjust):
        self.adjust = adjust

    def get_Tx_Attenuation(self):
        return self.Tx_Attenuation

    def set_Tx_Attenuation(self, Tx_Attenuation):
        self.Tx_Attenuation = Tx_Attenuation
        self.iio_pluto_sink_0.set_attenuation(0,self.Tx_Attenuation)




def main(top_block_cls=AM_Transmitter_ADALM_PLUTO, options=None):

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
