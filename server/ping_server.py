import http.server
import threading


def http_get(r):
    r.send_response(200)
    r.end_headers()
    r.wfile.write(bytes('ok', 'UTF-8'))


def run(port):
    h = http.server.BaseHTTPRequestHandler
    h.do_GET = http_get
    s = http.server.HTTPServer(('0.0.0.0', port), h)
    print("Ping server listening on port " + str(port))
    s.serve_forever()


def init(port=8767):
    thread = threading.Thread(target=run, args=(port,))
    thread.daemon = True

    try:
        thread.start()
    except KeyboardInterrupt:
        server.shutdown()
        sys.exit(0)
