import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// API_HOST is set to http://api:8000 inside Docker Compose.
// Falls back to localhost for local dev without Docker.
const API_HOST = process.env.API_HOST || "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true, // bind to 0.0.0.0 so Docker exposes the port
    proxy: {
      "/api": {
        target: API_HOST,
        changeOrigin: true,
      },
    },
  },
});
