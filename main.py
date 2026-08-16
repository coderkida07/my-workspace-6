import sqlite3
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")
DATABASE = "todo.db"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
            """
        )


@app.get("/")
def home():
    return send_from_directory(".", "index.html")


@app.get("/api/tasks")
def get_tasks():
    with get_db() as connection:
        rows = connection.execute(
            "SELECT id, title, completed FROM tasks ORDER BY id DESC"
        ).fetchall()
    return jsonify([
        {"id": row["id"], "title": row["title"], "completed": bool(row["completed"])}
        for row in rows
    ])


@app.post("/api/tasks")
def add_task():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify({"error": "Task title is required"}), 400

    with get_db() as connection:
        cursor = connection.execute(
            "INSERT INTO tasks (title, completed) VALUES (?, 0)", (title,)
        )
        task_id = cursor.lastrowid

    return jsonify({"id": task_id, "title": title, "completed": False}), 201


@app.patch("/api/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json(silent=True) or {}

    with get_db() as connection:
        task = connection.execute(
            "SELECT id, title, completed FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

        if task is None:
            return jsonify({"error": "Task not found"}), 404

        title = str(data.get("title", task["title"])).strip()
        completed = int(bool(data.get("completed", bool(task["completed"]))))

        if not title:
            return jsonify({"error": "Task title cannot be empty"}), 400

        connection.execute(
            "UPDATE tasks SET title = ?, completed = ? WHERE id = ?",
            (title, completed, task_id),
        )

    return jsonify({"id": task_id, "title": title, "completed": bool(completed)})


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    with get_db() as connection:
        cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    if cursor.rowcount == 0:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted"})


init_db()

if __name__ == "__main__":
    app.run(debug=True)
