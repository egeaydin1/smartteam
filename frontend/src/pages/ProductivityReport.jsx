import { useEffect, useState } from "react";
import api from "../api/client";
import Layout from "../components/Layout";
import { useAuth } from "../context/AuthContext";

export default function ProductivityReport() {
  const { user } = useAuth();
  const [tasks,   setTasks]   = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/projects/").then(async (r) => {
      const all = await Promise.all(
        r.data.map((p) => api.get(`/projects/${p.id}/tasks/`).then((t) => t.data))
      );
      setTasks(all.flat().filter((t) => t.assigned_to === user?.id));
    }).finally(() => setLoading(false));
  }, [user]);

  const total    = tasks.length;
  const done     = tasks.filter((t) => t.status === "DONE").length;
  const inProg   = tasks.filter((t) => t.status === "IN_PROGRESS").length;
  const todo     = tasks.filter((t) => t.status === "TO_DO").length;
  const overdue  = tasks.filter((t) => {
    if (!t.deadline || t.status === "DONE") return false;
    return new Date(t.deadline) < new Date();
  }).length;
  const pct = total ? Math.round((done / total) * 100) : 0;

  if (loading) return <Layout title="My Report"><p>Loading…</p></Layout>;

  return (
    <Layout title="Productivity Report">
      <div className="card" style={{ maxWidth: 600, marginBottom: 24 }}>
        <h2 style={{ marginBottom: 16, fontSize: "1rem", fontWeight: 600 }}>
          {user?.username}'s Task Summary
        </h2>

        <div className="stat-grid" style={{ marginBottom: 20 }}>
          <div className="stat-card"><div className="stat-value">{total}</div><div className="stat-label">Total Assigned</div></div>
          <div className="stat-card"><div className="stat-value" style={{ color: "var(--success)" }}>{done}</div><div className="stat-label">Completed</div></div>
          <div className="stat-card"><div className="stat-value" style={{ color: "var(--warn)" }}>{inProg}</div><div className="stat-label">In Progress</div></div>
          <div className="stat-card"><div className="stat-value">{todo}</div><div className="stat-label">To Do</div></div>
          <div className="stat-card"><div className="stat-value" style={{ color: "var(--danger)" }}>{overdue}</div><div className="stat-label">Overdue</div></div>
        </div>

        <div style={{ marginBottom: 8 }}>
          <div className="flex items-center justify-between text-sm" style={{ marginBottom: 6 }}>
            <span>Completion rate</span>
            <strong>{pct}%</strong>
          </div>
          <div className="progress-bar-bg">
            <div className="progress-bar-fill" style={{ width: `${pct}%`, background: pct === 100 ? "var(--success)" : "var(--primary)" }} />
          </div>
        </div>
      </div>

      <div className="section-header"><h2>My Tasks</h2></div>
      {tasks.length === 0 ? (
        <div className="empty-state"><div className="empty-icon">📈</div><p>No tasks assigned to you yet.</p></div>
      ) : (
        <div className="card">
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Title</th><th>Status</th><th>Priority</th><th>Deadline</th><th>Overdue?</th>
                </tr>
              </thead>
              <tbody>
                {tasks.map((t) => {
                  const od = t.deadline && t.status !== "DONE" && new Date(t.deadline) < new Date();
                  return (
                    <tr key={t.id}>
                      <td>{t.title}</td>
                      <td><span className={`chip chip-${t.status.toLowerCase()}`}>{t.status.replace("_", " ")}</span></td>
                      <td><span className={`chip chip-${t.priority.toLowerCase()}`}>{t.priority}</span></td>
                      <td>{t.deadline || "—"}</td>
                      <td>{od ? <span style={{ color: "var(--danger)", fontWeight: 600 }}>⚠ Yes</span> : "—"}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </Layout>
  );
}
