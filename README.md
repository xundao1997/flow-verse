# Flow Verse

`flow-verse` is a two-project workspace that contains a frontend delivery surface (`verse-web`) and a backend service foundation (`verse-agent`). The repository is structured for continued product development and includes Docker build assets for both applications so the codebase can be built by local Docker tooling or Alibaba Cloud Yunxiao image pipelines.

## Repository Structure

```text
flow-verse/
|-- README.md
|-- .env.example
|-- .gitignore
|-- docker-compose.yml
|-- verse-agent/
|   |-- Dockerfile
|   |-- .dockerignore
|   |-- pyproject.toml
|   |-- .env.example
|   |-- src/
|   `-- tests/
`-- verse-web/
    |-- Dockerfile
    |-- .dockerignore
    |-- nginx/
    |   `-- default.conf
    |-- package.json
    |-- .env.example
    |-- src/
    `-- public/
```

## Technology Stack

### Backend: `verse-agent`
- Python 3.11
- FastAPI
- SQLAlchemy async + aiomysql
- Redis
- Celery
- Loguru
- Pytest

### Frontend: `verse-web`
- React 19
- TypeScript 4.9
- Vite 4
- Tailwind CSS 3
- React Router 6
- Zustand 4
- TanStack Query 5
- React Hook Form 7
- Jest 27 + React Testing Library
- ESLint

## Local Development

### Backend
```bash
cd verse-agent
pip install -e .[dev]
python -m pytest
uvicorn verse_agent.main:create_app --factory --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd verse-web
npm install
npm run lint
npm test
npm run build
npm run dev
```

### Local Port Convention
- Backend direct run: `http://localhost:8000`
- Frontend dev server: `http://localhost:5173`
- Frontend default API target in local development: `http://localhost:8000/api/v1`

## Docker Build

### Backend Image
```bash
docker build -t flow-verse/verse-agent:latest ./verse-agent
```

Build once and reuse the same image for a Celery worker by overriding the container command.

### Frontend Image
```bash
docker build   --build-arg VITE_APP_NAME="Verse Web"   --build-arg VITE_API_BASE_URL="http://localhost:8000/api/v1"   --build-arg VITE_REQUEST_TIMEOUT_MS=8000   -t flow-verse/verse-web:latest ./verse-web
```

`verse-web` is a static Vite application, so its `VITE_*` values are compiled into the build during image creation.

## Docker Compose

The repository-level `docker-compose.yml` intentionally packages only the application containers. It assumes MySQL and Redis already exist outside the stack and injects their endpoints through environment variables.

```bash
docker compose --env-file .env.example up -d
```

Compose port convention:
- Backend container and host port: `8000`
- Frontend container port: `80`
- Frontend published host port: `80`

This keeps Docker and local backend defaults aligned.

## Docker Run

### Backend API
```bash
docker run --rm -p 8000:8000 --env-file verse-agent/.env.example flow-verse/verse-agent:latest
```

### Backend Celery Worker
```bash
docker run --rm --env-file verse-agent/.env.example flow-verse/verse-agent:latest   celery -A verse_agent.tasks.celery_app.celery_app worker --loglevel=INFO
```

### Frontend Web Server
```bash
docker run --rm -p 80:80 flow-verse/verse-web:latest
```

## Deployment Notes

- The Dockerfiles are suitable for Rocky Linux 9.7 hosts because container builds are isolated from the host OS.
- The frontend image uses multi-stage Node + Nginx packaging for a small runtime image.
- The backend image uses a multi-stage Python wheel build to separate build-time tooling from runtime layers.
- The backend service expects external MySQL and Redis infrastructure; those services are not bundled into this repository.
- The repository does not yet include Yunxiao pipeline YAML, Kubernetes manifests, or Compose-managed worker services.

## Yunxiao Guidance

When configuring Alibaba Cloud Yunxiao:

1. Use the repository root as the checkout directory.
2. Configure two image build tasks with different build contexts:
   - `verse-agent`
   - `verse-web`
3. For the frontend task, pass the desired `VITE_*` build arguments per environment.
4. Inject backend runtime secrets through Yunxiao environment variables or secret management, not through committed files.
5. Run project verification before image publishing:
   - backend: `python -m pytest`
   - frontend: `npm run lint`, `npm test`, and `npm run build`

## Current State and Constraints

- Docker CLI is not available in the current local environment, so the Dockerfiles and compose file were updated from the real project structure but were not executed with `docker build` or `docker compose` here.
- The frontend runtime configuration is build-time only. Changing `VITE_*` values requires rebuilding the frontend image.
- The backend image can serve either FastAPI or Celery by changing the container command at runtime.
- The repository-level compose file is intentionally not a full local stack; it targets deployments with externally managed MySQL and Redis.

## Extension Suggestions

- Add Yunxiao pipeline configuration files once the target registry, namespaces, and deployment stages are finalized.
- Add a separate full-stack local compose file if you want this repository to run MySQL, Redis, and a Celery worker on one command.
- Introduce separate production env templates distinct from `.env.example` once real deployment values and secret sources are defined.
- Consider adding container health checks once deployment targets and ingress behavior are fixed.
