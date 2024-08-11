from http.server import HTTPServer
from server.handler import ScrumAppHTTPRequestHandler

def run(server_class=HTTPServer, handler_class=ScrumAppHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Starting server on port 8000...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
