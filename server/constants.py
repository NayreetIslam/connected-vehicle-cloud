import os

SERVER_PORT = int(os.getenv("SERVER_PORT", 8765))
PING_PORT = int(os.getenv("PING_PORT", SERVER_PORT + 1))
HTTP_STATIC_PORT = int(os.getenv("STATIC_PORT", PING_PORT + 1))
HTTP_STATIC_SERVER = "http://" + os.getenv("IP_ADDRESS", "localhost") + \
    ":" + str(HTTP_STATIC_PORT) + "/"
