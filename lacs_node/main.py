import json
import syslog
from http.server import BaseHTTPRequestHandler, HTTPServer

from .subsystems.config import get_config_object
from .subsystems.firewall import UFWManager

def main():
    syslog.syslog(syslog.LOG_INFO, "Initializing...")
    conf = get_config_object()
    ufw_man = UFWManager()

    class handler(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path == "/processrequest":
                syslog.syslog(syslog.LOG_INFO, "Recieved process request.")
                content_length = int(self.headers['Content-Length'])
                message = json.loads(self.rfile.read(content_length))
                if message["key"] == conf["key"]:
                    ip = message["ip"]
                    allow_time = int(message["time"])
                    try:
                        ufw_man.add_ip_to_ufw(ip, allow_time)
                        syslog.syslog(syslog.LOG_INFO, "Process request successful.")
                        self.send_response(200)
                        self.send_header('Content-type','application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
                    except Exception as e:
                        syslog.syslog(syslog.LOG_ERR, f"Process request failed with: {e}")
                        self.send_response(500)
                        self.send_header('Content-type','application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": False, "e": e}).encode("utf-8"))
                else:
                    syslog.syslog(syslog.LOG_ERR, f"Recieved process failed: invalid key from {self.address_string()}.")
                    self.send_response(403)
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False}).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()

    with HTTPServer((conf["bind_addr"], conf["port"]), handler) as server:
        server.serve_forever()
