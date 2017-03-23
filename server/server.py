#!/usr/bin/env python3.5

import asyncio
import websockets
import json
import static_server
import ping_server
import queue
import command_processor
import time
from multiprocessing import Process
import threading
import constants

prio_queue = queue.PriorityQueue()


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except TypeError:
        return False
    return True


def convert_to_json(message):
    print(message)
    if is_json(message):
        return json.loads(message)
    else:
        return None


def determine_prio(jsonMessage):
    priorities = {
        'INFO': 6,
        'NOTICE': 5,
        'WARNING': 4,
        'ALERT': 3,
        'CRITICAL': 2,
        'EMERGENCY': 1,
    }
    priority = priorities[jsonMessage['level']]
    if priority is not None:
        return priority
    return 1


@asyncio.coroutine
def handler(websocket, path):
    while True:
        try:
            message = yield from websocket.recv()
            jsonMessages = convert_to_json(message)
            if isinstance(jsonMessages, dict):
                jsonMessages = [jsonMessages]
            for command in jsonMessages:
                timestamp = int(command['timestamp'])
                print((determine_prio(command), timestamp))
                prio_queue.put(
                    (timestamp, determine_prio(command), command, websocket),
                )
        except websockets.exceptions.ConnectionClosed:
            # print("Client disconnected")
            time.sleep(1)
            pass


def processQueue(prio_queue):
    print('processQueue starting')
    while True:
        try:
            print('processQueue')
            yield from command_processor.process(prio_queue)
            time.sleep(0.5)
        except Exception as e:
            print(e)
            time.sleep(1)
            pass


def startProcessingQueue(prio_queue):
    queueProcessor = processQueue(prio_queue)
    for i in queueProcessor:
        pass


def startQueueProcessing(prio_queue):
    thread = threading.Thread(target=startProcessingQueue, args=(prio_queue,))
    thread.daemon = True

    try:
        print('startQueueProcessing starting')
        thread.start()
    except KeyboardInterrupt:
        server.shutdown()
        sys.exit(0)


# processQueue(prio_queue)

start_server = websockets.serve(handler, '0.0.0.0', constants.SERVER_PORT, max_size=None)
print("Server listening on port " + str(constants.SERVER_PORT))

static_server.init(constants.HTTP_STATIC_PORT)
ping_server.init(constants.PING_PORT)
# Process(target=processQueue, args=(prio_queue,)).start()
startQueueProcessing(prio_queue)
# processQueue(prio_queue)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

# [{"type": "read", "payload": "hello.txt", "level": "INFO", "timestamp": "1489686823710"}, {"type": "read", "payload": "hello.txt", "level": "INFO", "timestamp": "1489686823730"}, {"type": "write", "payload": "good-bye", "filename": "hello.txt", "level": "NOTICE", "timestamp": "1489686823730"}]
