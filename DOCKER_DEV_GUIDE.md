# Docker Development Guide

This guide walks you through setting up and running the M. abscessus Tolerance Platform using Docker for local development.

## 📋 Prerequisites

Before you start, make sure you have installed:

- **Docker** (v24.0+) - [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (v2.20+) - Usually included with Docker Desktop
- **Git** - For cloning the repository

### Verify Installation

```bash
docker --version
docker compose version
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/spartan124/m-abscessus-tolerance-platform.git
cd m-abscessus-tolerance-platform
```

### 2. Create Environment File

```bash
cp .env.example .env
```

**Default credentials for development:**
- PostgreSQL: `postgres` / `postgres123`
- MongoDB: `mongoadmin` / `mongo123`
- Backend Secret: Auto-generated (change in production)

### 3. Start All Services

```bash
# Build and start all services in the background
docker compose up -d

# Verify all services are running
docker compose ps
```

### 4. Access the Application

Once all services are healthy (~30-60 seconds):

- **Frontend**: http://localhost:80 or http://localhost
- **Backend API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 5. View Logs

```bash
# View logs from all services
docker compose logs -f

# View logs from a specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres
docker compose logs -f mongodb
```

## 🛑 Stop Services

```bash
# Stop all services (containers remain)
docker compose stop

# Remove all containers and networks
docker compose down

# Remove everything including volumes (⚠️ deletes data!)
docker compose down -v
```

## 📝 Service Architecture

```
┌─────────────────────────────────────────────┐
│           Docker Compose Network            │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │      NGINX (Port 80, 443)            │  │
│  │      - Routes traffic                │  │
│  │      - Serves static files           │  │
│  └──────────────────────────────────────┘  │
│           ↓              ↓                  │
│  ┌──────────────┐  ┌──────────────┐        │
│  │   Frontend   │  │   Backend    │        │
│  │  (React)     │  │  (FastAPI)   │        │
│  │  Port: 3000  │  │  Port: 8000  │        │
│  └──────────────┘  └──────────────┘        │
│           ↓              ↓                  │
│  ┌────────────────────────────────────┐   │
│  │      PostgreSQL + MongoDB          │   │
│  │  - postgres:5432                   │   │
│  │  - mongodb:27017                   │   │
│  └────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

## 🔧 Common Development Tasks

### Run Database Migrations

If you have Alembic migrations configured:

```bash
# Run migrations in the backend container
docker compose exec backend alembic upgrade head
```

### Access Backend Container Shell

```bash
docker compose exec backend bash
# Inside container, you can run Python commands
python -c "from app.main import app; print('App loaded')"
```

### Access Frontend Container Shell

```bash
docker compose exec frontend sh
# Inside container
npm list
```

### Access PostgreSQL CLI

```bash
docker compose exec postgres psql -U postgres -d mabscessus_db
# Common commands:
# \dt          - List tables
# \d users     - Describe 'users' table
# SELECT * FROM users;
# \q           - Quit
```

### Access MongoDB CLI

```bash
docker compose exec mongodb mongosh -u mongoadmin -p mongo123 --authenticationDatabase admin

# Common commands:
use mabscessus_mongo
db.collections.find()
exit
```

### View Database Data Volumes

```bash
# List all volumes
docker volume ls

# Inspect a volume
docker volume inspect m-abscessus-tolerance-platform_postgres_data
```

### Run Backend Tests

```bash
docker compose exec backend pytest tests/ -v --cov=app
```

### Rebuild a Specific Service

```bash
# Rebuild backend without cache
docker compose build --no-cache backend

# Rebuild frontend
docker compose build --no-cache frontend

# Rebuild all
docker compose build --no-cache
```

## 🐛 Troubleshooting

### Services Not Starting

```bash
# Check service health status
docker compose ps

# View full logs
docker compose logs

# Check specific service
docker compose logs backend
```

### Port Already in Use

If you get "port 80 already in use" or similar:

```bash
# Find what's using the port (on Linux/Mac)
lsof -i :80

# Change port in docker-compose.yml
# Change: ports: ["80:80"] to ports: ["8080:80"]
```

### Database Connection Issues

```bash
# Verify database is healthy
docker compose ps

# Check PostgreSQL logs
docker compose logs postgres

# Test connection from backend
docker compose exec backend ping postgres
```

### Frontend Not Loading

```bash
# Clear frontend build and restart
docker compose down frontend
docker compose build --no-cache frontend
docker compose up -d frontend
```

### Out of Disk Space

```bash
# Clean up unused Docker resources
docker system prune -a

# Remove all volumes (⚠️ DELETES DATA!)
docker volume prune
```

## 🔒 Security Notes for Development

### Default Credentials

The `.env.example` contains default credentials for **development only**. 

**For production, you must:**

1. Change `POSTGRES_PASSWORD` to a strong password
2. Change `MONGODB_PASSWORD` to a strong password
3. Generate a secure `SECRET_KEY`:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
4. Update `ALLOWED_ORIGINS` to your production domain
5. Set `DEBUG=False` in the backend
6. Use environment-specific `.env` files (don't commit to Git)

### Storing Secrets

- Create a `.env.local` file (gitignored) for sensitive data
- Use Docker secrets for production deployments
- Never commit credentials to the repository

## 📊 Monitoring and Performance

### Check Service Resource Usage

```bash
# Monitor Docker resources in real-time
docker stats

# Exit with Ctrl+C
```

### Cleanup Old Images and Containers

```bash
# Remove unused images
docker image prune -a

# Remove stopped containers
docker container prune
```

## 🔄 Updating Dependencies

### Backend (Python)

```bash
# Update requirements.txt
# Then rebuild:
docker compose build --no-cache backend
docker compose up -d backend
```

### Frontend (Node)

```bash
# Update package.json
# Then rebuild:
docker compose build --no-cache frontend
docker compose up -d frontend
```

## 📚 Docker Compose File Reference

**Service Descriptions:**

| Service | Purpose | Port | Notes |
|---------|---------|------|-------|
| `nginx` | Reverse proxy & static serving | 80, 443 | Routes traffic |
| `frontend` | React application | 3000 (internal) | Built with multi-stage build |
| `backend` | FastAPI server | 8000 (internal) | Depends on databases |
| `postgres` | PostgreSQL database | 5432 (internal) | Volume: `postgres_data` |
| `mongodb` | MongoDB database | 27017 (internal) | Volume: `mongo_data` |

**Volumes:**

- `postgres_data` - PostgreSQL data persistence
- `mongo_data` - MongoDB data persistence
- `uploads_data` - File uploads directory

**Networks:**

- `app-network` - Internal bridge network for service communication

## 🎯 Development Workflow

### For Backend Changes

```bash
# 1. Make code changes in backend/
# 2. Rebuild backend service
docker compose build backend

# 3. Restart backend service
docker compose up -d backend

# 4. Check logs
docker compose logs -f backend
```

### For Frontend Changes

```bash
# 1. Make code changes in frontend/
# 2. Rebuild frontend service
docker compose build frontend

# 3. Restart frontend service
docker compose up -d frontend

# 4. Check browser (usually auto-refreshes)
```

### Running Specific Tests

```bash
# Backend unit tests
docker compose exec backend pytest tests/unit -v

# Backend integration tests
docker compose exec backend pytest tests/integration -v

# Backend with coverage
docker compose exec backend pytest --cov=app tests/
```

## 📖 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [MongoDB Docker Image](https://hub.docker.com/_/mongo)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

## 💡 Tips & Tricks

### One-liner to Reset Everything

```bash
docker compose down -v && docker compose up -d && docker compose logs -f
```

### Watch Real-time Logs from Multiple Services

```bash
docker compose logs -f backend frontend postgres mongodb
```

### Execute Python Code in Backend

```bash
docker compose exec backend python -c "import app; print('App imported successfully')"
```

### Copy Files Between Host and Container

```bash
# Copy from host to container
docker compose cp ./local-file backend:/app/path/

# Copy from container to host
docker compose cp backend:/app/path/file ./local-file
```

## 🆘 Need Help?

For issues or questions:

1. Check the [main README](./README.md)
2. Review [backend README](./backend/README.md)
3. Review [frontend README](./frontend/README.md)
4. Check logs: `docker compose logs service-name`
5. Open a [GitHub Issue](https://github.com/spartan124/m-abscessus-tolerance-platform/issues)

---

**Happy developing with Docker! 🐳**
