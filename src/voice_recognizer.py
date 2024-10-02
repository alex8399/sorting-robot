from gpiozero import Button
import time
import subprocess
import requests
from enum import Enum

from src.command_unit import CommandUnit
from config import BUTTON_START_VOICE_RECOGNITION_PIN, SERVER_URL


class VoiceCommand(Enum):
    PUSH_DISK = "go"
    STOP_CONVEYER = "stop"
    START_CONVEYER = "start"
    PUSH_DISKS_INFINITE = "run"
    STOP_PUSHER = "boom"


class VoiceRecognizer:
    VOICE_RECOGNITION_FILE_NAME = "out.wav"
    RECORDING_TIME = 2

    SERVER_OK_RESPONSE = 200

    SLEEPING_BETWEEN_CYCLES_TIME = 0.1

    def __init__(self, command_unit: CommandUnit):
        self.button = Button(BUTTON_START_VOICE_RECOGNITION_PIN)
        self.audio_file = self.VOICE_RECOGNITION_FILE_NAME
        self.time_to_record = self.RECORDING_TIME
        self.command_unit = command_unit

    def detect_press(self):
        return self.button.is_active

    def run(self):
        while True:
            if self.detect_press():
                self.record_sound()
                text = self.decode_sound().lower()

                if VoiceCommand.STOP_CONVEYER in text:
                    self.command_unit.set_conveyor_is_running(False)
                elif VoiceCommand.START_CONVEYER in text:
                    self.command_unit.set_conveyor_is_running(True)
                elif VoiceCommand.PUSH_DISK in text:
                    self.command_unit.set_pushing_one_disk(True)
                elif VoiceCommand.PUSH_DISKS_INFINITE in text:
                    self.command_unit.set_pushing_disks_infinitely(True)
                elif VoiceCommand.STOP_PUSHER in text:
                    self.command_unit.set_pushing_disks_infinitely(False)

            time.sleep(self.SLEEPING_BETWEEN_CYCLES_TIME)

    def record_sound(self):
        subprocess.run(["arecord", "--format=S16_LE", "--rate=16000",
                       f"--duration={self.time_to_record}", "--file-type=wav", self.audio_file])

    def decode_sound(self) -> str:
        url = SERVER_URL
        files = {'file': open(self.audio_file, 'rb')}
        data = {'model_name': 'base.en'}

        response = requests.post(url, files=files, data=data)

        if response.status_code == self.SERVER_OK_RESPONSE:
            result = response.text.strip()
            return result
        else:
            return ""
