import time
import json
import asyncio
from threading import Thread
import RPi.GPIO as GPIO
from datetime import datetime

GPIO.setmode(GPIO.BCM)

TRIG_PIN = 17
ECHO_PIN = 27
DELAY = 0.5
SAFE_DISTANCE = 8

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.output(TRIG_PIN, GPIO.LOW)


def start(handleBroadcast, handleStop):
    while True:
        GPIO.output(TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG, GPIO.LOW)

        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        if distance < SAFE_DISTANCE:
            handleStop()

        message = {
            "type": "sensor_distance_data",
            "payload": [distance, datetime.now()],
            "level": "NOTICE",
            "timestamp": time.time() * 1000,
        }
        print(message)
        handleBroadcast(json.dumps(message))
        time.sleep(DELAY)


def init(handleBroadcast, handleStop):
    Thread(target=start, args=(handleBroadcast, handleStop,)).start()
