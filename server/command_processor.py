#!/usr/bin/env python3.5

import asyncio
import websockets
import aiofiles
import uuid
import os
import json
from constants import HTTP_STATIC_SERVER
import car_controller


def write_file(command):
    f = yield from aiofiles.open(command['filename'], mode='w')
    try:
        yield from f.write(command['payload'])
    except Exception as e:
        return {
            'type': 'error',
            'message': str(e),
        }
    finally:
        yield from f.close()
        return {
            'type': 'success',
        }

    # yield aiofiles.open(command['filename'], mode='w') as f:
    #     try:
    #         await f.write(command['payload'])
    #         return (yield {
    #             'type': 'success',
    #         })
    #     except Exception as e:
    #         return (yield {
    #             'type': 'error',
    #             'message': str(e),
    #         })


def read_file(command):
    types = {
        'mp3': 'audio',
        'wav': 'audio',
        'mp4': 'video',
        'jpeg': 'image',
        'jpg': 'image',
        'png': 'image',
        'txt': 'text',
    }
    uri = HTTP_STATIC_SERVER + command['payload']
    try:
        type = types[command['payload'].split(".")[-1]]
    except Exception as e:
        response = {
            'type': 'error',
            'message': str(e),
        }
    else:
        response = {
            'type': type,
            'uri': uri,
        }

    return response
    # async with aiofiles.open(command['payload'], mode='rb') as f:
    #     return await f.read()


def update_file(command):
    ext = command['payload']['ext']
    filepath = command['filepath']
    new_filename = filepath + ext
    os.rename(filepath, new_filename)
    return new_filename


def ping(command):
    return 'pong'


def listdir(command):
    files = os.listdir("./uploads")
    response = {
        'files': files,
        'command_type': 'RECEIVE_DIRECTORY',
    }
    return response


def process_sensor_data(command):
    f = yield from aiofiles.open(command['device_id'] + '-sensor-data.json', mode='w')
    try:
        yield from f.write(command['payload'])
    except Exception as e:
        return {
            'type': 'error',
            'message': str(e),
        }
    finally:
        yield from f.close()
        return {
            'type': 'success',
        }


def process_car_controller(command):
    if command['payload'] == 'drive':
        car_controller.driveForward()
    elif command['payload'] == 'stop':
        car_controller.stop()


def process_command(command):
    # if is_json(command):
    # print("< {}".format(command))
    # command_received = json.loads(command)

    options = {
        'write': write_file,
        'read': read_file,
        'update': update_file,
        'ping': ping,
        'listdir': listdir,
        'sensor_data': process_sensor_data,
        'car_controller': process_car_controller,
    }

    return options[command['type']](command)
    # else:
    #     # File upload
    #     filepath = "uploads/" + str(uuid.uuid4())
    #     async with aiofiles.open(filepath, mode='wb') as f:
    #         print("[INFO] Writing to " + filepath)
    #         response = {
    #             'command_type': 'FILE_UPLOAD_COMPLETE',
    #             'filepath': filepath,
    #         }
    #         return await f.write(command) and response


@asyncio.coroutine
def process(queue):
    print("processing command")
    if queue.qsize() == 0:
        return (yield None)
    command = queue.get()
    print(command)
    message = command[2]
    websocket = command[3]
    print(message)
    response = process_command(message)
    print('response')
    print(response)
    responseType = 'success'
    if response['type'] == 'error':
        responseType = 'error'
        response = response['message']
    print(json.dumps({
        'type': responseType,
        'payload': response if response is not None else '',
    }))

    yield from websocket.send(json.dumps({
        'type': responseType,
        'payload': response if response is not None else '',
    }))
