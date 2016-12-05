import http.server
import threading


def start_server(port=8766, bind="", cgi=False):
    if cgi is True:
        return http.server.test(HandlerClass=http.server.CGIHTTPRequestHandler,
                                port=port, bind=bind)
    else:
        return http.server.test(
            HandlerClass=http.server.SimpleHTTPRequestHandler,
            port=port, bind=bind)

# If you want cgi, set cgi to True e.g. start_server(cgi=True)
thread = threading.Thread(target=start_server)
thread.daemon = True

try:
    thread.start()
except KeyboardInterrupt:
    server.shutdown()
    sys.exit(0)

# start_server()
