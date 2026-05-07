import { useEffect, useState } from "react";
import api from "../api/client";
import { useAuth } from "../context/AuthContext";

export default function CommentSection({ projectId, taskId }) {
  const { user } = useAuth();
  const [comments, setComments] = useState([]);
  const [content, setContent]   = useState("");
  const [saving, setSaving]     = useState(false);

  const load = () =>
    api.get(`/projects/${projectId}/tasks/${taskId}/comments/`)
      .then((r) => setComments(r.data));

  useEffect(() => { load(); }, [taskId]);

  const submit = async (e) => {
    e.preventDefault();
    if (!content.trim()) return;
    setSaving(true);
    await api.post(`/projects/${projectId}/tasks/${taskId}/comments/`, { content });
    setContent("");
    await load();
    setSaving(false);
  };

  const remove = async (id) => {
    await api.delete(`/projects/${projectId}/tasks/${taskId}/comments/${id}`);
    setComments((c) => c.filter((x) => x.id !== id));
  };

  return (
    <div style={{ marginTop: 20 }}>
      <strong style={{ fontSize: ".85rem" }}>Comments ({comments.length})</strong>
      <div className="comment-list">
        {comments.map((c) => (
          <div className="comment-item" key={c.id}>
            <div>
              <span className="comment-author">User #{c.user_id}</span>
              <span className="comment-date">{new Date(c.created_at).toLocaleString()}</span>
              {(user?.id === c.user_id || user?.role === "ADMIN") && (
                <button
                  className="btn btn-ghost btn-sm"
                  style={{ float: "right", padding: "2px 8px" }}
                  onClick={() => remove(c.id)}
                >✕</button>
              )}
            </div>
            <p style={{ marginTop: 4 }}>{c.content}</p>
          </div>
        ))}
        {comments.length === 0 && <p className="text-muted text-sm">No comments yet.</p>}
      </div>
      <form onSubmit={submit} style={{ marginTop: 12, display: "flex", gap: 8 }}>
        <input
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Add a comment…"
          style={{ flex: 1, padding: "8px 12px", borderRadius: 8, border: "1px solid var(--border)", fontSize: ".875rem" }}
        />
        <button className="btn btn-primary btn-sm" disabled={saving}>
          {saving ? "…" : "Post"}
        </button>
      </form>
    </div>
  );
}
