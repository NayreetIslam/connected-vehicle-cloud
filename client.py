#!/usr/bin/env python3.5

import asyncio
import websockets
import json

# async def handler(websocket, path):
#   while True:
#     message = await producer()
#     print('message:\n'.format(message))
#     await websocket.send(message)

async def writeFile(filename, content):
  return json.dumps({
    'type': 'write',
    'filename': filename,
    'payload': content,
  })

async def readFile(filename):
  return json.dumps({
    'type': 'read',
    'payload': filename,
  })

async def client():
  async with websockets.connect('ws://localhost:8765') as websocket:

    # Write a file
    filename = input('Writing to a file...\nEnter a filename:')
    content = input('Enter the content of the file:')
    print('\nSending a request to save the data to a file...\n')
    data = await writeFile(filename, content)
    await websocket.send(data)
    response = await websocket.recv()
    print("Response:\n{}".format(response))

    # Read a file
    print('Sending a request to read the file...')
    data = await readFile(filename)
    await websocket.send(data)
    response = await websocket.recv()
    print("Response:\n{}".format(response))

asyncio.get_event_loop().run_until_complete(client())
# asyncio.get_event_loop().run_forever()