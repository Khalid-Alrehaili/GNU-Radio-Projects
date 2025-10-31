# this module will be imported in the into your flowgraph

def frequency_detector(signal, vector_length):
	global a, b
	a = 0
	b = 0
	if type(signal) is list:
		a = max(signal)
		b = signal.index(a)-vector_length/2
	return b

