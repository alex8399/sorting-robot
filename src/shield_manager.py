import time
from AMSpi import AMSpi
from enum import Enum
from typing import Dict
from dataclasses import dataclass
from threading import Lock

from config import (
    LATCH_REGISTER_PIN, CLK_REGISTER_PIN, SER_REGISTER_PIN, MOTOR_1_PIN, MOTOR_2_PIN, MOTOR_3_PIN, MOTOR_4_PIN)


class ShieldManager:
    __instance = None
    __amspi: AMSpi
    
    AVAILABLE_MOTOR_NUMBERS = (1, 2, 3, 4)

    def __init__(self):
        if ShieldManager.__instance is not None:
            raise Exception(
                "This is a singleton class. Use getInstance() method.")

        self.__amspi = AMSpi()
        self.__amspi.set_74HC595_pins(
            LATCH_REGISTER_PIN, CLK_REGISTER_PIN, SER_REGISTER_PIN)
        self.__amspi.set_L293D_pins(
            MOTOR_1_PIN, MOTOR_2_PIN, MOTOR_3_PIN, MOTOR_4_PIN)
        ShieldManager.__instance = self
        self.mutex = Lock()

    @staticmethod
    def getInstance():
        if ShieldManager.__instance is None:
            ShieldManager()
        return ShieldManager.__instance

    def runMotor(self, motor: int, clockwise: bool = True, speed: int = 100) -> bool:
        """Run motor with given direction and speed.

        Args:
            motor (int): number of dc motor.
            clockwise (bool, optional): True for clockwise, False for counterclockwise. Defaults to True.
            speed (int, optional): pwm duty cycle (range 0-100). Defaults to 100.

        Returns:
            bool: False in case of an ERROR, True if everything is OK.
        """
        if speed < 0 or speed > 100:
            raise Exception("Speed can not be less than 0 and more than 100.")
        
        if not self.is_available_motor_number(motor):
            raise Exception("There is no motor with number {}.".format(motor))
                
        with self.mutex:
            result = False
            while not result:
                result = self.__amspi.run_dc_motor(motor, clockwise, speed)

    def stopMotor(self, motor: int) -> bool:
        """Stop running motor.

        Args:
            motor (int): number of dc motor.

        Returns:
            bool: False in case of an ERROR, True if everything is OK.
        """
        if not self.is_available_motor_number(motor):
            raise Exception("There is no motor with number {}.".format(motor))
        
        with self.mutex:
            result = False
            while not result:
                result = self.__amspi.stop_dc_motor(motor)
                
    def is_available_motor_number(self, motor: int):
        return motor in self.AVAILABLE_MOTOR_NUMBERS