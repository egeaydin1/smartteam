import { useAuth } from "../context/AuthContext";
import Sidebar from "./Sidebar";

export default function Layout({ title, children }) {
  const { user } = useAuth();
  return (
    <div className="layout">
      <Sidebar />
      <div className="main">
        <div className="topbar">
          <h1>{title}</h1>
          <div className="user-chip">
            <span>{user?.email}</span>
            <span className={`badge badge-${user?.role?.toLowerCase()}`}>{user?.role}</span>
          </div>
        </div>
        <div className="page">{children}</div>
      </div>
    </div>
  );
}
