import time
import logging
from threading import Thread
import RPi.GPIO as GPIO

from conveyor import Conveyor
from color_sensor import ColorSensor, Color
from motion_sensor import MotionSensor
from pusher import Pusher
from voice_recognizer import VoiceRecognizer
from AMSpi import AMSpi
from dispenser import Dispenser
from src.command_unit import CommandUnit


class Robot:
    CONVEYER_SLEEPING_TIME = 0.1
    CYCLE_SLEEPING_TIME = 0.2

    DISPENSER_SLEEPING_TIME = 0.1
    PAUSE_BETWEEN_DISPENSING_TIME = 6

    def __init__(self):
        self.command_unit = CommandUnit()
        self.voice_recognizer = VoiceRecognizer(self.command_unit)

        self.conveyor = Conveyor()
        self.pusher = Pusher()
        self.color_sensor = ColorSensor()
        self.motion_sensor = MotionSensor()
        self.dispenser = Dispenser()

        self.disp_thread = Thread(target=self.despense_disks_infinitely)
        self.sound_thread = Thread(target=self.voice_recognizer.run)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.conveyor.stop()
            self.pusher.stop()
            self.dispenser.stop()
            self.disp_thread.join()
            self.dispenser.stop()
            GPIO.cleanup()
        except RuntimeWarning:
            return True

    def despense_disks_infinitely(self):
        while self.command_unit.get_dispenser_is_running():
            if self.command_unit.get_pushing_one_disk() or self.command_unit.get_pushing_disks_infinitely():
                self.dispenser.dispense()

                if self.command_unit.get_pushing_disks_infinitely():
                    time.sleep(self.PAUSE_BETWEEN_DISPENSING_TIME)

                self.command_unit.set_pushing_one_disk(False)

            time.sleep(self.DISPENSER_SLEEPING_TIME)

    def run_in_waiting_state(self):
        if self.command_unit.get_conveyor_is_running():
            raise Exception(
                "Conveyor of robot is set for running that is restricted in the current state.")

        if self.conveyor.is_running():
            self.conveyor.stop()

        time.sleep(self.CONVEYER_SLEEPING_TIME)

    def run_in_dispensing_state(self):
        if not self.command_unit.get_conveyor_is_running():
            raise Exception(
                "Conveyor of robot is not set for running that is restricted in the current state.")

        if not self.conveyor.is_running():
            self.conveyor.run()

        time.sleep(self.CONVEYER_SLEEPING_TIME)

        if self.motion_sensor.detectObject():
            color = self.color_sensor.detectColor()

            if color == Color.BLACK:
                self.pusher.push_right()
            elif color == Color.WHITE:
                self.pusher.push_left()

        time.sleep(self.CYCLE_SLEEPING_TIME)

    def run(self):
        self.conveyor.run()
        self.sound_thread.start()
        self.disp_thread.start()

        try:
            while True:
                if self.command_unit.get_conveyor_is_running():
                    self.run_in_dispensing_state()
                else:
                    self.run_in_waiting_state()
        finally:
            self.conveyor.stop()
