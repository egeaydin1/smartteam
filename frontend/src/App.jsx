import { Navigate, Route, Routes } from "react-router-dom";
import PrivateRoute from "./components/PrivateRoute";
import ActivityLog from "./pages/ActivityLog";
import AdminUsers from "./pages/AdminUsers";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import ProductivityReport from "./pages/ProductivityReport";
import ProjectDetail from "./pages/ProjectDetail";
import Projects from "./pages/Projects";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
      <Route path="/projects" element={<PrivateRoute><Projects /></PrivateRoute>} />
      <Route path="/projects/:id" element={<PrivateRoute><ProjectDetail /></PrivateRoute>} />
      <Route path="/report" element={<PrivateRoute><ProductivityReport /></PrivateRoute>} />

      <Route path="/admin/users"    element={<PrivateRoute adminOnly><AdminUsers /></PrivateRoute>} />
      <Route path="/admin/activity" element={<PrivateRoute adminOnly><ActivityLog /></PrivateRoute>} />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
