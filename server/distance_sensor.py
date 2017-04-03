from hcsr04sensor import sensor
import time
import json
import asyncio
from threading import Thread
from datetime import datetime

TRIG_PIN = 17
ECHO_PIN = 27
DELAY = 0.03
SAFE_DISTANCE = 8
NUMBER_OF_SAMPLES = 5


def start(handleBroadcast, handleStop):
    while True:
        #  Create a distance reading with the hcsr04 sensor module
        value = sensor.Measurement(TRIG_PIN, ECHO_PIN)
        raw_measurement = value.raw_distance(sample_size=NUMBER_OF_SAMPLES, sample_wait=DELAY)

        # Calculate the distance in centimeters
        metric_distance = value.distance_metric(raw_measurement)
        if metric_distance < SAFE_DISTANCE:
            handleStop()

        message = {
            "type": "sensor_distance_data",
            "payload": [metric_distance, str(datetime.now())],
            "level": "NOTICE",
            "timestamp": time.time() * 1000,
        }
        print(message)
        handleBroadcast(json.dumps(message))


def init(handleBroadcast, handleStop):
    Thread(target=start, args=(handleBroadcast, handleStop,)).start()
