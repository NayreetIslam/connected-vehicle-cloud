#!/usr/bin/env python3.5

import asyncio
import websockets
import json
import sys
import getopt
import os
import time

SERVER_PORT = int(os.getenv("SERVER_PORT", 8765))

# async def handler(websocket, path):
#   while True:
#     message = await producer()
#     print('message:\n'.format(message))
#     await websocket.send(message)

# async def write_file(filename, content):
#     return json.dumps({
#         'type': 'write',
#         'filename': filename,
#         'payload': content,
#     })
#
# async def read_file(filename):
#     return json.dumps({
#         'type': 'read',
#         'payload': filename,
#     })


def get_command(websocket):
    command = input('Command: ')
    yield from websocket.send(command)
    response = yield from websocket.recv()
    print("Response:\n{}".format(response))


def listen(websocket):
    response = yield from websocket.recv()
    print("Received << :\n{}".format(response))


def client(argv):
    address = '127.0.0.1'
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ip="])
    except getopt.GetoptError:
        print('client.py -i <serverAddress>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ip"):
            address = arg
    print('Server address is: ', address + '\n')
    websocketAddress = 'ws://' + address + ':' + str(SERVER_PORT)
    try:
        websocket = yield from websockets.connect(websocketAddress)
    except:
        time.sleep(1)
        eventloop = asyncio.new_event_loop()
        asyncio.set_event_loop(eventloop)
        eventloop.run_until_complete(client(argv))
        return
    while True:
        # yield from get_command(websocket)
        yield from listen(websocket)

asyncio.get_event_loop().run_until_complete(client(sys.argv[1:]))
asyncio.get_event_loop().run_forever()
