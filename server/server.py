#!/usr/bin/env python3.5

import asyncio
import websockets
import json
import aiofiles

async def writeFile(command):
  async with aiofiles.open(command['filename'], mode='w') as f:
    await f.write(command['payload'])

async def readFile(command):
  async with aiofiles.open(command['payload'], mode='r') as f:
    return await f.read()

async def handler(websocket, path):
  while True:
    try:
      message = await websocket.recv()
      response = await processCommand(message)
      await websocket.send(json.dumps({
        'type': 'success',
        'payload': response if response is not None else '',
      }))
    except websockets.exceptions.ConnectionClosed:
      # print("Client disconnected")
      pass
    


async def processCommand(command):
  print("< {}".format(command))
  commandReceived = json.loads(command)

  options = {
    'write': writeFile,
    'read': readFile,
  }

  return await options[commandReceived['type']](commandReceived)

start_server = websockets.serve(handler, '0.0.0.0', 8765)
print("Server listening on port 8765")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
