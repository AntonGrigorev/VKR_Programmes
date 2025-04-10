from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import ssl
import socket

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello from GET request!")
        print(f"GET request to {self.path}")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        
        response = {
            "status": "success",
            "received_data": post_data.decode("utf-8")
        }
        self.wfile.write(json.dumps(response).encode("utf-8"))
        
        print(f"POST request to {self.path}, data: {post_data.decode('utf-8')}")

if __name__ == "__main__":
    host = "0.0.0.0"  
    port = 8000        
    server = HTTPServer((host, port), SimpleHTTPRequestHandler)
    #server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cont = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    cont.load_cert_chain('/app/certs/cert3.pem', '/app/keys/key3.pem')
    server.socket = cont.wrap_socket(
    server.socket,
    server_side=True
)
    print(f"Server running on https://{host}:{port}")
    server.serve_forever()
