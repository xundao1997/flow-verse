# Verse Web

`verse-web` is a reusable frontend foundation for future product work inside `flow-verse`. It provides a production-oriented React + TypeScript + Vite baseline with routing, shared layout, Tailwind styling, Zustand state, TanStack Query wiring, a request client, React Hook Form integration, Jest-based tests, and ESLint-based static checks.

## Version Notes

The requested stack contained version combinations that are risky together in a modern React 19 setup. To keep the project runnable and maintainable, this scaffold uses:

- React `19.1.0`
- TypeScript `4.9.5` instead of `4.5.0`
- Vite `4.5.14` within the requested Vite 4 major
- Tailwind CSS `3.4.17` within the requested Tailwind 3 major
- React Router `6.30.1` within the requested React Router 6 major
- Zustand `4.5.7` within the requested Zustand 4 major
- TanStack Query `5.59.0` instead of React Query 3 because React Query 3 does not support React 19 peer dependencies
- React Hook Form `7.54.2` within the requested RHF 7 major
- Jest `27.5.1`

This keeps the skeleton aligned with your requested ecosystem while avoiding a brittle or non-runnable dependency set.

## Project Structure

```text
verse-web/
|-- .env.example
|-- .eslintrc.cjs
|-- .gitignore
|-- index.html
|-- jest.config.cjs
|-- jest.setup.ts
|-- package.json
|-- postcss.config.cjs
|-- README.md
|-- tailwind.config.cjs
|-- tsconfig.jest.json
|-- tsconfig.json
|-- tsconfig.node.json
|-- vite.config.ts
|-- public/
|   `-- verse-mark.svg
`-- src/
    |-- app/
    |-- components/
    |-- config/
    |-- hooks/
    |-- layouts/
    |-- pages/
    |-- router/
    |-- services/
    |-- store/
    |-- styles/
    |-- test/
    |-- types/
    |-- utils/
    |-- main.tsx
    `-- vite-env.d.ts
```

## Included Foundations

- React 19 application entry with Vite build tooling
- Route registry with lazy-loaded pages and 404 fallback
- Global shell layout and neutral example pages
- Zustand store with an extendable slice pattern
- TanStack Query provider and query bootstrap example
- Generic HTTP request client with timeout and typed error handling
- React Hook Form example with validation and submission preview
- Tailwind CSS theme setup and global style entry
- Jest + React Testing Library coverage for rendering, routing, request, and state basics
- ESLint for TypeScript, React, and React Hooks checks
- Centralized environment variable access through `src/config/env.ts`

## Environment Variables

Create a local `.env` file from `.env.example`.

```bash
cp .env.example .env
```

Available variables:

- `VITE_APP_NAME`: frontend application display name
- `VITE_API_BASE_URL`: default base URL used by the request client
- `VITE_REQUEST_TIMEOUT_MS`: default request timeout in milliseconds

### Runtime Contexts

- Local frontend + local backend: keep `VITE_API_BASE_URL=http://localhost:8000/api/v1`
- Docker Compose deployment in this repository: the backend is also exposed on `http://localhost:8000/api/v1`
- Built frontend containers are static; changing `VITE_*` values requires rebuilding the image

## Install and Start

```bash
npm install
npm run lint
npm test
npm run build
npm run dev
```

Default local dev server: `http://localhost:5173`

## Extension Guidance

- Add new feature pages under `src/pages/` and register them in `src/router/routes.tsx`
- Split the Zustand store into additional files when domain state appears
- Add API modules beside `src/services/http/client.ts` rather than mixing request logic into components
- Keep environment parsing centralized in `src/config/env.ts`
- The current env loader uses a single Vite-injected `__APP_ENV__` object so Vite builds and Jest share one configuration entry point
- Add shared UI primitives under `src/components/common/` and feature-specific components under dedicated folders
