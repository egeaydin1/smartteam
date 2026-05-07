import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const links = [
  { to: "/",         label: "Dashboard",   icon: "📊" },
  { to: "/projects", label: "Projects",    icon: "📁" },
  { to: "/report",   label: "My Report",   icon: "📈" },
];

const adminLinks = [
  { to: "/admin/users",    label: "Manage Users",    icon: "👥" },
  { to: "/admin/activity", label: "System Activity", icon: "🔍" },
];

export default function Sidebar() {
  const { user, logout } = useAuth();
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">⚡ SmartTeam</div>
      <nav>
        {links.map((l) => (
          <NavLink key={l.to} to={l.to} end={l.to === "/"}>
            <span>{l.icon}</span> {l.label}
          </NavLink>
        ))}
        {user?.role === "ADMIN" && (
          <>
            <hr style={{ border: "none", borderTop: "1px solid rgba(255,255,255,.15)", margin: "10px 24px" }} />
            {adminLinks.map((l) => (
              <NavLink key={l.to} to={l.to}>
                <span>{l.icon}</span> {l.label}
              </NavLink>
            ))}
          </>
        )}
      </nav>
      <div className="sidebar-footer">
        <div style={{ fontSize: ".8rem", marginBottom: 10, opacity: .7 }}>
          {user?.username} · {user?.role}
        </div>
        <button onClick={logout}>Sign out</button>
      </div>
    </aside>
  );
}
