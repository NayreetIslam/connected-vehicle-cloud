# SenseHAT Logger from
# https://github.com/raspberrypilearning/sense-hat-data-logger
from datetime import datetime
import time
from sense_hat import SenseHat
from evdev import InputDevice, categorize, ecodes, list_devices
from select import select
import picamera
from threading import Thread

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
BASENAME = "Fall"
WRITE_FREQUENCY = 1
ENABLE_CAMERA = False
LOG_AT_START = False


def init(websocket):
    camera = None
    dev = None
    run = True
    logging = LOG_AT_START
    batch_data = []

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

    # Function to capture input from the Sense Hat Joystick
    def get_joystick():
        devices = [InputDevice(fn) for fn in list_devices()]
        for dev in devices:
            if dev.name == "Raspberry Pi Sense HAT Joystick":
                return dev

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

    def check_input():
        running = True
        logging_event = False
        r, w, x = select([dev.fd], [], [], 0.01)
        for fd in r:
            for event in dev.read():
                if event.type == ecodes.EV_KEY and event.value == 1:
                    logging_event = True
                    if event.code == ecodes.KEY_UP:
                        if ENABLE_CAMERA and camera.recording:
                            camera.stop_recording()
                        running = False
                    if event.code == ecodes.KEY_LEFT:
                        if ENABLE_CAMERA:
                            camera.start_recording(
                                "SenseVid-"+str(datetime.now()) + ".h264"
                            )
                            logging_event = False

        return logging_event, running

    def log_data():
        output_string = ",".join(str(value) for value in sense_data)
        batch_data.append(output_string)

    def timed_log():
        while run:
            if logging is True:
                log_data()
            time.sleep(DELAY)

    # Main Program
    sense = SenseHat()
    show_state(logging)
    dev = get_joystick()

    if BASENAME == "":
        filename = "SenseLog-"+str(datetime.now())+".csv"
    else:
        filename = BASENAME+"-"+str(datetime.now())+".csv"

    file_setup(filename)

    if DELAY > 0:
        Thread(target=timed_log).start()

    if ENABLE_CAMERA:
        camera = picamera.PiCamera()

    while run is True:
        sense_data = get_sense_data()

        logging_event, run = check_input()

        if logging_event:
            logging = not(logging)
            show_state(logging)

        if logging is True and DELAY == 0:
            log_data()

        if len(batch_data) >= WRITE_FREQUENCY:
            with open(filename, "a") as f:
                websocket.send({
                    "type": "sensor_data",
                    "payload": batch_data,
                    "level": "INFO",
                    "timestamp": time.time() * 1000,
                })
                for line in batch_data:
                    f.write(line + "\n")
                batch_data = []

    with open(filename, "a") as f:
        for line in batch_data:
            f.write(line + "\n")
            batch_data = []

    sense.clear()
