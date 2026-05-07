import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";
import Layout from "../components/Layout";
import { useAuth } from "../context/AuthContext";

const STATUS_ORDER = ["TO_DO", "IN_PROGRESS", "DONE"];

export default function Dashboard() {
  const { user } = useAuth();
  const [projects, setProjects] = useState([]);
  const [tasks,    setTasks]    = useState([]);
  const [loading,  setLoading]  = useState(true);

  useEffect(() => {
    Promise.all([
      api.get("/projects/"),
      api.get("/projects/").then(async (r) => {
        const all = await Promise.all(
          r.data.map((p) => api.get(`/projects/${p.id}/tasks/`).then((t) => t.data))
        );
        return all.flat();
      }),
    ]).then(([p, t]) => { setProjects(p.data); setTasks(t); })
      .finally(() => setLoading(false));
  }, []);

  const counts = STATUS_ORDER.reduce((acc, s) => {
    acc[s] = tasks.filter((t) => t.status === s).length;
    return acc;
  }, {});

  const myTasks = tasks.filter((t) => t.assigned_to === user?.id);

  if (loading) return <Layout title="Dashboard"><p>Loading…</p></Layout>;

  return (
    <Layout title="Dashboard">
      {/* Stats */}
      <div className="stat-grid">
        <div className="stat-card">
          <div className="stat-value">{projects.length}</div>
          <div className="stat-label">Projects</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{tasks.length}</div>
          <div className="stat-label">Total Tasks</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{counts.TO_DO ?? 0}</div>
          <div className="stat-label">To Do</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{counts.IN_PROGRESS ?? 0}</div>
          <div className="stat-label">In Progress</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{counts.DONE ?? 0}</div>
          <div className="stat-label">Done</div>
        </div>
      </div>

      {/* My tasks */}
      <div className="section-header">
        <h2>My Assigned Tasks</h2>
        <Link to="/projects" className="btn btn-ghost btn-sm">All Projects →</Link>
      </div>
      {myTasks.length === 0 ? (
        <div className="empty-state"><div className="empty-icon">✅</div><p>No tasks assigned to you.</p></div>
      ) : (
        <div className="card-grid">
          {myTasks.map((t) => (
            <div className="card" key={t.id}>
              <div className="flex items-center justify-between">
                <span className={`chip chip-${t.status.toLowerCase()}`}>{t.status.replace("_", " ")}</span>
                <span className={`chip chip-${t.priority.toLowerCase()}`}>{t.priority}</span>
              </div>
              <div className="card-title mt-2">{t.title}</div>
              {t.deadline && <div className="card-meta">Due: {t.deadline}</div>}
            </div>
          ))}
        </div>
      )}

      {/* Recent projects */}
      <div className="section-header" style={{ marginTop: 32 }}>
        <h2>Recent Projects</h2>
      </div>
      <div className="card-grid">
        {projects.slice(0, 6).map((p) => (
          <Link to={`/projects/${p.id}`} key={p.id}>
            <div className="card" style={{ cursor: "pointer" }}>
              <div className="card-title">📁 {p.title}</div>
              <div className="card-meta">{p.description || "No description"}</div>
            </div>
          </Link>
        ))}
      </div>
    </Layout>
  );
}
