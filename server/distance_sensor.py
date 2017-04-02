from hcsr04sensor import sensor
import time
import json
import asyncio
from threading import Thread

TRIG_PIN = 17
ECHO_PIN = 27
DELAY = 0
SAFE_DISTANCE = 8


def init(handleBroadcast, handleStop):
    Thread(target=timed_log, args=(handleBroadcast, handleStop,)).start()


def start(handleBroadcast, handleStop):
    while True:
        #  Create a distance reading with the hcsr04 sensor module
        value = sensor.Measurement(TRIG_PIN, ECHO_PIN)
        raw_measurement = value.raw_distance()

        # Calculate the distance in centimeters
        metric_distance = value.distance_metric(raw_measurement)
        if (metric_distance < SAFE_DISTANCE) {
            handleStop()
        }
        asyncio.async(handleBroadcast(json.dumps({
            "type": "sensor_distance_data",
            "payload": metric_distance,
            "level": "NOTICE",
            "timestamp": time.time() * 1000,
        })))
        # yield from time.sleep(DELAY)
