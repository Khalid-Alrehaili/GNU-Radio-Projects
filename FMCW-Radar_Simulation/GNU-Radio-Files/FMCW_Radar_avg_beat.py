# this module will be imported in the into your flowgraph
import numpy as np
from scipy.constants import speed_of_light

#UpBeat Detector
upbeat_values = np.array([1 , 2])
upbeat = 0
previous_lvl = 0
def reject_outliers(data, m=2):
	return data[abs(data - np.mean(data)) < m * np.std(data)]

def upbeat_detect(stage, probe_lvl):
	global upbeat, upbeat_values, previous_lvl
	if stage == 1:
		upbeat_values = np.append(upbeat_values, [probe_lvl])
		previous_lvl = probe_lvl
	if stage == -1:
		upbeat_values = reject_outliers(upbeat_values)
		upbeat = np.mean(upbeat_values)
	return upbeat

# Downbeat Detector
downbeat_values = np.array([1 , 2])
downbeat = 0
previous_lvl = 0
def reject_outliers(data, m=2):
	return data[abs(data - np.mean(data)) < m * np.std(data)]

def downbeat_detect(stage, probe_lvl):
	global downbeat, downbeat_values, previous_lvl
	if stage == -1:
		downbeat_values = np.append(downbeat_values, [probe_lvl])
		previous_lvl = probe_lvl
	if stage == 1:
		downbeat_values = reject_outliers(downbeat_values)
		downbeat = np.mean(downbeat_values)
	return downbeat

# Velocity Calculator
def Velocity_calculator(fc, downbeat, upbeat):
	velocity = speed_of_light*(-1*downbeat-upbeat)/(4*fc)
	return np.round(velocity, 3)

# Distance Calculator
def distance_calculator(Bandwidth, PRF, downbeat, upbeat):
	distance = (speed_of_light/(4*2*Bandwidth*PRF))*(upbeat-downbeat)
	return np.round(distance, 3)




    
    
