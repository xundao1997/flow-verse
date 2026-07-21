import eslint from "@eslint/js";
import tseslint from "typescript-eslint";

const browserGlobals = {
  AbortController: "readonly",
  DOMException: "readonly",
  document: "readonly",
  fetch: "readonly",
  window: "readonly",
};

export default tseslint.config(
  {
    ignores: ["dist", "coverage"],
  },
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ["src/**/*.{ts,tsx}"],
    languageOptions: {
      globals: browserGlobals,
    },
  },
);
