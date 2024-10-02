import RPi.GPIO as GPIO
from robot import Robot


def setup() -> None:
    """
    Setup environment for robot.
    """

    GPIO.setmode(GPIO.BCM)


if __name__ == "__main__":
    setup()

    with Robot() as robot:
        robot.run()
