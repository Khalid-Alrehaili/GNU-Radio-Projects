import math
from scipy.constants import speed_of_light
c = speed_of_light

class object():
    def __init__(self, position : list, radial_velocity : float, area : float):
        self.position = position
        self.area = area
        self.radial_velocity = radial_velocity

    def get_position(self):
        return self.position

    def get_speed(self):
        return self.speed

    def get_area(self):
        return self.area

    def distance(self):
        return math.sqrt(math.pow(self.position[0], 2)+ math.pow(self.position[1], 2)+ math.pow(self.position[2], 2))

    def FSPL(self, frequency):
        FSPLv = 4*math.pi*frequency*self.distance()/c
        return FSPLv

    def get_radial_velocity(self):
        return self.radial_velocity

    def frequency_shift(self, frequency):
        answer = 2*self.radial_velocity*frequency/speed_of_light
        return answer
    