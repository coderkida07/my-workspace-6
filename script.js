const form = document.getElementById("task-form");
const input = document.getElementById("task-input");
const list = document.getElementById("task-list");
const count = document.getElementById("task-count");
const emptyState = document.getElementById("empty-state");
const clearCompleted = document.getElementById("clear-completed");

async function loadTasks() {
  const response = await fetch("/api/tasks");
  const tasks = await response.json();
  renderTasks(tasks);
}

function renderTasks(tasks) {
  list.innerHTML = "";
  emptyState.hidden = tasks.length > 0;
  count.textContent = `${tasks.length} ${tasks.length === 1 ? "task" : "tasks"}`;

  tasks.forEach((task) => {
    const item = document.createElement("li");
    item.className = `task-item${task.completed ? " completed" : ""}`;

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = task.completed;
    checkbox.setAttribute("aria-label", `Complete ${task.title}`);
    checkbox.addEventListener("change", () => toggleTask(task.id, checkbox.checked));

    const label = document.createElement("label");
    label.textContent = task.title;

    const deleteButton = document.createElement("button");
    deleteButton.className = "delete-button";
    deleteButton.type = "button";
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => deleteTask(task.id));

    item.append(checkbox, label, deleteButton);
    list.appendChild(item);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const title = input.value.trim();
  if (!title) return;

  const response = await fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });

  if (response.ok) {
    input.value = "";
    input.focus();
    await loadTasks();
  }
});

async function toggleTask(id, completed) {
  await fetch(`/api/tasks/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed }),
  });
  await loadTasks();
}

async function deleteTask(id) {
  await fetch(`/api/tasks/${id}`, { method: "DELETE" });
  await loadTasks();
}

clearCompleted.addEventListener("click", async () => {
  const response = await fetch("/api/tasks");
  const tasks = await response.json();
  await Promise.all(
    tasks.filter((task) => task.completed).map((task) =>
      fetch(`/api/tasks/${task.id}`, { method: "DELETE" })
    )
  );
  await loadTasks();
});

loadTasks().catch(() => {
  emptyState.textContent = "Could not connect to the backend. Start the Flask server and try again.";
  emptyState.hidden = false;
});
