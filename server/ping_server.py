import http.server
import threading

def http_get(r):
    r.send_response(200)
    r.end_headers()
    r.wfile.write(bytes('ok', 'UTF-8'))

def run():
    h = http.server.BaseHTTPRequestHandler
    h.do_GET = http_get
    s = http.server.HTTPServer(('0.0.0.0', 8767), h)
    print("Ping server listening on port 8767")
    s.serve_forever()

thread = threading.Thread(target=run)
thread.daemon = True

try:
    thread.start()
except KeyboardInterrupt:
    server.shutdown()
    sys.exit(0)
