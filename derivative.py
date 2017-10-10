import threading
from gpiozero import DigitalInputDevice, Robot
from time import sleep

class Encoder(object):
    def __init__(self, pin):
        self._value = 0

        # setup gpiozero to call increment on each when_activated
        encoder = DigitalInputDevice(pin)
        encoder.when_activated = self._increment
        encoder.when_deactivated = self._increment
        
    def reset(self):
        self._value = 0

    def _increment(self):
        self._value += 1

    @property
    def value(self):
        return self._value

def clamp(value):
    return max(min(1, value), 0)

SAMPLETIME = 0.5
TARGET = 20
KP = 0.025
KD = 0.0125

r = Robot((10,9), (8,7)) 
e1 = Encoder(17)
e2 = Encoder(18)

m1_speed = 1
m2_speed = 1
r.value = (m1_speed, m2_speed)

e1_prev_error = 0
e2_prev_error = 0

while True:

    e1_error = TARGET - e1.value
    e2_error = TARGET - e2.value

    #print("error1 {} error2 {} adj1 {} adj2 {}".format(e1_error, e2_error, e1_adj, e2_adj))

    m1_speed += (e1_error * KP) + (e1_prev_error * KD)
    m2_speed += (e2_error * KP)  + (e1_prev_error * KD)

    m1_speed = clamp(m1_speed)
    m2_speed = clamp(m2_speed)

    # update the robots speed
    r.value = (m1_speed, m2_speed)

    print("e1 {} e2 {} m1 {} m2 {}".format(e1.value, e2.value, m1_speed, m2_speed))

    e1_prev_error = e1_error
    e2_prev_error = e2_error

    e1.reset()
    e2.reset()

    sleep(SAMPLETIME)