import http.server
import socketserver

# Define a custom request handler
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Print the requested URL (path) to the terminal
        print(f"Requested URL: {self.path}")

        # Call the parent class's method to handle the request as usual

# Set the port number for the server
PORT = 8080

# Create and run the server
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving on port {PORT}...")
    httpd.serve_forever()
