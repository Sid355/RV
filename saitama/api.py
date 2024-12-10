import requests

import http.server
import socketserver

# Define a custom request handler
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Print the requested URL (path) to the terminal
        print(self.path)
        global httpd
        httpd.shutdown()
        # Call the parent class's method to handle the request as usual

# Set the port number for the server
PORT = 8000

# Create and run the server
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving on port {PORT}...")
    #httpd.serve_forever()

if 0:
    url = "https://api.upstox.com/v2/login/authorization/dialog"

    data={'client_id':'ddb1a379-62db-4ed3-b109-fb31df0596cc',
             'redirect_uri':'https://127.0.0.1:8000',
             'response_type':'code'}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=data)

    #'https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id=ddb1a379-62db-4ed3-b109-fb31df0596cc&redirect_uri=https%3A%2F%2F127.0.0.1%3A8000'


code='HDj8h6'                        ################################################################

if 1:
    url = 'https://api.upstox.com/v2/login/authorization/token'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'code': code,
        'client_id': 'ddb1a379-62db-4ed3-b109-fb31df0596cc',
        'client_secret': '6j126pzt1k',
        'redirect_uri': 'https://127.0.0.1:8000',
        'grant_type': 'authorization_code',
    }

    response = requests.post(url, headers=headers, data=data)

    print(response.status_code)
    print(response.json())

    