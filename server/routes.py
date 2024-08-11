import json
from server.database import get_db_connection

def handle_get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, status FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    tasks_list = []
    for task in tasks:
        tasks_list.append({
            "id": task["id"],
            "title": task["title"],
            "description": task["description"],
            "status": task["status"]
        })
    return tasks_list

def handle_add_task(task_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
                   (task_data['title'], task_data['description'], 'todo'))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def handle_update_task(task_id, task_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", 
                   (task_data['status'], task_id))
    conn.commit()
    conn.close()
