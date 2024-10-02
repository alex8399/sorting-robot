# Embedded system Sorting robot

The robot sorts black and white disks and discards objects of other colors. The robot is intended to simulate an airport conveyor belt: dispatching international (black disks) and domestic (white disks) baggage and discarding foreign objects (objects of other colors) from the conveyor belt. The project is described in detail on the [poster for presentation](/presentation/poster.pdf).

## Content
[Elements of the Robot](#elements-of-the-robot)

[Images](#images)

[Team](#team)

[Requirements](#requirements)

[How to run](#how-to-run)

## Elements of the Robot
- **Disc dispenser:** Disc dispensers dispense black, white, and other colored disks onto the conveyor belt.

- **Conveyer:** The conveyer transported discs.

- **Motion sensor:** The motion sensor detects the presence of a disk on the conveyor belt.

- **Color sensor:** The color sensor emits visible light and, based on the reflection, detects if an object is white, black, or another color.

- **Disc rotating sorter:** The sorter rotates to dispense each disk into the correct box.

## Images
![Image1](/presentation/image01.jpg)

## Team
* [Aleksandr Vardanian](https://github.com/alex8399)
* [Aleksandr Nikolaev](https://github.com/Allex-Nik)
* [Ivan Bondyrev](https://github.com/iyubondyrev)
* [Arhan Chhabra](https://github.com/accc2023)
* [Dylan Galiart](https://github.com/dylangaliart)
* [João Cesse Valença Calado de Freitas](https://github.com/Joao-Freitas2004)
* [Jazman bin Mohamad Ismail](https://github.com/DareRagon)

## Requirements
 * Raspberry Pi 3B (with installed Python 3.10+)
 * Arduino L293D Motor Shield with shift register
 * Breadboard 400 points
 * TCS3200D-TCS230 Color Recognition Sensor
 * Infrared Break Beam Sensor (motion sensor)
 * DrPhone MPM - Mini Microphone With Holder - USB
 * 4xAA Battery Holder with Loose Wires
 * Fischertechnik construction set (with 4x motors)
 * Tactile Pushbutton Switch Momentary
 * DuPont Jumper wires (Female-Female, Male-Male, Female-Male)

## How to run
The folowing actions must be done on Raspberry Pi 3B with installed Python 3.10+.

### Installation 
1. **Clone the repository**:
    ```bash
    git clone https://github.com/alex8399/sorting-robot.git
    cd sorting-robot
    ```

2. **Create and activate a virtual environment** (optional but recommended):


    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. **Web-server for voice recognition**: Ensure your `src/config.py` file contains the URL to the server processing voice recognition:
    ```python
    # src/config.py
    SERVER_URL = 'URL_TO_YOUR_SERVER_FOR_VOICE_RECOGNITION'
    ```

### Running the robot

1. **Start robot**:
    ```bash
    python src/main.py  
    ```
