#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FMCW_Radar
# Author: Khalid Alrehaili, Hatem Aljuhani, Mohammed Atif
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
from scipy.constants import speed_of_light
import FMCW_Radar_avg_beat as avg_beat  # embedded python module
import FMCW_Radar_beat_detection as beat_detection  # embedded python module
import FMCW_Radar_beat_detection_0 as beat_detection_0  # embedded python module
import FMCW_Radar_object_module as object_module  # embedded python module
import myobjects
import threading
import time



class FMCW_Radar(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FMCW_Radar", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FMCW_Radar")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "FMCW_Radar")

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
        self.tri_prob_func_0 = tri_prob_func_0 = 0
        self.tri_prob_func = tri_prob_func = 0
        self.probe_func_0 = probe_func_0 = 0
        self.avg_upbeat = avg_upbeat = avg_beat.upbeat_detect(beat_detection.detect(tri_prob_func), probe_func_0)
        self.avg_downbeat = avg_downbeat = avg_beat.downbeat_detect(beat_detection_0.detect(tri_prob_func_0), probe_func_0)
        self.PRF = PRF = 2560
        self.Bandwidth = Bandwidth = 6e6*5
        self.signal_freq = signal_freq = 2.4e9
        self.probe_func = probe_func = 0
        self.distance_calculated = distance_calculated = avg_beat.distance_calculator(Bandwidth, PRF, avg_downbeat, avg_upbeat)
        self.velocity_gui = velocity_gui = round(avg_beat.Velocity_calculator(signal_freq,avg_downbeat,avg_upbeat), 2)
        self.velocity_calculated = velocity_calculated = avg_beat.Velocity_calculator(signal_freq,avg_downbeat,avg_upbeat)
        self.upbeat_gui = upbeat_gui = int(avg_upbeat)
        self.samp_rate = samp_rate = 10e9
        self.power = power = 10000
        self.pi = pi = math.pi
        self.object1 = object1 = object_module.object([0, 0, 30], -20,10)
        self.downbeat_gui = downbeat_gui = int(avg_downbeat)
        self.distance_gui = distance_gui = round(distance_calculated,2)
        self.decimation = decimation = 256*1.5
        self.beatfrequency_gui = beatfrequency_gui = int(probe_func)
        self.anntena_gain = anntena_gain = 500

        ##################################################
        # Blocks
        ##################################################

        self.tri_prob_0 = blocks.probe_signal_f()
        self.tri_prob = blocks.probe_signal_f()
        self.probe_signal = blocks.probe_signal_f()
        self._velocity_gui_tool_bar = Qt.QToolBar(self)

        if None:
            self._velocity_gui_formatter = None
        else:
            self._velocity_gui_formatter = lambda x: eng_notation.num_to_str(x)

        self._velocity_gui_tool_bar.addWidget(Qt.QLabel("Velocity (m/s): "))
        self._velocity_gui_label = Qt.QLabel(str(self._velocity_gui_formatter(self.velocity_gui)))
        self._velocity_gui_tool_bar.addWidget(self._velocity_gui_label)
        self.top_grid_layout.addWidget(self._velocity_gui_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._upbeat_gui_tool_bar = Qt.QToolBar(self)

        if None:
            self._upbeat_gui_formatter = None
        else:
            self._upbeat_gui_formatter = lambda x: str(x)

        self._upbeat_gui_tool_bar.addWidget(Qt.QLabel("average beat (+): "))
        self._upbeat_gui_label = Qt.QLabel(str(self._upbeat_gui_formatter(self.upbeat_gui)))
        self._upbeat_gui_tool_bar.addWidget(self._upbeat_gui_label)
        self.top_grid_layout.addWidget(self._upbeat_gui_tool_bar, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        def _tri_prob_func_0_probe():
          self.flowgraph_started.wait()
          while True:

            val = self.tri_prob_0.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_tri_prob_func_0,val))
              except AttributeError:
                self.set_tri_prob_func_0(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _tri_prob_func_0_thread = threading.Thread(target=_tri_prob_func_0_probe)
        _tri_prob_func_0_thread.daemon = True
        _tri_prob_func_0_thread.start()
        def _tri_prob_func_probe():
          self.flowgraph_started.wait()
          while True:

            val = self.tri_prob.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_tri_prob_func,val))
              except AttributeError:
                self.set_tri_prob_func(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _tri_prob_func_thread = threading.Thread(target=_tri_prob_func_probe)
        _tri_prob_func_thread.daemon = True
        _tri_prob_func_thread.start()
        def _probe_func_0_probe():
          self.flowgraph_started.wait()
          while True:

            val = self.probe_signal.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_probe_func_0,val))
              except AttributeError:
                self.set_probe_func_0(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _probe_func_0_thread = threading.Thread(target=_probe_func_0_probe)
        _probe_func_0_thread.daemon = True
        _probe_func_0_thread.start()
        def _probe_func_probe():
          self.flowgraph_started.wait()
          while True:

            val = self.probe_signal.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_probe_func,val))
              except AttributeError:
                self.set_probe_func(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _probe_func_thread = threading.Thread(target=_probe_func_probe)
        _probe_func_thread.daemon = True
        _probe_func_thread.start()
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                5e9,
                1e6,
                window.WIN_HAMMING,
                6.76))
        self.fir_filter_xxx_0_0_0 = filter.fir_filter_fff(64, [1])
        self.fir_filter_xxx_0_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(int(decimation), [1])
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.filter_fft_low_pass_filter_0 = filter.fft_filter_ccc(1, firdes.low_pass(1, (samp_rate/decimation), 2.4e6, 1e6, window.WIN_HAMMING, 6.76), 4)
        self._downbeat_gui_tool_bar = Qt.QToolBar(self)

        if None:
            self._downbeat_gui_formatter = None
        else:
            self._downbeat_gui_formatter = lambda x: str(x)

        self._downbeat_gui_tool_bar.addWidget(Qt.QLabel("average beat (-):  "))
        self._downbeat_gui_label = Qt.QLabel(str(self._downbeat_gui_formatter(self.downbeat_gui)))
        self._downbeat_gui_tool_bar.addWidget(self._downbeat_gui_label)
        self.top_grid_layout.addWidget(self._downbeat_gui_tool_bar, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._distance_gui_tool_bar = Qt.QToolBar(self)

        if None:
            self._distance_gui_formatter = None
        else:
            self._distance_gui_formatter = lambda x: eng_notation.num_to_str(x)

        self._distance_gui_tool_bar.addWidget(Qt.QLabel("Distance (m): "))
        self._distance_gui_label = Qt.QLabel(str(self._distance_gui_formatter(self.distance_gui)))
        self._distance_gui_tool_bar.addWidget(self._distance_gui_label)
        self.top_grid_layout.addWidget(self._distance_gui_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_vco_c_0 = blocks.vco_c(samp_rate, (2*pi*signal_freq), (power/1000))
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_multiply_const_vxx_2_0_0 = blocks.multiply_const_cc(1/(object1.FSPL(signal_freq)))
        self.blocks_multiply_const_vxx_2_0 = blocks.multiply_const_cc(1/(object1.FSPL(signal_freq)))
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_cc(math.sqrt(anntena_gain))
        self.blocks_multiply_const_vxx_1_1 = blocks.multiply_const_cc(math.sqrt(57))
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_ff((samp_rate/(2*pi)/decimation))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(math.sqrt(57))
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff((int(samp_rate/100000/decimation)), (1/(samp_rate/100000/decimation)), 40000, 1)
        self.blocks_freqshift_cc_0 = blocks.rotator_cc(2.0*math.pi*object1.frequency_shift(signal_freq)/samp_rate)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, (int(object1.distance()*2*samp_rate/speed_of_light)))
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self._beatfrequency_gui_tool_bar = Qt.QToolBar(self)

        if None:
            self._beatfrequency_gui_formatter = None
        else:
            self._beatfrequency_gui_formatter = lambda x: str(x)

        self._beatfrequency_gui_tool_bar.addWidget(Qt.QLabel("Beat Frequency (Hz): "))
        self._beatfrequency_gui_label = Qt.QLabel(str(self._beatfrequency_gui_formatter(self.beatfrequency_gui)))
        self._beatfrequency_gui_tool_bar.addWidget(self._beatfrequency_gui_label)
        self.top_grid_layout.addWidget(self._beatfrequency_gui_tool_bar, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.band_pass_filter_0_0 = filter.fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                1,
                samp_rate,
                2.38e9,
                2.42e9,
                5e6,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0 = filter.fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                1,
                samp_rate,
                2.38e9,
                2.42e9,
                5e6,
                window.WIN_HAMMING,
                6.76))
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_TRI_WAVE, PRF, ((Bandwidth / signal_freq)), ((1 - (Bandwidth / (signal_freq*2)))), 0)
        self.analog_pll_freqdet_cf_0_0 = analog.pll_freqdet_cf((pi/50), (pi/200), (-pi/200))
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 0.001, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_pll_freqdet_cf_0_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_freqshift_cc_0, 0))
        self.connect((self.blocks_freqshift_cc_0, 0), (self.blocks_multiply_const_vxx_2_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_multiply_const_vxx_1_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.probe_signal, 0))
        self.connect((self.blocks_multiply_const_vxx_1_1, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.blocks_multiply_const_vxx_2_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2_0_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_vco_c_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.fir_filter_xxx_0_0_0, 0))
        self.connect((self.blocks_vco_c_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0, 0), (self.analog_pll_freqdet_cf_0_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.filter_fft_low_pass_filter_0, 0))
        self.connect((self.fir_filter_xxx_0_0_0, 0), (self.tri_prob, 0))
        self.connect((self.fir_filter_xxx_0_0_0, 0), (self.tri_prob_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_const_vxx_2, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "FMCW_Radar")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_tri_prob_func_0(self):
        return self.tri_prob_func_0

    def set_tri_prob_func_0(self, tri_prob_func_0):
        self.tri_prob_func_0 = tri_prob_func_0
        self.set_avg_downbeat(avg_beat.downbeat_detect(beat_detection_0.detect(self.tri_prob_func_0), self.probe_func_0))

    def get_tri_prob_func(self):
        return self.tri_prob_func

    def set_tri_prob_func(self, tri_prob_func):
        self.tri_prob_func = tri_prob_func
        self.set_avg_upbeat(avg_beat.upbeat_detect(beat_detection.detect(self.tri_prob_func), self.probe_func_0))

    def get_probe_func_0(self):
        return self.probe_func_0

    def set_probe_func_0(self, probe_func_0):
        self.probe_func_0 = probe_func_0
        self.set_avg_downbeat(avg_beat.downbeat_detect(beat_detection_0.detect(self.tri_prob_func_0), self.probe_func_0))
        self.set_avg_upbeat(avg_beat.upbeat_detect(beat_detection.detect(self.tri_prob_func), self.probe_func_0))

    def get_avg_upbeat(self):
        return self.avg_upbeat

    def set_avg_upbeat(self, avg_upbeat):
        self.avg_upbeat = avg_upbeat
        self.set_distance_calculated(avg_beat.distance_calculator(self.Bandwidth, self.PRF, self.avg_downbeat, self.avg_upbeat))
        self.set_upbeat_gui(int(self.avg_upbeat))
        self.set_velocity_calculated(avg_beat.Velocity_calculator(self.signal_freq,self.avg_downbeat,self.avg_upbeat))
        self.set_velocity_gui(round(avg_beat.Velocity_calculator(self.signal_freq,self.avg_downbeat,self.avg_upbeat), 2))

    def get_avg_downbeat(self):
        return self.avg_downbeat

    def set_avg_downbeat(self, avg_downbeat):
        self.avg_downbeat = avg_downbeat
        self.set_distance_calculated(avg_beat.distance_calculator(self.Bandwidth, self.PRF, self.avg_downbeat, self.avg_upbeat))
        self.set_downbeat_gui(int(self.avg_downbeat))
        self.set_velocity_calculated(avg_beat.Velocity_calculator(self.signal_freq,self.avg_downbeat,self.avg_upbeat))
        self.set_velocity_gui(round(avg_beat.Velocity_calculator(self.signal_freq,self.avg_downbeat,self.avg_upbeat), 2))

    def get_PRF(self):
        return self.PRF

    def set_PRF(self, PRF):
        self.PRF = PRF
        self.set_distance_calculated(avg_beat.distance_calculator(self.Bandwidth, self.PRF, self.avg_downbeat, self.avg_upbeat))
        self.analog_sig_source_x_0.set_frequency(self.PRF)

    def get_Bandwidth(self):
        return self.Bandwidth

    def set_Bandwidth(self, Bandwidth):
        self.Bandwidth = Bandwidth
        self.set_distance_calculated(avg_beat.distance_calculator(self.Bandwidth, self.PRF, self.avg_downbeat, self.avg_upbeat))
        self.analog_sig_source_x_0.set_amplitude(((self.Bandwidth / self.signal_freq)))
        self.analog_sig_source_x_0.set_offset(((1 - (self.Bandwidth / (self.signal_freq*2)))))

    def get_signal_freq(self):
        return self.signal_freq

    def set_signal_freq(self, signal_freq):
        self.signal_freq = signal_freq
        self.set_velocity_calculated(avg_beat.Velocity_calculator(self.signal_freq,self.avg_downbeat,self.avg_upbeat))
        self.set_velocity_gui(round(avg_beat.Velocity_calculator(self.signal_freq,self.avg_downbeat,self.avg_upbeat), 2))
        self.analog_sig_source_x_0.set_amplitude(((self.Bandwidth / self.signal_freq)))
        self.analog_sig_source_x_0.set_offset(((1 - (self.Bandwidth / (self.signal_freq*2)))))
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*object1.frequency_shift(self.signal_freq)/self.samp_rate)
        self.blocks_multiply_const_vxx_2_0.set_k(1/(object1.FSPL(self.signal_freq)))
        self.blocks_multiply_const_vxx_2_0_0.set_k(1/(object1.FSPL(self.signal_freq)))

    def get_probe_func(self):
        return self.probe_func

    def set_probe_func(self, probe_func):
        self.probe_func = probe_func
        self.set_beatfrequency_gui(int(self.probe_func))

    def get_distance_calculated(self):
        return self.distance_calculated

    def set_distance_calculated(self, distance_calculated):
        self.distance_calculated = distance_calculated
        self.set_distance_gui(round(self.distance_calculated,2))

    def get_velocity_gui(self):
        return self.velocity_gui

    def set_velocity_gui(self, velocity_gui):
        self.velocity_gui = velocity_gui
        Qt.QMetaObject.invokeMethod(self._velocity_gui_label, "setText", Qt.Q_ARG("QString", str(self._velocity_gui_formatter(self.velocity_gui))))

    def get_velocity_calculated(self):
        return self.velocity_calculated

    def set_velocity_calculated(self, velocity_calculated):
        self.velocity_calculated = velocity_calculated

    def get_upbeat_gui(self):
        return self.upbeat_gui

    def set_upbeat_gui(self, upbeat_gui):
        self.upbeat_gui = upbeat_gui
        Qt.QMetaObject.invokeMethod(self._upbeat_gui_label, "setText", Qt.Q_ARG("QString", str(self._upbeat_gui_formatter(self.upbeat_gui))))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, 2.38e9, 2.42e9, 5e6, window.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, 2.38e9, 2.42e9, 5e6, window.WIN_HAMMING, 6.76))
        self.blocks_delay_0.set_dly(int((int(object1.distance()*2*self.samp_rate/speed_of_light))))
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*object1.frequency_shift(self.signal_freq)/self.samp_rate)
        self.blocks_moving_average_xx_0.set_length_and_scale((int(self.samp_rate/100000/self.decimation)), (1/(self.samp_rate/100000/self.decimation)))
        self.blocks_multiply_const_vxx_0_0_0.set_k((self.samp_rate/(2*self.pi)/self.decimation))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.filter_fft_low_pass_filter_0.set_taps(firdes.low_pass(1, (self.samp_rate/self.decimation), 2.4e6, 1e6, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 5e9, 1e6, window.WIN_HAMMING, 6.76))

    def get_power(self):
        return self.power

    def set_power(self, power):
        self.power = power

    def get_pi(self):
        return self.pi

    def set_pi(self, pi):
        self.pi = pi
        self.analog_pll_freqdet_cf_0_0.set_loop_bandwidth((self.pi/50))
        self.analog_pll_freqdet_cf_0_0.set_max_freq((self.pi/200))
        self.analog_pll_freqdet_cf_0_0.set_min_freq((-self.pi/200))
        self.blocks_multiply_const_vxx_0_0_0.set_k((self.samp_rate/(2*self.pi)/self.decimation))

    def get_object1(self):
        return self.object1

    def set_object1(self, object1):
        self.object1 = object1

    def get_downbeat_gui(self):
        return self.downbeat_gui

    def set_downbeat_gui(self, downbeat_gui):
        self.downbeat_gui = downbeat_gui
        Qt.QMetaObject.invokeMethod(self._downbeat_gui_label, "setText", Qt.Q_ARG("QString", str(self._downbeat_gui_formatter(self.downbeat_gui))))

    def get_distance_gui(self):
        return self.distance_gui

    def set_distance_gui(self, distance_gui):
        self.distance_gui = distance_gui
        Qt.QMetaObject.invokeMethod(self._distance_gui_label, "setText", Qt.Q_ARG("QString", str(self._distance_gui_formatter(self.distance_gui))))

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.blocks_moving_average_xx_0.set_length_and_scale((int(self.samp_rate/100000/self.decimation)), (1/(self.samp_rate/100000/self.decimation)))
        self.blocks_multiply_const_vxx_0_0_0.set_k((self.samp_rate/(2*self.pi)/self.decimation))
        self.filter_fft_low_pass_filter_0.set_taps(firdes.low_pass(1, (self.samp_rate/self.decimation), 2.4e6, 1e6, window.WIN_HAMMING, 6.76))

    def get_beatfrequency_gui(self):
        return self.beatfrequency_gui

    def set_beatfrequency_gui(self, beatfrequency_gui):
        self.beatfrequency_gui = beatfrequency_gui
        Qt.QMetaObject.invokeMethod(self._beatfrequency_gui_label, "setText", Qt.Q_ARG("QString", str(self._beatfrequency_gui_formatter(self.beatfrequency_gui))))

    def get_anntena_gain(self):
        return self.anntena_gain

    def set_anntena_gain(self, anntena_gain):
        self.anntena_gain = anntena_gain
        self.blocks_multiply_const_vxx_2.set_k(math.sqrt(self.anntena_gain))




def main(top_block_cls=FMCW_Radar, options=None):

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
