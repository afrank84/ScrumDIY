from http.server import BaseHTTPRequestHandler
import json
import os
from server.routes import handle_get_tasks, handle_add_task, handle_update_task

class ScrumAppHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        
        try:
            # Serve static files
            if self.path.endswith(".html") or self.path.endswith(".css") or self.path.endswith(".js"):
                file_path = self.path.lstrip("/")
                if os.path.exists(file_path):
                    self.send_response(200)
                    if self.path.endswith(".html"):
                        self.send_header("Content-Type", "text/html")
                    elif self.path.endswith(".css"):
                        self.send_header("Content-Type", "text/css")
                    elif self.path.endswith(".js"):
                        self.send_header("Content-Type", "application/javascript")
                    self.end_headers()
                    with open(file_path, "rb") as file:
                        self.wfile.write(file.read())
                else:
                    self.send_error(404, f"File Not Found: {self.path}")
            # Serve API for tasks
            elif self.path == "/tasks":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                tasks_list = handle_get_tasks()
                self.wfile.write(json.dumps(tasks_list).encode())
            else:
                self.send_error(404, "API Endpoint Not Found")
        except Exception as e:
            self.send_error(500, str(e))

    def do_POST(self):
        if self.path == "/add-task":
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                task_data = json.loads(post_data)

                task_id = handle_add_task(task_data)
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "id": task_id,
                    "title": task_data['title'],
                    "description": task_data['description'],
                    "status": 'todo'
                }).encode())
            except Exception as e:
                self.send_error(500, str(e))

        elif self.path.startswith("/update-task/"):
            try:
                task_id = self.path.split("/")[-1]
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                task_data = json.loads(post_data)

                handle_update_task(task_id, task_data)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404, "API Endpoint Not Found")
