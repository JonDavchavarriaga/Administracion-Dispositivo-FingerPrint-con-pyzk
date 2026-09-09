# Biometric Attendance Platform

Enterprise-oriented biometric attendance platform built with Python, FastAPI, SQLAlchemy, MySQL, Celery, Redis, React and Vite. The project supports physical ZKTeco devices and a deterministic demo mode for portfolio demonstrations.

## Architecture

The backend follows a hexagonal architecture:

```text
Domain
  Entities, value objects and device roles
        |
Application
  Use cases and ports
  BiometricDeviceRepository
        |
Infrastructure
  ZKTeco/pyzk adapter
  Mock/Rush Hour adapter
  MySQL repositories
  Celery + Redis workers
        |
Delivery
  FastAPI REST and WebSocket endpoints
```

`pyzk` is isolated in `backend/src/infrastructure/devices/zk_device.py`. Application services only depend on the `BiometricDeviceRepository` port, so the mock and ZKTeco adapters use the same synchronization flow.

Each device returns a complete snapshot of users and attendance records. Synchronization processes snapshots in batches and uses the approved idempotency key:

```text
UNIQUE(device_id, user_external_id, timestamp)
```

The database schema is managed by Alembic. `cost_centers` is a dedicated normalized table, and `users.cost_center_id` is a foreign key.

## Repository structure

```text
backend/
  alembic/                       Database migrations
  src/application/ports/         Application contracts
  src/application/services/      Use cases
  src/domain/models/             Domain entities
  src/infrastructure/api/        REST and WebSocket delivery
  src/infrastructure/devices/    ZKTeco and mock adapters
  src/infrastructure/queue/      Celery application and tasks
  src/infrastructure/realtime/   In-memory WebSocket manager
frontend/
  src/api/                       REST clients
  src/hooks/                     React integration hooks
  src/pages/                     User-facing screens
docker-compose.yml               Local MySQL, Redis, API, workers and frontend
render.yaml                      Render web/worker/beat services
netlify.toml                     Netlify build and SPA fallback
```

## Demo / MOCK_MODE

Set `MOCK_MODE=True` to run without physical biometric devices. The mock adapter:

- Generates complete snapshots like the real hardware.
- Adds demo employees during subsequent cycles.
- Produces repeatable Rush Hour attendance bursts.
- Supports `ENTRY`, `EXIT` and `CAFETERIA` device roles.
- Uses the same Celery, persistence, deduplication and WebSocket paths as real devices.

The repository `.env.example` is configured for the portfolio demo. Copy it to `.env` before running locally:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

For real devices, set `MOCK_MODE=False` and register devices with reachable LAN addresses. The backend must run in a network environment that can route to the company LAN; Docker `network_mode: host` is intentionally preserved in the local Compose setup.

## Environment variables

### Backend

| Variable | Example | Purpose |
|---|---|---|
| `DB_HOST` | `127.0.0.1` | MySQL host when `DATABASE_URL` is not set |
| `DB_PORT` | `3306` | MySQL port |
| `DB_NAME` | `attendance` | Database name |
| `DB_USER` | `root` | Database user |
| `DB_PASSWORD` | `secret` | Database password |
| `DATABASE_URL` | `mysql+pymysql://...` | Full SQLAlchemy URL; recommended on Render |
| `REDIS_URL` | `redis://localhost:6379/0` | Celery broker/result backend |
| `CORS_ORIGINS` | `http://localhost:5173` | Comma-separated frontend origins |
| `MOCK_MODE` | `True` | Enable the demo adapter |
| `MOCK_SEED` | `42` | Reproducible demo data |
| `MOCK_BURST_SIZE` | `5` | Records generated per mock cycle |
| `ENABLE_LEGACY_SCHEDULER` | `False` | Only enable for legacy single-process scheduling; Celery Beat is preferred |

### Frontend

| Variable | Example | Purpose |
|---|---|---|
| `VITE_API_URL` | `http://localhost:8000` | Public backend URL used by Axios and WebSockets |

For Netlify, set `VITE_API_URL` to the Render API URL, for example `https://your-api.onrender.com`.

## Local services

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Services:

- Frontend: `http://localhost:5173`
- API: `http://localhost:8000`
- API health: `http://localhost:8000/health`
- Swagger: `http://localhost:8000/docs`
- Device WebSocket: `ws://localhost:8000/ws/devices`
- MySQL: `localhost:3306`
- Redis: `localhost:6379`

The API container applies `alembic upgrade head` before starting. Celery Worker processes synchronization jobs and Celery Beat schedules full snapshots every five minutes.

## Deploying the portfolio demo

### Render

The included `render.yaml` defines a web service for the no-dependency demo. Configure:

- `CORS_ORIGINS`: the Netlify site URL.
- `MOCK_MODE=True` for the public demo.

`DATABASE_URL` and `REDIS_URL` are intentionally omitted for this demo. The backend uses temporary in-memory repositories and direct mock synchronization when `MOCK_MODE=True`. Data resets on redeploy/restart. Render cannot reach biometric devices on a private company LAN. A real-device deployment must run inside the company network or through an approved VPN/private networking solution.

### Netlify

The included `netlify.toml` builds `frontend/` and enables SPA fallback routing. Configure:

```text
VITE_API_URL=https://your-api.onrender.com
```

The browser must be able to reach the Render API over HTTPS and its WebSocket endpoint over WSS.

## Release readiness

The current `main` branch contains the three implemented phases:

- `phase-1-baseline`: hexagonal device ports and demo adapter.
- `phase-2-persistence`: Alembic, idempotent batch persistence, Celery, Redis and MySQL Compose.
- `phase-3-final`: WebSockets, React reconnection, deployment configuration and documentation.

Before making the public demo live, configure only `MOCK_MODE=True`, `CORS_ORIGINS` in Render and `VITE_API_URL` in Netlify. Do not commit `.env` or production credentials. For a persistent production release later, add managed MySQL/Redis and enable the Celery Worker/Beat services. Releasing this demo from `main` is the correct path.
