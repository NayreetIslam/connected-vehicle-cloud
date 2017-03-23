import acceleration
import time


def init(websocket):
    for measurement in acceleration.startSensing():
        websocket.send(json.dump({
            "type": "sensor_data",
            "payload": measurement,
            "sensor_type": "acceleration",
            "level": "INFO",
            "timestamp": time.time(),
        }))
