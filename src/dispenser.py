from time import sleep

from shield_manager import ShieldManager
from config import DISPENSER_MOTOR

class Dispenser:
    MOVING_FORWARD_TIME = 1.2
    MOVING_BACK_TIME = 1
    
    def __init__(self):
        self.shieldManager = ShieldManager.getInstance()
        self.motor = DISPENSER_MOTOR

    def stop(self):
        self.shieldManager.stopMotor(self.motor)
        
    def dispense(self):
        self.rotate_motor(True, self.MOVING_FORWARD_TIME)
        self.rotate_motor(False, self.MOVING_BACK_TIME)
    
    def rotate_motor(self, back: bool, sleep_time):
        self.shieldManager.runMotor(self.motor, back)
        sleep(sleep_time)
        self.shieldManager.stopMotor(self.motor)
        