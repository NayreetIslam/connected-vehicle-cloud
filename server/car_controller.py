import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

fwdPin = 12
bwdPin = 13
leftPin = 16
rightPin = 26

GPIO.setup(fwdPin, GPIO.OUT)
GPIO.setup(bwdPin, GPIO.OUT)
GPIO.setup(leftPin, GPIO.OUT)
GPIO.setup(rightPin, GPIO.OUT)


def driveForward():
    GPIO.output(fwdPin, GPIO.HIGH)


def driveBackward():
    GPIO.output(fwdPin, GPIO.HIGH)


def turnWheels(direction):
    if direction is 'left':
        GPIO.output(rightPin, GPIO.LOW)
        GPIO.output(leftPin, GPIO.HIGH)
    elif direction is 'right':
        GPIO.output(leftPin, GPIO.LOW)
        GPIO.output(rightPin, GPIO.HIGH)


def stop():
    GPIO.output(fwdPin, GPIO.LOW)
    GPIO.output(bwdPin, GPIO.LOW)
    GPIO.output(leftPin, GPIO.LOW)
    GPIO.output(rightPin, GPIO.LOW)


def cleanupResources():
    GPIO.cleanup()


try:
    driveForward()
except KeyboardInterrupt:
    stop()
    cleanupResources()
    raise
