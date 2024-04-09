import RPi_I2C_driver as RPi_I2C_driver
from time import *

mylcd = RPi_I2C_driver.lcd()


class car:

    def __init__(self, number, location, timestamp):
        self.number = number
        self.location = location
        self.timestamp = timestamp
    
    def display(self):
        mylcd.lcd_display_string(self.number, 1)
        mylcd.lcd_display_string(self.location, 2)
        mylcd.lcd_display_string(self.timestamp, 3)
    
        sleep(5)

        mylcd.lcd_clear()