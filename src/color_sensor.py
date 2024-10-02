from enum import Enum
from config import (SIGNAL_SENSOR_PIN,
                    COLOR_SENSOR_PIN_1,
                    COLOR_SENSOR_PIN_2,
                    COLOR_SENSOR_PIN_3,
                    COLOR_SENSOR_PIN_4)
import RPi.GPIO as GPIO
import time
from dataclasses import dataclass


class Color(Enum):
    OTHER = 1
    BLACK = 2
    WHITE = 3


class ColorSensor:

    @dataclass
    class Threshold:
        red = 1
        green = 1
        blue = 1

    NUM_CYCLES = 10
    SCANNING_CYCLES = 4
    TIME_TO_DETECT = 0.1
    
    LOWER_BOUND_RED = 1350
    LOWER_BOUND_GREEN = 1050
    LOWER_BOUND_BLUE = 1250
    
    UPPER_BOUND_RED = 2000
    UPPER_BOUND_GREEN = 2000
    UPPER_BOUND_BLUE = 2000

    def __init__(self):
        ColorSensor.setup()

        self.lower_bound = self.Threshold()
        self.lower_bound.red = self.LOWER_BOUND_RED
        self.lower_bound.green = self.LOWER_BOUND_GREEN
        self.lower_bound.blue = self.LOWER_BOUND_BLUE

        self.upper_bound = self.Threshold()
        self.upper_bound.red = self.UPPER_BOUND_RED
        self.upper_bound.green = self.UPPER_BOUND_GREEN
        self.upper_bound.blue = self.UPPER_BOUND_BLUE

    def detectColor(self) -> Color:
        red_freq, green_freq, blue_freq = 0, 0, 0

        for _ in range(self.SCANNING_CYCLES):
            red_freq_new, green_freq_new, blue_freq_new = self.read_color()
            red_freq += red_freq_new
            green_freq += green_freq_new
            blue_freq += blue_freq_new
        red_freq /= self.SCANNING_CYCLES
        green_freq /= self.SCANNING_CYCLES
        blue_freq /= self.SCANNING_CYCLES

        red, green, blue = self.convert_all_to_rgb(
            red_freq, green_freq, blue_freq)

        if int(red > 210) + int(green > 210) + int(blue > 210) >= 1:
            if red > 200 and green < 200 and blue < 200:
                color = Color.OTHER
            color = Color.WHITE
        elif int(red <= 65) + int(green <= 65) + int(blue <= 65) >= 3:
            color = Color.BLACK
        else:
            color = Color.OTHER

        return color

    @staticmethod
    def setup():
        GPIO.setup(SIGNAL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup([COLOR_SENSOR_PIN_1, COLOR_SENSOR_PIN_2,
                   COLOR_SENSOR_PIN_3, COLOR_SENSOR_PIN_4], GPIO.OUT)
        GPIO.output(COLOR_SENSOR_PIN_1, GPIO.HIGH)
        GPIO.output(COLOR_SENSOR_PIN_2, GPIO.LOW)

    def read_color(self):
        GPIO.output(COLOR_SENSOR_PIN_3, GPIO.LOW)
        GPIO.output(COLOR_SENSOR_PIN_4, GPIO.LOW)
        time.sleep(self.TIME_TO_DETECT)
        red = self.read_frequency()

        GPIO.output(COLOR_SENSOR_PIN_3, GPIO.HIGH)
        GPIO.output(COLOR_SENSOR_PIN_4, GPIO.HIGH)
        time.sleep(self.TIME_TO_DETECT)
        green = self.read_frequency()

        GPIO.output(COLOR_SENSOR_PIN_3, GPIO.LOW)
        GPIO.output(COLOR_SENSOR_PIN_4, GPIO.HIGH)
        time.sleep(self.TIME_TO_DETECT)
        blue = self.read_frequency()

        return red, green, blue

    def read_frequency(self):
        start = time.time()
        for impulse_count in range(self.NUM_CYCLES):
            GPIO.wait_for_edge(SIGNAL_SENSOR_PIN, GPIO.FALLING)
        duration = time.time() - start
        return self.NUM_CYCLES / duration

    @staticmethod
    def convert_frequency_to_rgb(freq, lower_bound, upper_bound):
        if freq < lower_bound:
            return 0
        elif freq > upper_bound:
            return 255
        else:
            return int(255 * (freq - lower_bound) / (upper_bound - lower_bound))

    def convert_all_to_rgb(self, red_freq, green_freq, blue_freq):
        return (self.convert_frequency_to_rgb(red_freq, self.lower_bound.red, self.upper_bound.red),
                self.convert_frequency_to_rgb(
                    green_freq, self.lower_bound.green, self.upper_bound.green),
                self.convert_frequency_to_rgb(blue_freq, self.lower_bound.blue, self.upper_bound.blue))