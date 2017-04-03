# SenseHAT Logger from
# https://github.com/raspberrypilearning/sense-hat-data-logger
import asyncio
import aiofiles
from datetime import datetime
import time
from sense_hat import SenseHat
from select import select
from threading import Thread
import json

# Logging Settings
TEMP_H = True
TEMP_P = False
HUMIDITY = False
PRESSURE = False
ORIENTATION = True
ACCELERATION = True
MAG = False
GYRO = True
DELAY = 0
BASENAME = "sensor"
WRITE_FREQUENCY = 1
LOG_AT_START = True

sense = None
sense_data = []
run = True
logging = LOG_AT_START
batch_data = []
websocketConnection = None
filename = None
broadcastMessage = None


def file_setup(filename):
    header = []
    if TEMP_H:
        header.append("temp_h")
    if TEMP_P:
        header.append("temp_p")
    if HUMIDITY:
        header.append("humidity")
    if PRESSURE:
        header.append("pressure")
    if ORIENTATION:
        header.extend(["pitch", "roll", "yaw"])
    if MAG:
        header.extend(["mag_x", "mag_y", "mag_z"])
    if ACCELERATION:
        header.extend(["accel_x", "accel_y", "accel_z"])
    if GYRO:
        header.extend(["gyro_x", "gyro_y", "gyro_z"])
    header.append("timestamp")

    with open(filename, "w") as f:
        f.write(",".join(str(value) for value in header) + "\n")


# Function to collect data from the sense hat and build a string
def get_sense_data():
    sense_data = []

    if TEMP_H:
        sense_data.append(sense.get_temperature_from_humidity())

    if TEMP_P:
        sense_data.append(sense.get_temperature_from_pressure())

    if HUMIDITY:
        sense_data.append(sense.get_humidity())

    if PRESSURE:
        sense_data.append(sense.get_pressure())

    if ORIENTATION:
        yaw, pitch, roll = sense.get_orientation().values()
        sense_data.extend([pitch, roll, yaw])

    if MAG:
        mag_x, mag_y, mag_z = sense.get_compass_raw().values()
        sense_data.extend([mag_x, mag_y, mag_z])

    if ACCELERATION:
        x, y, z = sense.get_accelerometer_raw().values()
        sense_data.extend([x, y, z])

    if GYRO:
        gyro_x, gyro_y, gyro_z = sense.get_gyroscope_raw().values()
        sense_data.extend([gyro_x, gyro_y, gyro_z])

    sense_data.append(datetime.now())
    return sense_data


def show_state(logging):
    if logging:
        sense.show_letter("Y", text_colour=[0, 100, 0])
    else:
        sense.show_letter("N", text_colour=[100, 0, 0])


def log_data():
    output_string = ",".join(str(value) for value in sense_data)
    batch_data.append(output_string)


def timed_log():
    while run:
        if logging is True:
            log_data()
        eventloop = asyncio.new_event_loop()
        asyncio.set_event_loop(eventloop)
        eventloop.run_until_complete(run())
        time.sleep(DELAY)


def run():
    global sense_data
    sense_data = get_sense_data()

    show_state(logging)

    if logging is True and DELAY == 0:
        log_data()

    if len(batch_data) >= WRITE_FREQUENCY:
        yield from broadcastMessage(json.dumps({
            "type": "sensor_data",
            "payload": batch_data,
            "level": "INFO",
            "timestamp": time.time() * 1000,
        }))
        f = yield from aiofiles.open(filename, mode='a')
        try:
            for line in batch_data:
                yield from f.write(line + "\n")
                global batch_data
                batch_data = []
        except Exception as e:
            print(e)
        finally:
            yield from f.close()


def init(handleBroadcast):

    # Main Program
    global sense
    sense = SenseHat()

    global broadcastMessage
    broadcastMessage = handleBroadcast

    show_state(logging)

    if BASENAME == "":
        global filename
        filename = "SenseLog-"+str(datetime.now())+".csv"
    else:
        global filename
        filename = BASENAME+"-"+str(datetime.now())+".csv"

    file_setup(filename)
    Thread(target=timed_log).start()

    sense.clear()

    return sense
