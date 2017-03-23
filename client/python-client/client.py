#!/usr/bin/env python3.5

import asyncio
import websockets
import json
import sys
import getopt
import os
import sensors

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
    # options = {
    #     'write': write_file,
    #     'read': read_file,
    #     'update': update_file,
    #     'ping': ping,
    #     'listdir': listdir,
    # }
    # json_command = json.loads(command)
    # return await options[json_command['type']](json_command)
    yield from websocket.send(command)
    response = yield from websocket.recv()
    print("Response:\n{}".format(response))

async def client(argv):
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

    async with websockets.connect('ws://' + address + ':' +
                                  str(SERVER_PORT)) as websocket:
            sensors.init(websocket)
            while True:
                await get_command(websocket)
            # Write a file
            # filename = input('Writing to a file...\nEnter a filename:')
            # content = input('Enter the content of the file:')
            # print('\nSending a request to save the data to a file...\n')
            # data = await write_file(filename, content)
            # await websocket.send(data)
            # response = await websocket.recv()
            # print("Response:\n{}".format(response))
            #
            # # Read a file
            # print('Sending a request to read the file...')
            # data = await read_file(filename)
            # await websocket.send(data)
            # response = await websocket.recv()
            # print("Response:\n{}".format(response))

asyncio.get_event_loop().run_until_complete(client(sys.argv[1:]))
# asyncio.get_event_loop().run_forever()
