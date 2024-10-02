import RPi.GPIO as GPIO

from config import MOTION_SENSOR_PIN

class MotionSensor:
    
    def __init__(self):
        self.pin : int = MOTION_SENSOR_PIN
        self.setup()
    
    def setup(self) -> None:
        """Setup pin for motion sensor.
        """
        
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def getPin(self) -> int:
        """Return pin which was set for output.

        Returns:
            int: number of pin.
        """
        return self.pin
        
    def detectObject(self) -> bool:
        """Get output of motion sensor.

        Returns:
            bool: True if motion sensor detects object. Otherwise, False.
        """
                
        output: int = not GPIO.input(self.pin)
        
        response: bool = False
        if output:
            response = True
        
        return response