import Adafruit_PCA9685


class ServoDrive:
    def __init__(self, num = 5):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)
        self.pos_init = 300
        self.pos_max = 500
        self.pos_min = 100
        self.number = num

    def turn(self, pos = 300, b = 0):
        self.pwm.set_pwm(self.number, b, pos)
    
    def turn_max(self, b = 0):
        self.pwm.set_pwm(self.number, b, self.pos_max)

    def turn_min(self, b = 0):
        self.pwm.set_pwm(self.number, b, self.pos_min)