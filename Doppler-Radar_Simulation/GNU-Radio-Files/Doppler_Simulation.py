#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Doppler Radar Simulation
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
import math
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from math import log10
from math import pi
from scipy.constants import c
import Doppler_Simulation_frequency_detector_0 as frequency_detector_0  # embedded python module
import myobjects
import threading
import time



class Doppler_Simulation(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Doppler Radar Simulation", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Doppler Radar Simulation")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "Doppler_Simulation")

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
        self.func_0 = func_0 = 0
        self.fc = fc = int(2.4e9)
        self.lambda1 = lambda1 = c/fc
        self.freq_0 = freq_0 = round(frequency_detector_0.frequency_detector(func_0),2)
        self.speed_0 = speed_0 = freq_0*lambda1/2*3.6
        self.vector_length = vector_length = 1024*128*2
        self.variable_qtgui_label_0_1 = variable_qtgui_label_0_1 = str(round(freq_0, 2))+" Hz"
        self.variable_qtgui_label_0_0_0 = variable_qtgui_label_0_0_0 = str(round(speed_0, 2))+" Km/h"
        self.threshold = threshold = -100
        self.samp_rate = samp_rate = (4.9e9)
        self.object1 = object1 = myobjects.object([0, 0, 10], -40/3.6,1)
        self.decimation = decimation = 100

        ##################################################
        # Blocks
        ##################################################

        self.probe_signal_0 = blocks.probe_signal_f()
        self._variable_qtgui_label_0_1_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_0_1_formatter = None
        else:
            self._variable_qtgui_label_0_1_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_1_tool_bar.addWidget(Qt.QLabel("doppler shift: "))
        self._variable_qtgui_label_0_1_label = Qt.QLabel(str(self._variable_qtgui_label_0_1_formatter(self.variable_qtgui_label_0_1)))
        self._variable_qtgui_label_0_1_tool_bar.addWidget(self._variable_qtgui_label_0_1_label)
        self.top_layout.addWidget(self._variable_qtgui_label_0_1_tool_bar)
        self._variable_qtgui_label_0_0_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_0_0_0_formatter = None
        else:
            self._variable_qtgui_label_0_0_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_0_0_tool_bar.addWidget(Qt.QLabel("speed: "))
        self._variable_qtgui_label_0_0_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_0_0_formatter(self.variable_qtgui_label_0_0_0)))
        self._variable_qtgui_label_0_0_0_tool_bar.addWidget(self._variable_qtgui_label_0_0_0_label)
        self.top_layout.addWidget(self._variable_qtgui_label_0_0_0_tool_bar)
        def _func_0_probe():
          self.flowgraph_started.wait()
          while True:

            val = self.probe_signal_0.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_func_0,val))
              except AttributeError:
                self.set_func_0(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _func_0_thread = threading.Thread(target=_func_0_probe)
        _func_0_thread.daemon = True
        _func_0_thread.start()
        self.fir_filter_xxx_0 = filter.fir_filter_ccf(decimation, [1])
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((samp_rate/(2*pi*decimation)))
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_freqshift_cc_0 = blocks.rotator_cc(2.0*math.pi*object1.frequency_shift(fc)/samp_rate)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, (int(object1.distance()*2*samp_rate/c)))
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, fc, 1, 0, 0)
        self.analog_pll_freqdet_cf_0 = analog.pll_freqdet_cf((pi/100000), (pi/2), (-pi/2))
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 0.0001, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_pll_freqdet_cf_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_freqshift_cc_0, 0))
        self.connect((self.blocks_freqshift_cc_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.probe_signal_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.fir_filter_xxx_0, 0), (self.analog_pll_freqdet_cf_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "Doppler_Simulation")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_func_0(self):
        return self.func_0

    def set_func_0(self, func_0):
        self.func_0 = func_0
        self.set_freq_0(round(frequency_detector_0.frequency_detector(self.func_0),2))

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.set_lambda1(c/self.fc)
        self.analog_sig_source_x_0.set_frequency(self.fc)
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*object1.frequency_shift(self.fc)/self.samp_rate)
        self.blocks_multiply_const_vxx_1.set_k(1/((object1.FSPL(self.fc))))

    def get_lambda1(self):
        return self.lambda1

    def set_lambda1(self, lambda1):
        self.lambda1 = lambda1
        self.set_speed_0(self.freq_0*self.lambda1/2*3.6)

    def get_freq_0(self):
        return self.freq_0

    def set_freq_0(self, freq_0):
        self.freq_0 = freq_0
        self.set_speed_0(self.freq_0*self.lambda1/2*3.6)
        self.set_variable_qtgui_label_0_1(str(round(self.freq_0, 2))+" Hz")

    def get_speed_0(self):
        return self.speed_0

    def set_speed_0(self, speed_0):
        self.speed_0 = speed_0
        self.set_variable_qtgui_label_0_0_0(str(round(self.speed_0, 2))+" Km/h")

    def get_vector_length(self):
        return self.vector_length

    def set_vector_length(self, vector_length):
        self.vector_length = vector_length

    def get_variable_qtgui_label_0_1(self):
        return self.variable_qtgui_label_0_1

    def set_variable_qtgui_label_0_1(self, variable_qtgui_label_0_1):
        self.variable_qtgui_label_0_1 = variable_qtgui_label_0_1
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_1_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_0_1_formatter(self.variable_qtgui_label_0_1))))

    def get_variable_qtgui_label_0_0_0(self):
        return self.variable_qtgui_label_0_0_0

    def set_variable_qtgui_label_0_0_0(self, variable_qtgui_label_0_0_0):
        self.variable_qtgui_label_0_0_0 = variable_qtgui_label_0_0_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_0_0_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_0_0_0_formatter(self.variable_qtgui_label_0_0_0))))

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_delay_0.set_dly(int((int(object1.distance()*2*self.samp_rate/c))))
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*object1.frequency_shift(self.fc)/self.samp_rate)
        self.blocks_multiply_const_vxx_0.set_k((self.samp_rate/(2*pi*self.decimation)))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)

    def get_object1(self):
        return self.object1

    def set_object1(self, object1):
        self.object1 = object1

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.blocks_multiply_const_vxx_0.set_k((self.samp_rate/(2*pi*self.decimation)))




def main(top_block_cls=Doppler_Simulation, options=None):

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
