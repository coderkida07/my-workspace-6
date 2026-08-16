from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")

tasks = []
next_id = 1


@app.get("/")
def home():
    return send_from_directory(".", "index.html")


@app.get("/api/tasks")
def get_tasks():
    return jsonify(tasks)


@app.post("/api/tasks")
def add_task():
    global next_id
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify({"error": "Task title is required"}), 400

    task = {"id": next_id, "title": title, "completed": False}
    tasks.append(task)
    next_id += 1
    return jsonify(task), 201


@app.patch("/api/tasks/<int:task_id>")
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json(silent=True) or {}
    if "completed" in data:
        task["completed"] = bool(data["completed"])
    if "title" in data:
        title = str(data["title"]).strip()
        if title:
            task["title"] = title
    return jsonify(task)


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    global tasks
    original_length = len(tasks)
    tasks = [task for task in tasks if task["id"] != task_id]
    if len(tasks) == original_length:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":
    app.run(debug=True)
