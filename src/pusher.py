from time import sleep

from shield_manager import ShieldManager
from config import PUSHER_MOTOR


class Pusher:
    ROTATION_TIME_RIGHT_FORWARD_TIME = 0.65
    ROTATION_TIME_RIGHT_BACK_TIME = 1.2
    ROTATION_TIME_LEFT_FORWARD_TIME = 1.1
    ROTATION_TIME_LEFT_BACK_TIME = 1.5

    WAITING_TIME = 3

    def __init__(self):
        self.shieldManager = ShieldManager.getInstance()
        self.motor = PUSHER_MOTOR
        self.white_pos = False
        self.black_pos = False

    def stop(self):
        self.shieldManager.stopMotor(self.motor)

    def push_right(self):
        self.rotate_motor(True, self.ROTATION_TIME_RIGHT_FORWARD_TIME)
        sleep(self.WAITING_TIME)
        self.rotate_motor(False, self.ROTATION_TIME_RIGHT_BACK_TIME)

    def push_left(self):
        self.rotate_motor(True, self.ROTATION_TIME_LEFT_FORWARD_TIME)
        sleep(self.WAITING_TIME)
        self.rotate_motor(False, self.ROTATION_TIME_LEFT_BACK_TIME)

    def rotate_motor(self, left: bool, sleep_time):
        self.shieldManager.runMotor(self.motor, left)
        sleep(sleep_time)
        self.shieldManager.stopMotor(self.motor)
