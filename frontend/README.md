# M. abscessus Tolerance Platform — Frontend

React + TypeScript frontend for the M. abscessus antibiotic tolerance research platform.

## Tech Stack

- **React 18** with TypeScript
- **React Router v6** for client-side routing
- **Axios** for API communication
- **Recharts** for data visualisation (survival curves, heatmaps, scatter plots)
- **React Dropzone** for drag-and-drop file uploads
- **Tailwind CSS** for styling
- **Headless UI** for accessible UI primitives

## Development

```bash
# Install dependencies
npm install

# Start development server (proxies /api to backend)
npm start

# Build for production
npm run build
```

Set `REACT_APP_API_URL` to override the default API base (`/api/v1`).

## Docker

```bash
docker build -t abscessus-frontend .
docker run -p 3000:80 abscessus-frontend
```

The nginx image proxies `/api` to the `backend` service. When using docker-compose, ensure the backend service is named `backend`.

## Routes

| Path | Description |
|------|-------------|
| `/login` | Login page |
| `/register` | Registration page |
| `/dashboard` | Dashboard (protected) |
| `/experiments` | Experiment list (protected) |
| `/experiments/:id` | Experiment detail (protected) |
| `/upload` | File upload (protected) |
| `/analysis` | Analysis (protected) |
| `/visualization/:id` | Visualisation (protected) |
