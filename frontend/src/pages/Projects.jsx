import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";
import Layout from "../components/Layout";
import Modal from "../components/Modal";

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ title: "", description: "" });
  const [saving, setSaving] = useState(false);

  const load = () => api.get("/projects/").then((r) => setProjects(r.data));
  useEffect(() => { load(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setSaving(true);
    await api.post("/projects/", form);
    setForm({ title: "", description: "" });
    setShowModal(false);
    await load();
    setSaving(false);
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete this project and all its tasks?")) return;
    await api.delete(`/projects/${id}`);
    setProjects((p) => p.filter((x) => x.id !== id));
  };

  return (
    <Layout title="Projects">
      <div className="section-header">
        <h2>All Projects</h2>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>+ New Project</button>
      </div>

      {projects.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📁</div>
          <p>No projects yet. Create your first one!</p>
        </div>
      ) : (
        <div className="card-grid">
          {projects.map((p) => (
            <div className="card" key={p.id}>
              <div className="flex items-center justify-between">
                <Link to={`/projects/${p.id}`}>
                  <div className="card-title" style={{ color: "var(--primary)", cursor: "pointer" }}>📁 {p.title}</div>
                </Link>
                <button className="btn btn-danger btn-sm" onClick={() => handleDelete(p.id)}>Delete</button>
              </div>
              <div className="card-meta mt-2">{p.description || "No description"}</div>
              <div className="card-meta mt-2">Created: {new Date(p.created_at).toLocaleDateString()}</div>
              <Link to={`/projects/${p.id}`} className="btn btn-ghost btn-sm" style={{ marginTop: 12 }}>
                View Tasks →
              </Link>
            </div>
          ))}
        </div>
      )}

      {showModal && (
        <Modal
          title="New Project"
          onClose={() => setShowModal(false)}
          footer={
            <>
              <button className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancel</button>
              <button className="btn btn-primary" form="project-form" type="submit" disabled={saving}>
                {saving ? "Creating…" : "Create"}
              </button>
            </>
          }
        >
          <form id="project-form" onSubmit={handleCreate}>
            <div className="form-group">
              <label>Title *</label>
              <input required value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} placeholder="Project name" />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} placeholder="Optional description" />
            </div>
          </form>
        </Modal>
      )}
    </Layout>
  );
}
