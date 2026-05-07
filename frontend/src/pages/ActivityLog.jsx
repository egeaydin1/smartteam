import { useEffect, useState } from "react";
import api from "../api/client";
import Layout from "../components/Layout";

export default function ActivityLog() {
  const [users,    setUsers]    = useState([]);
  const [projects, setProjects] = useState([]);
  const [tasks,    setTasks]    = useState([]);
  const [loading,  setLoading]  = useState(true);

  useEffect(() => {
    Promise.all([
      api.get("/users/"),
      api.get("/projects/"),
    ]).then(async ([u, p]) => {
      setUsers(u.data);
      setProjects(p.data);
      const allTasks = await Promise.all(
        p.data.map((proj) => api.get(`/projects/${proj.id}/tasks/`).then((r) => r.data))
      );
      setTasks(allTasks.flat());
    }).finally(() => setLoading(false));
  }, []);

  const tasksByProject = projects.map((p) => ({
    ...p,
    tasks: tasks.filter((t) => t.project_id === p.id),
  }));

  if (loading) return <Layout title="System Activity"><p>Loading…</p></Layout>;

  return (
    <Layout title="System Activity Monitor">
      {/* System-wide stats */}
      <div className="stat-grid" style={{ marginBottom: 28 }}>
        <div className="stat-card"><div className="stat-value">{users.length}</div><div className="stat-label">Total Users</div></div>
        <div className="stat-card"><div className="stat-value">{users.filter((u) => u.role === "ADMIN").length}</div><div className="stat-label">Admins</div></div>
        <div className="stat-card"><div className="stat-value">{users.filter((u) => u.is_active).length}</div><div className="stat-label">Active Users</div></div>
        <div className="stat-card"><div className="stat-value">{projects.length}</div><div className="stat-label">Projects</div></div>
        <div className="stat-card"><div className="stat-value">{tasks.length}</div><div className="stat-label">Total Tasks</div></div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: "var(--success)" }}>
            {tasks.filter((t) => t.status === "DONE").length}
          </div>
          <div className="stat-label">Completed</div>
        </div>
      </div>

      {/* Per-project breakdown */}
      <div className="section-header"><h2>Project Breakdown</h2></div>
      <div className="card">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Project</th><th>Owner ID</th><th>Total Tasks</th>
                <th>To Do</th><th>In Progress</th><th>Done</th><th>Completion</th>
              </tr>
            </thead>
            <tbody>
              {tasksByProject.map((p) => {
                const todo = p.tasks.filter((t) => t.status === "TO_DO").length;
                const inp  = p.tasks.filter((t) => t.status === "IN_PROGRESS").length;
                const done = p.tasks.filter((t) => t.status === "DONE").length;
                const pct  = p.tasks.length ? Math.round((done / p.tasks.length) * 100) : 0;
                return (
                  <tr key={p.id}>
                    <td><strong>{p.title}</strong></td>
                    <td>{p.owner_id}</td>
                    <td>{p.tasks.length}</td>
                    <td>{todo}</td>
                    <td>{inp}</td>
                    <td>{done}</td>
                    <td>
                      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                        <div className="progress-bar-bg" style={{ width: 80 }}>
                          <div className="progress-bar-fill" style={{ width: `${pct}%` }} />
                        </div>
                        <span className="text-sm">{pct}%</span>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Users table */}
      <div className="section-header" style={{ marginTop: 32 }}><h2>Registered Users</h2></div>
      <div className="card">
        <div className="table-wrap">
          <table>
            <thead>
              <tr><th>ID</th><th>Username</th><th>Email</th><th>Role</th><th>Status</th><th>Joined</th></tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td>{u.id}</td>
                  <td>{u.username}</td>
                  <td>{u.email}</td>
                  <td><span className={`badge badge-${u.role.toLowerCase()}`}>{u.role}</span></td>
                  <td><span style={{ color: u.is_active ? "var(--success)" : "var(--danger)", fontWeight: 600, fontSize: ".82rem" }}>{u.is_active ? "Active" : "Inactive"}</span></td>
                  <td className="text-muted text-sm">{new Date(u.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Layout>
  );
}
