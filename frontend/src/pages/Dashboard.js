import { useEffect, useState } from "react";
import { apiFetch } from "../api";

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(true);

  // Load tasks from backend
  const loadTasks = async () => {
    setLoading(true);
    try {
      const data = await apiFetch("/tasks");
      // Make sure tasks is always an array
      setTasks(Array.isArray(data) ? data : data.tasks || []);
    } catch (err) {
      console.error("Failed to load tasks:", err);
      setTasks([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  // Add new task
  const addTask = async () => {
    if (!title.trim()) return alert("Task title cannot be empty");

    try {
      await apiFetch("/tasks", {
        method: "POST",
        body: JSON.stringify({ title: title.trim() }),
      });
      setTitle("");
      loadTasks();
    } catch (err) {
      console.error("Failed to add task:", err);
    }
  };

  // Delete task
  const deleteTask = async (id) => {
    if (!window.confirm("Are you sure you want to delete this task?")) return;

    try {
      await apiFetch(`/tasks/${id}`, { method: "DELETE" });
      loadTasks();
    } catch (err) {
      console.error("Failed to delete task:", err);
    }
  };

  // Update task title
  const updateTask = async (id) => {
    const newTitle = prompt("New title?");
    if (!newTitle || !newTitle.trim()) return;

    try {
      await apiFetch(`/tasks/${id}`, {
        method: "PUT",
        body: JSON.stringify({ title: newTitle.trim() }),
      });
      loadTasks();
    } catch (err) {
      console.error("Failed to update task:", err);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto" }}>
      <h2>Dashboard</h2>

      <div style={{ marginBottom: "1rem" }}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New Task"
          style={{ padding: "0.5rem", width: "70%" }}
        />
        <button onClick={addTask} style={{ padding: "0.5rem", marginLeft: "0.5rem" }}>
          Add
        </button>
      </div>

      {loading ? (
        <p>Loading tasks...</p>
      ) : tasks.length === 0 ? (
        <p>No tasks yet!</p>
      ) : (
        <ul>
          {tasks.map((t) => (
            <li key={t.id} style={{ marginBottom: "0.5rem" }}>
              {t.title}{" "}
              <button onClick={() => updateTask(t.id)} style={{ marginLeft: "0.5rem" }}>
                Edit
              </button>
              <button onClick={() => deleteTask(t.id)} style={{ marginLeft: "0.5rem" }}>
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}