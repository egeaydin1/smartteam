import { useEffect, useState } from "react";
import api from "../api/client";
import Layout from "../components/Layout";

export default function AdminUsers() {
  const [users,   setUsers]   = useState([]);
  const [loading, setLoading] = useState(true);

  const load = () => api.get("/users/").then((r) => setUsers(r.data)).finally(() => setLoading(false));
  useEffect(() => { load(); }, []);

  const toggleActive = async (u) => {
    await api.patch(`/users/${u.id}`, { is_active: !u.is_active });
    setUsers((prev) => prev.map((x) => x.id === u.id ? { ...x, is_active: !x.is_active } : x));
  };

  const changeRole = async (u, role) => {
    await api.patch(`/users/${u.id}`, { role });
    setUsers((prev) => prev.map((x) => x.id === u.id ? { ...x, role } : x));
  };

  if (loading) return <Layout title="Manage Users"><p>Loading…</p></Layout>;

  return (
    <Layout title="Manage Users">
      <div className="card">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th><th>Username</th><th>Email</th><th>Role</th><th>Status</th><th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td>{u.id}</td>
                  <td><strong>{u.username}</strong></td>
                  <td>{u.email}</td>
                  <td>
                    <select
                      value={u.role}
                      onChange={(e) => changeRole(u, e.target.value)}
                      style={{ padding: "4px 8px", borderRadius: 6, border: "1px solid var(--border)", fontSize: ".8rem" }}
                    >
                      <option value="MEMBER">MEMBER</option>
                      <option value="ADMIN">ADMIN</option>
                    </select>
                  </td>
                  <td>
                    <span style={{ color: u.is_active ? "var(--success)" : "var(--danger)", fontWeight: 600, fontSize: ".82rem" }}>
                      {u.is_active ? "Active" : "Inactive"}
                    </span>
                  </td>
                  <td>
                    <button
                      className={`btn btn-sm ${u.is_active ? "btn-danger" : "btn-primary"}`}
                      onClick={() => toggleActive(u)}
                    >
                      {u.is_active ? "Deactivate" : "Activate"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Layout>
  );
}
