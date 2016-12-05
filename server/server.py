#!/usr/bin/env python3.5

import asyncio
import websockets
import json
import aiofiles
import uuid
import os


async def write_file(command):
    async with aiofiles.open(command['filename'], mode='w') as f:
        await f.write(command['payload'])


async def read_file(command):
    async with aiofiles.open(command['payload'], mode='r') as f:
        return await f.read()


async def updateFile(command):
    ext = command['payload']['ext']
    filePath = command['filepath']
    newFilename = filePath + ext
    os.rename(filePath, newFilename)
    return newFilename


async def ping(command):
    return 'pong'

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
      response = await processCommand(message)
      await websocket.send(json.dumps({
        'type': 'success',
        'payload': response if response is not None else '',
      }))
    except websockets.exceptions.ConnectionClosed:
      # print("Client disconnected")
      pass

async def processCommand(command):
  if is_json(command):
      print("< {}".format(command))
      commandReceived = json.loads(command)

      options = {
        'write': writeFile,
        'read': readFile,
        'update': updateFile,
        'ping': ping,
      }

      return await options[commandReceived['type']](commandReceived)
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


start_server = websockets.serve(handler, '0.0.0.0', 8765)
print("Server listening on port 8765")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
