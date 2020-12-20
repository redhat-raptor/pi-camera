from picamera import PiCamera
import RPi.GPIO as GPIO
from datetime import datetime
import numpy as np
from time import sleep
import time
import atexit


class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)
        self.camera.vflip = False
        self.camera.hflip = False

    def take_picture(self):
        self.camera.start_preview()
        sleep(2)
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        _filename = 'pic-{}.jpg'.format(timestamp)
        self.camera.capture(_filename)


class MyServo:
    def __init__(self, pin):
        self.servo_pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.servo_pin , 50) # 50 Hz (20 ms PWM period)
        self.pwm.start(7)

        atexit.register(self.cleanup)

        # mapping duty cycle to angle
        self.pwm_range = np.linspace(2.0, 12.0)
        self.pwm_span = self.pwm_range[-1] - self.pwm_range[0]
        self.ang_range = np.linspace(0.0, 180.0)
        self.ang_span = self.ang_range[-1] - self.ang_range[0]
    
    def angle_to_duty(self, ang):
        return round((((ang - self.ang_range[0]) / self.ang_span) * self.pwm_span) + self.pwm_range[0], 1)

    
    def cleanup(self):
        print('cleanup called...')
        self.pwm.ChangeDutyCycle(0) # this prevents jitter
        self.pwm.stop() # stops the pwm
        GPIO.cleanup()

    def rotate_to(self, degree):
        _duty_cycle = self.angle_to_duty(degree)
        print(f'{degree} -> {_duty_cycle}')
        self.pwm.ChangeDutyCycle(_duty_cycle)
        time.sleep(0.1)
        

servo = MyServo(27)
camera = Camera()
angle_step = 3
while(True):
    for angle in range(30, 150, angle_step):
        servo.rotate_to(angle)
        if angle % 30 == 0:
            camera.take_picture()

    for angle in range(150, 30, -angle_step):
        servo.rotate_to(angle)
        if angle % 30 == 0:
            camera.take_picture()
