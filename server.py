from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json
import urllib.parse

class ScrumAppHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/tasks":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, description, status FROM tasks")
            tasks = cursor.fetchall()

            tasks_list = []
            for task in tasks:
                tasks_list.append({
                    "id": task[0],
                    "title": task[1],
                    "description": task[2],
                    "status": task[3]
                })

            self.wfile.write(json.dumps(tasks_list).encode())
            conn.close()
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/add-task":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_data = json.loads(post_data)

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
                           (task_data['title'], task_data['description'], 'todo'))
            conn.commit()
            task_id = cursor.lastrowid
            conn.close()

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "id": task_id,
                "title": task_data['title'],
                "description": task_data['description'],
                "status": 'todo'
            }).encode())
        else:
            self.send_error(404)


def run(server_class=HTTPServer, handler_class=ScrumAppHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Starting server on port 8000...')
    httpd.serve_forever()

if __name__ == "__main__":
    # Initialize the database if it doesn't exist
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    run()
