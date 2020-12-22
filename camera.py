from picamera import PiCamera
import RPi.GPIO as GPIO
from datetime import datetime
import numpy as np
from time import sleep
import time
import atexit

from sender import sender

class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)
        self.camera.vflip = False
        self.camera.hflip = False

    def take_picture(self, add_timestamp=False):
        self.camera.start_preview()
        sleep(2)
        _filename = 'picture.jpg'
        if add_timestamp:
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            _filename = 'picture-{}.jpg'.format(timestamp)

        self.camera.capture(_filename)
        return _filename
        

def send(filename):
    file_path = f'./{filename}'
    if sender.is_ready:
        f = open(file_path, 'rb').read()
        try:
            sender.send(f);
        except Exception as e:
            print('Warning: Failed to send picture! Error: {}'.format(e))
        else:
            print('Picrture sent!')


camera = Camera()
while(True):
    _filename = camera.take_picture()
    # Enhance me: make it async
    send(_filename)
    sleep(5)
