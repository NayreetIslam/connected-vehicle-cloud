import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

fwdPin = 13
bwdPin = 12
leftPin = 16
rightPin = 26

GPIO.setup(fwdPin, GPIO.OUT)
GPIO.setup(bwdPin, GPIO.OUT)
GPIO.setup(leftPin, GPIO.OUT)
GPIO.setup(rightPin, GPIO.OUT)

driving = False


def driveForward():
    GPIO.output(fwdPin, GPIO.HIGH)
    global driving
    driving = True


def driveBackward():
    GPIO.output(fwdPin, GPIO.HIGH)


def turnWheels(direction):
    if direction == 'left':
        GPIO.output(rightPin, GPIO.LOW)
        GPIO.output(leftPin, GPIO.HIGH)
    elif direction == 'right':
        GPIO.output(leftPin, GPIO.LOW)
        GPIO.output(rightPin, GPIO.HIGH)


def stop():
    GPIO.output(leftPin, GPIO.LOW)
    GPIO.output(rightPin, GPIO.LOW)
    GPIO.output(fwdPin, GPIO.LOW)

    if driving:
        global driving
        driving = False
        GPIO.output(bwdPin, GPIO.HIGH)
        time.sleep(0.10)
        GPIO.output(bwdPin, GPIO.LOW)
    else:
        GPIO.output(bwdPin, GPIO.LOW)


def cleanupResources():
    GPIO.cleanup()
