import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/client";
import CommentSection from "../components/CommentSection";
import Layout from "../components/Layout";
import Modal from "../components/Modal";
import { useAuth } from "../context/AuthContext";

const STATUSES  = ["TO_DO", "IN_PROGRESS", "DONE"];
const PRIORITIES = ["LOW", "MEDIUM", "HIGH"];

function TaskCard({ task, projectId, onAdvance, onDelete }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <div className="card" style={{ cursor: "pointer" }} onClick={() => setOpen(true)}>
        <div className="flex items-center justify-between">
          <span className={`chip chip-${task.status.toLowerCase()}`}>{task.status.replace("_", " ")}</span>
          <span className={`chip chip-${task.priority.toLowerCase()}`}>{task.priority}</span>
        </div>
        <div className="card-title mt-2">{task.title}</div>
        {task.deadline && <div className="card-meta">Due: {task.deadline}</div>}
        <div className="flex gap-2 mt-4">
          {task.status !== "DONE" && (
            <button className="btn btn-primary btn-sm" onClick={(e) => { e.stopPropagation(); onAdvance(task.id); }}>
              Advance ▶
            </button>
          )}
          <button className="btn btn-danger btn-sm" onClick={(e) => { e.stopPropagation(); onDelete(task.id); }}>
            Delete
          </button>
        </div>
      </div>

      {open && (
        <Modal title={task.title} onClose={() => setOpen(false)}>
          <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
            <span className={`chip chip-${task.status.toLowerCase()}`}>{task.status.replace("_", " ")}</span>
            <span className={`chip chip-${task.priority.toLowerCase()}`}>{task.priority}</span>
          </div>
          {task.deadline && <p className="text-muted text-sm">Deadline: {task.deadline}</p>}
          <hr className="divider" />
          <CommentSection projectId={projectId} taskId={task.id} />
        </Modal>
      )}
    </>
  );
}

export default function ProjectDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const [project, setProject] = useState(null);
  const [tasks,   setTasks]   = useState([]);
  const [filter,  setFilter]  = useState("ALL");
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ title: "", priority: "MEDIUM", deadline: "", assigned_to: "" });
  const [saving, setSaving] = useState(false);

  const loadProject = () => api.get(`/projects/${id}`).then((r) => setProject(r.data));
  const loadTasks   = () => api.get(`/projects/${id}/tasks/`).then((r) => setTasks(r.data));

  useEffect(() => { loadProject(); loadTasks(); }, [id]);

  const handleCreate = async (e) => {
    e.preventDefault();
    setSaving(true);
    const payload = { ...form };
    if (!payload.assigned_to) delete payload.assigned_to;
    if (!payload.deadline)    delete payload.deadline;
    await api.post(`/projects/${id}/tasks/`, payload);
    setForm({ title: "", priority: "MEDIUM", deadline: "", assigned_to: "" });
    setShowModal(false);
    await loadTasks();
    setSaving(false);
  };

  const handleAdvance = async (taskId) => {
    await api.post(`/projects/${id}/tasks/${taskId}/advance`);
    await loadTasks();
  };

  const handleDelete = async (taskId) => {
    if (!confirm("Delete task?")) return;
    await api.delete(`/projects/${id}/tasks/${taskId}`);
    setTasks((t) => t.filter((x) => x.id !== taskId));
  };

  const visible = filter === "ALL" ? tasks : tasks.filter((t) => t.status === filter);
  const done    = tasks.filter((t) => t.status === "DONE").length;
  const pct     = tasks.length ? Math.round((done / tasks.length) * 100) : 0;

  if (!project) return <Layout title="Loading…"><p>Loading…</p></Layout>;

  return (
    <Layout title={project.title}>
      {/* Progress */}
      <div className="card" style={{ marginBottom: 24 }}>
        <div className="flex items-center justify-between" style={{ marginBottom: 8 }}>
          <span className="text-sm text-muted">{done} / {tasks.length} tasks done</span>
          <span className="text-sm" style={{ fontWeight: 600 }}>{pct}%</span>
        </div>
        <div className="progress-bar-bg">
          <div className="progress-bar-fill" style={{ width: `${pct}%` }} />
        </div>
      </div>

      {/* Header */}
      <div className="section-header">
        <div style={{ display: "flex", gap: 8 }}>
          {["ALL", ...STATUSES].map((s) => (
            <button
              key={s}
              className={`btn btn-sm ${filter === s ? "btn-primary" : "btn-ghost"}`}
              onClick={() => setFilter(s)}
            >{s.replace("_", " ")}</button>
          ))}
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>+ New Task</button>
      </div>

      {/* Task grid */}
      {visible.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📋</div>
          <p>No tasks here yet.</p>
        </div>
      ) : (
        <div className="card-grid">
          {visible.map((t) => (
            <TaskCard
              key={t.id}
              task={t}
              projectId={id}
              onAdvance={handleAdvance}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}

      {/* Create Task Modal */}
      {showModal && (
        <Modal
          title="New Task"
          onClose={() => setShowModal(false)}
          footer={
            <>
              <button className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancel</button>
              <button className="btn btn-primary" form="task-form" type="submit" disabled={saving}>
                {saving ? "Creating…" : "Create"}
              </button>
            </>
          }
        >
          <form id="task-form" onSubmit={handleCreate}>
            <div className="form-group">
              <label>Title *</label>
              <input required value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
            </div>
            <div className="form-group">
              <label>Priority</label>
              <select value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })}>
                {PRIORITIES.map((p) => <option key={p}>{p}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label>Deadline</label>
              <input type="date" value={form.deadline} onChange={(e) => setForm({ ...form, deadline: e.target.value })} />
            </div>
            <div className="form-group">
              <label>Assign to (User ID)</label>
              <input type="number" value={form.assigned_to} onChange={(e) => setForm({ ...form, assigned_to: e.target.value })} placeholder="Optional" />
            </div>
          </form>
        </Modal>
      )}
    </Layout>
  );
}
