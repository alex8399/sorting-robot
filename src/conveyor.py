from shield_manager import ShieldManager
from config import CONVEYOR_MOTOR

class Conveyor:
    CONVEYOR_SPEED = 60
    
    def __init__(self):
        self.shieldManager: ShieldManager = ShieldManager.getInstance()
        self.motor = CONVEYOR_MOTOR
        self.speed = self.CONVEYOR_SPEED
        self.active = False
        
    def set_speed(self, value: int):
        if value < 0 or value > 100:
            raise Exception("Speed can not be less than 0 and more than 100.")
        
        self.speed = value
        
    def get_speed(self) -> int:
        return self.speed

    def run(self, forward: bool = True) -> bool:
        self.active = True
        return self.shieldManager.runMotor(self.motor, forward, self.speed)

    def stop(self) -> bool:
        self.active = False
        return self.shieldManager.stopMotor(self.motor)
    
    def is_running(self) -> bool:
        return self.active