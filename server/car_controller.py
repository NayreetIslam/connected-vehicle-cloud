import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

fwdPin = 13
bwdPin = 12
leftPin = 26
rightPin = 16

GPIO.setup(fwdPin, GPIO.OUT)
GPIO.setup(bwdPin, GPIO.OUT)
GPIO.setup(leftPin, GPIO.OUT)
GPIO.setup(rightPin, GPIO.OUT)

driving = True


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

    if GPIO.input(fwdPin) == 1:
        global driving
        driving = False
        GPIO.output(fwdPin, GPIO.LOW)
        GPIO.output(bwdPin, GPIO.HIGH)
        time.sleep(0.10)
        GPIO.output(bwdPin, GPIO.LOW)
        print("sudden stop")
    else:
        GPIO.output(fwdPin, GPIO.LOW)
        GPIO.output(bwdPin, GPIO.LOW)


def cleanupResources():
    GPIO.cleanup()

driveForward()

