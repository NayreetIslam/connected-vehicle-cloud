import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
fwdPin = 13
bwdPin = 12
GPIO.setup(fwdPin, GPIO.OUT)
GPIO.setup(bwdPin, GPIO.OUT)

driving = True


def stop():
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
