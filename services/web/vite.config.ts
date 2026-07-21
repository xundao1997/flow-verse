import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const environment = loadEnv(mode, "../../", "FLOWVERSE_");
  const host = environment.FLOWVERSE_API_HOST || "127.0.0.1";
  const port = environment.FLOWVERSE_API_PORT || "8000";
  const target = environment.FLOWVERSE_API_BASE_URL || `http://${host}:${port}`;

  return {
    server: {
      proxy: {
        "/api": {
          target,
          changeOrigin: false,
        },
      },
    },
  };
});
