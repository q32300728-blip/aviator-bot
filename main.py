from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open("index.html", "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error loading index.html: {e}".encode())

if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHandler)
    print("Web server running on port 8080...")
    httpd.serve_forever()
