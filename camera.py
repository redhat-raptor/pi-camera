from picamera import PiCamera
import RPi.GPIO as GPIO
from datetime import datetime
import numpy as np
from time import sleep
import time
import atexit
import os
import logging
from sender import sender

logging.basicConfig(level=logging.DEBUG)

GPIO.setmode(GPIO.BCM)
GPIO.setup(1, GPIO.IN)
GPIO.setup(2, GPIO.IN)
GPIO.setup(3, GPIO.IN)

class Camera:
    def __init__(self, width=1024, height=768):
        self.camera = PiCamera()
        self.camera.resolution = (width, height)
        self.camera.vflip = False
        self.camera.hflip = False

    def take_picture(self, add_timestamp=False):
        logging.debug('Taking picture {} timestamp'.format('with' if add_timestamp else 'without'))
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



while(True):
    if GPIO.input(1):
        camera = Camera(1920, 1080)
    elif GPIO.input(2):
        camera = Camera(1920, 1080)
    else:
        camera = Camera()

    _filename = camera.take_picture(True)
    # Enhance me: make it async
    send(_filename)
    sleep(5)
