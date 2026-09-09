# Biometric Attendance Platform — Frontend

React + Vite administration dashboard for the biometric attendance platform.

## Configuration

Create `frontend/.env` for local development:

```env
VITE_API_URL=http://localhost:8000
```

For Netlify, set the same variable to the deployed Render API:

```env
VITE_API_URL=https://your-api.onrender.com
```

The frontend uses the REST API for devices and attendance, and connects to:

```text
wss://your-api.onrender.com/ws/devices
```

The device dashboard reconnects automatically and updates device status events without a page reload.

## Local development

```powershell
npm install
npm run dev
```

Available at `http://localhost:5173`.

## Production build

```powershell
npm ci
npm run lint
npm run build
```

Netlify is configured through the repository-level `netlify.toml`. It builds the `frontend` directory and enables SPA fallback routing.

User-facing labels remain in Spanish for the portfolio audience. Component names, hooks, variables and API code are maintained in English.
