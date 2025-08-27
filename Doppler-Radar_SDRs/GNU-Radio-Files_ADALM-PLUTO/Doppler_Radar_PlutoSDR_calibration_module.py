# this module will be imported in the into your flowgraph

global Mag
Mag = 0
def Mag1(button, Mag1):
	if button == 1:
		global Mag
		Mag = Mag1
	return Mag
global Arg
Arg = 0

def Arg1(button, Arg1):
	if button == 1:
		global Arg
		Arg = Arg1
	return Arg