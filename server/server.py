#!/usr/bin/env python3.5

import asyncio
import websockets
import json
import aiofiles
import uuid
import os
import static_server
import ping_server
import time

# Port initialization
SERVER_PORT = int(os.getenv("SERVER_PORT", 8765))
PING_PORT = int(os.getenv("PING_PORT", SERVER_PORT + 1))
HTTP_STATIC_PORT = int(os.getenv("STATIC_PORT", PING_PORT + 1))
HTTP_STATIC_SERVER = "http://" + os.getenv("IP_ADDRESS", "localhost") + \
    ":" + str(HTTP_STATIC_PORT) + "/"

async def write_file(command):
    async with aiofiles.open(command['filename'], mode='w') as f:
        await f.write(command['payload'])

async def read_file(command):
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

async def update_file(command):
    ext = command['payload']['ext']
    filepath = command['filepath']
    new_filename = filepath + ext
    os.rename(filepath, new_filename)
    return new_filename

async def ping(command):
    return 'pong'

async def listdir(command):
    files = os.listdir("./uploads")
    response = {
        'files': files,
        'command_type': 'RECEIVE_DIRECTORY',
    }
    return response


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except TypeError:
        return False
    return True

async def handler(websocket, path):
    while True:
        try:
            message = await websocket.recv()
            response = await process_command(message)
            responseType = 'success'
            if response['type'] == 'error':
                responseType = 'error'
                response = response['message']

            await websocket.send(json.dumps({
                'type': responseType,
                'payload': response if response is not None else '',
            }))
        except websockets.exceptions.ConnectionClosed:
            # print("Client disconnected")
            time.sleep(1)
            pass

async def process_command(command):
    if is_json(command):
        print("< {}".format(command))
        command_received = json.loads(command)

        options = {
            'write': write_file,
            'read': read_file,
            'update': update_file,
            'ping': ping,
            'listdir': listdir,
        }

        return await options[command_received['type']](command_received)
    else:
        # File upload
        filepath = "uploads/" + str(uuid.uuid4())
        async with aiofiles.open(filepath, mode='wb') as f:
            print("[INFO] Writing to " + filepath)
            response = {
                'command_type': 'FILE_UPLOAD_COMPLETE',
                'filepath': filepath,
            }
            return await f.write(command) and response


start_server = websockets.serve(handler, '0.0.0.0', SERVER_PORT, max_size=None)
print("Server listening on port " + str(SERVER_PORT))

static_server.init(HTTP_STATIC_PORT)
ping_server.init(PING_PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
