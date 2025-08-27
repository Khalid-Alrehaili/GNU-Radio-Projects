#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Doppler_Radar_USRP
# Author: Khalid Alrehaili
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import uhd
import time
from math import log10
from math import pi, cos
from scipy.constants import speed_of_light
import Doppler_Radar_USRP_calibration_module as calibration_module  # embedded python module
import Doppler_Radar_USRP_frequency_detector as frequency_detector  # embedded python module
import sip
import threading



class Doppler_Radar_USRP(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Doppler_Radar_USRP", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Doppler_Radar_USRP")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "Doppler_Radar_USRP")

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
        self.fc = fc = int(1.523e9)
        self.vector_length = vector_length = 1024*16
        self.threshold = threshold = -20
        self.samp_rate = samp_rate = int(1024*64)
        self.radar_angle = radar_angle = 0*pi/180
        self.lambda1 = lambda1 = speed_of_light/fc
        self.func = func = 0
        self.speed = speed = round(((frequency_detector.frequency_detector(func, vector_length, threshold))*samp_rate/vector_length-5e3)*lambda1, 2)/2*3.6/(cos(radar_angle))
        self.freq = freq = round((frequency_detector.frequency_detector(func, vector_length, threshold))*samp_rate/vector_length, 2)
        self.calibration_func_Mag1 = calibration_func_Mag1 = 0
        self.calibration_func_Arg1 = calibration_func_Arg1 = 0
        self.calibration = calibration = 0
        self.variable_qtgui_label_0_0 = variable_qtgui_label_0_0 = str(round(speed,2)) + " Km/h"
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = ": "+str(freq) + " Hz"
        self.tx_gain = tx_gain = 0.3
        self.delay = delay = 0
        self.decimation = decimation = 1
        self.comp_gain_A1 = comp_gain_A1 = calibration_module.Mag1(calibration, calibration_func_Mag1)
        self.comp_delay_A1 = comp_delay_A1 = calibration_module.Arg1(calibration, calibration_func_Arg1)
        self.amp = amp = 0

        ##################################################
        # Blocks
        ##################################################

        self._tx_gain_range = qtgui.Range(0, 1, 0.01, 0.3, 200)
        self._tx_gain_win = qtgui.RangeWidget(self._tx_gain_range, self.set_tx_gain, "tx_gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tx_gain_win)
        self.probe_signal = blocks.probe_signal_vf(vector_length)
        self._delay_range = qtgui.Range(-100, 100, 0.01, 0, 200)
        self._delay_win = qtgui.RangeWidget(self._delay_range, self.set_delay, "delay", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._delay_win)
        self._amp_range = qtgui.Range(0, 1, 0.01, 0, 200)
        self._amp_win = qtgui.RangeWidget(self._amp_range, self.set_amp, "amp", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._amp_win)
        self.Mag1 = blocks.probe_signal_f()
        self.Arg1 = blocks.probe_signal_f()
        self._variable_qtgui_label_0_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_0_0_formatter = None
        else:
            self._variable_qtgui_label_0_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_0_tool_bar.addWidget(Qt.QLabel("speed: "))
        self._variable_qtgui_label_0_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_0_formatter(self.variable_qtgui_label_0_0)))
        self._variable_qtgui_label_0_0_tool_bar.addWidget(self._variable_qtgui_label_0_0_label)
        self.top_layout.addWidget(self._variable_qtgui_label_0_0_tool_bar)
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_0_formatter = None
        else:
            self._variable_qtgui_label_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel("freq"))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_layout.addWidget(self._variable_qtgui_label_0_tool_bar)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_source_0.set_center_freq(fc, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_rx_agc(True, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0.set_center_freq(fc, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_normalized_gain(tx_gain, 0)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            vector_length,
            (-vector_length/2),
            1,
            "x-Axis",
            "y-Axis",
            "",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis((-10), 10)
        self.qtgui_vector_sink_f_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_win)
        def _func_probe():
          self.flowgraph_started.wait()
          while True:

            val = self.probe_signal.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_func,val))
              except AttributeError:
                self.set_func(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (60))
        _func_thread = threading.Thread(target=_func_probe)
        _func_thread.daemon = True
        _func_thread.start()
        self.fft_vxx_0 = fft.fft_vcc(vector_length, True, window.blackmanharris(vector_length), True, 1)
        def _calibration_func_Mag1_probe():
          self.flowgraph_started.wait()
          while True:

            val = self.Mag1.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_calibration_func_Mag1,val))
              except AttributeError:
                self.set_calibration_func_Mag1(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _calibration_func_Mag1_thread = threading.Thread(target=_calibration_func_Mag1_probe)
        _calibration_func_Mag1_thread.daemon = True
        _calibration_func_Mag1_thread.start()
        def _calibration_func_Arg1_probe():
          self.flowgraph_started.wait()
          while True:

            val = self.Arg1.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_calibration_func_Arg1,val))
              except AttributeError:
                self.set_calibration_func_Arg1(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _calibration_func_Arg1_thread = threading.Thread(target=_calibration_func_Arg1_probe)
        _calibration_func_Arg1_thread.daemon = True
        _calibration_func_Arg1_thread.start()
        _calibration_push_button = Qt.QPushButton('calibration')
        _calibration_push_button = Qt.QPushButton('calibration')
        self._calibration_choices = {'Pressed': 1, 'Released': 0}
        _calibration_push_button.pressed.connect(lambda: self.set_calibration(self._calibration_choices['Pressed']))
        _calibration_push_button.released.connect(lambda: self.set_calibration(self._calibration_choices['Released']))
        self.top_layout.addWidget(_calibration_push_button)
        self.blocks_sub_xx_0 = blocks.sub_cc(1)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vector_length)
        self.blocks_phase_shift_0 = blocks.phase_shift(-comp_delay_A1+delay, True)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, vector_length, (-10*log10(vector_length)))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(comp_gain_A1+amp)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(1, vector_length)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(vector_length)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)
        self.band_reject_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.band_reject(
                1,
                samp_rate,
                (5e3-10),
                (5e3+10),
                5,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                (5e3-800),
                (5e3+800),
                100,
                window.WIN_HAMMING,
                6.76))
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 5e3, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_phase_shift_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.band_reject_filter_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_complex_to_arg_0, 0), (self.Arg1, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.Mag1, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.probe_signal, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_complex_to_arg_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_phase_shift_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.band_reject_filter_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_sub_xx_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "Doppler_Radar_USRP")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.set_lambda1(speed_of_light/self.fc)
        self.uhd_usrp_sink_0.set_center_freq(self.fc, 0)
        self.uhd_usrp_source_0.set_center_freq(self.fc, 0)

    def get_vector_length(self):
        return self.vector_length

    def set_vector_length(self, vector_length):
        self.vector_length = vector_length
        self.set_freq(round((frequency_detector.frequency_detector(self.func, self.vector_length, self.threshold))*self.samp_rate/self.vector_length, 2))
        self.set_speed(round(((frequency_detector.frequency_detector(self.func, self.vector_length, self.threshold))*self.samp_rate/self.vector_length-5e3)*self.lambda1, 2)/2*3.6/(cos(self.radar_angle)))
        self.fft_vxx_0.set_window(window.blackmanharris(self.vector_length))
        self.qtgui_vector_sink_f_0.set_x_axis((-self.vector_length/2), 1)

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.set_freq(round((frequency_detector.frequency_detector(self.func, self.vector_length, self.threshold))*self.samp_rate/self.vector_length, 2))
        self.set_speed(round(((frequency_detector.frequency_detector(self.func, self.vector_length, self.threshold))*self.samp_rate/self.vector_length-5e3)*self.lambda1, 2)/2*3.6/(cos(self.radar_angle)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_freq(round((frequency_detector.frequency_detector(self.func, self.vector_length, self.threshold))*self.samp_rate/self.vector_length, 2))
        self.set_speed(round(((frequency_detector.frequency_detector(self.func, self.vector_length, self.threshold))*self.samp_rate/self.vector_length-5e3)*self.lambda1, 2)/2*3.6/(cos(self.radar_angle)))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, (5e3-800), (5e3+800), 100, window.WIN_HAMMING, 6.76))
        self.band_reject_filter_0.set_taps(firdes.band_reject(1, self.samp_rate, (5e3-10), (5e3+10), 5, window.WIN_HAMMING, 6.76))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_radar_angle(self):
        return self.radar_angle

    def set_radar_angle(self, radar_angle):
        self.radar_angle = radar_angle
        self.set_speed(round(((frequency_detector.frequency_detector(self.func, self.vector_length, self.threshold))*self.samp_rate/self.vector_length-5e3)*self.lambda1, 2)/2*3.6/(cos(self.radar_angle)))

    def get_lambda1(self):
        return self.lambda1

    def set_lambda1(self, lambda1):
        self.lambda1 = lambda1
        self.set_speed(round(((frequency_detector.frequency_detector(self.func, self.vector_length, self.threshold))*self.samp_rate/self.vector_length-5e3)*self.lambda1, 2)/2*3.6/(cos(self.radar_angle)))

    def get_func(self):
        return self.func

    def set_func(self, func):
        self.func = func
        self.set_freq(round((frequency_detector.frequency_detector(self.func, self.vector_length, self.threshold))*self.samp_rate/self.vector_length, 2))
        self.set_speed(round(((frequency_detector.frequency_detector(self.func, self.vector_length, self.threshold))*self.samp_rate/self.vector_length-5e3)*self.lambda1, 2)/2*3.6/(cos(self.radar_angle)))

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed
        self.set_variable_qtgui_label_0_0(str(round(self.speed,2)) + " Km/h")

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_variable_qtgui_label_0(": "+str(self.freq) + " Hz")

    def get_calibration_func_Mag1(self):
        return self.calibration_func_Mag1

    def set_calibration_func_Mag1(self, calibration_func_Mag1):
        self.calibration_func_Mag1 = calibration_func_Mag1
        self.set_comp_gain_A1(calibration_module.Mag1(self.calibration, self.calibration_func_Mag1))

    def get_calibration_func_Arg1(self):
        return self.calibration_func_Arg1

    def set_calibration_func_Arg1(self, calibration_func_Arg1):
        self.calibration_func_Arg1 = calibration_func_Arg1
        self.set_comp_delay_A1(calibration_module.Arg1(self.calibration, self.calibration_func_Arg1))

    def get_calibration(self):
        return self.calibration

    def set_calibration(self, calibration):
        self.calibration = calibration
        self.set_comp_delay_A1(calibration_module.Arg1(self.calibration, self.calibration_func_Arg1))
        self.set_comp_gain_A1(calibration_module.Mag1(self.calibration, self.calibration_func_Mag1))

    def get_variable_qtgui_label_0_0(self):
        return self.variable_qtgui_label_0_0

    def set_variable_qtgui_label_0_0(self, variable_qtgui_label_0_0):
        self.variable_qtgui_label_0_0 = variable_qtgui_label_0_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_0_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_0_0_formatter(self.variable_qtgui_label_0_0))))

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0))))

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_normalized_gain(self.tx_gain, 0)

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        self.blocks_phase_shift_0.set_shift(-self.comp_delay_A1+self.delay)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation

    def get_comp_gain_A1(self):
        return self.comp_gain_A1

    def set_comp_gain_A1(self, comp_gain_A1):
        self.comp_gain_A1 = comp_gain_A1
        self.blocks_multiply_const_vxx_0_0.set_k(self.comp_gain_A1+self.amp)

    def get_comp_delay_A1(self):
        return self.comp_delay_A1

    def set_comp_delay_A1(self, comp_delay_A1):
        self.comp_delay_A1 = comp_delay_A1
        self.blocks_phase_shift_0.set_shift(-self.comp_delay_A1+self.delay)

    def get_amp(self):
        return self.amp

    def set_amp(self, amp):
        self.amp = amp
        self.blocks_multiply_const_vxx_0_0.set_k(self.comp_gain_A1+self.amp)




def main(top_block_cls=Doppler_Radar_USRP, options=None):

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
