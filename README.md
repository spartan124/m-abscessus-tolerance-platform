# M. abscessus Tolerance Platform

A full-stack research platform for studying antibiotic tolerance mechanisms in *Mycobacterium abscessus*. This repository combines a FastAPI backend with a React TypeScript frontend to provide tools for data analysis, visualization, and collaborative research.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation with UV](#installation-with-uv)
  - [Installation with Pip (Legacy)](#installation-with-pip-legacy)
- [Project Structure](#project-structure)
- [Development](#development)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 📖 Project Overview

The M. abscessus Tolerance Platform is designed to facilitate research into antibiotic tolerance mechanisms. It provides:

- **Data Management**: Upload and manage experimental datasets
- **Analysis Tools**: Perform statistical and computational analysis
- **Visualization**: Interactive charts and heatmaps for results
- **Collaboration**: Secure authentication and user management

**Language Composition:**
- Python (57.4%) - Backend API
- TypeScript (39.4%) - Frontend
- CSS, Dockerfile, HTML, Shell, JavaScript (3.2%) - Supporting technologies

## 🛠 Tech Stack

### Backend
- **Python 3.11+** with FastAPI
- **PostgreSQL 13+** for relational data
- **MongoDB 6+** for document storage
- **SQLAlchemy** for ORM
- **Motor** for async MongoDB
- **Pytest** for testing

### Frontend
- **React 18** with TypeScript
- **React Router v6** for navigation
- **Axios** for HTTP requests
- **Tailwind CSS** for styling
- **Recharts** for data visualization
- **Headless UI** for accessible components

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:

- **Python 3.11** or higher (for backend)
- **Node.js 18+** (for frontend)
- **PostgreSQL 13+** (for database)
- **MongoDB 6+** (for document store)

### Installation with UV

**UV** is a faster, more efficient Python package manager. We recommend using it for development.

#### 1. Install UV

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (with PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip (if you have Python installed)
pip install uv
```

#### 2. Clone the Repository

```bash
git clone https://github.com/spartan124/m-abscessus-tolerance-platform.git
cd m-abscessus-tolerance-platform
```

#### 3. Backend Setup with UV

```bash
cd backend

# Create a virtual environment with UV
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies with UV
uv pip install -r requirements.txt

# Copy environment configuration
cp .env.example .env

# Edit .env with your database credentials
# PostgreSQL: postgresql://user:password@localhost/dbname
# MongoDB: mongodb://localhost:27017
nano .env  # or use your preferred editor

# Run migrations (if applicable)
# alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### 4. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

### Installation with Pip (Legacy)

If you prefer the traditional pip approach:

```bash
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies with pip
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
nano .env

# Start the backend
uvicorn app.main:app --reload
```

## 📁 Project Structure

```
m-abscessus-tolerance-platform/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── config.py          # Configuration from environment variables
│   │   ├── database.py        # PostgreSQL + MongoDB connections
│   │   ├── security.py        # JWT authentication & password hashing
│   │   ├── api/               # Route handlers (endpoints)
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── services/          # Business logic & data processing
│   │   ├── utils/             # Helper functions & utilities
│   │   └── middleware/        # Custom middleware (logging, CORS, etc.)
│   ├── tests/                 # Pytest test suite
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment variables template
│   └── README.md              # Backend-specific documentation
│
├── frontend/                  # React + TypeScript frontend
│   ├── src/
│   │   ├── components/        # Reusable React components
│   │   ├── pages/             # Page components (Dashboard, Analysis, etc.)
│   │   ├── services/          # API client services
│   │   ├── hooks/             # Custom React hooks
│   │   ├── styles/            # Tailwind CSS styles
│   │   ├── types/             # TypeScript type definitions
│   │   └── App.tsx            # Root component
│   ├── public/                # Static assets
│   ├── package.json           # Node dependencies
│   ├── tsconfig.json          # TypeScript configuration
│   └── README.md              # Frontend-specific documentation
│
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker build configuration
├── README.md                  # This file
├── LICENSE                    # MIT License
└── CONTRIBUTING.md            # Contribution guidelines
```

## 💻 Development

### Backend Setup

**Using UV (Recommended):**

```bash
cd backend
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env

# Start development server
uvicorn app.main:app --reload
```

**Key Environment Variables:**

```bash
DATABASE_URL=postgresql://user:password@localhost/abscessus_db
MONGODB_URL=mongodb://localhost:27017
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

**Available Scripts:**

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run lint` - Run ESLint

## 🏃 Running the Application

### Local Development (Both Services)

**Terminal 1 - Backend:**

```bash
cd backend
source .venv/bin/activate  # Activate UV virtual environment
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm start
```

Access the application at `http://localhost:3000`

### Docker Compose (All Services)

```bash
# Start all services (backend, frontend, PostgreSQL, MongoDB)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Services will be available at:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`

## 🧪 Testing

### Backend Tests

```bash
cd backend
source .venv/bin/activate

# Run all tests with coverage
pytest tests/ -v --cov=app

# Run specific test file
pytest tests/test_api.py -v

# Run with markers
pytest -m unit -v
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## 🐳 Docker Deployment

### Build Images

```bash
# Build frontend
docker build -t abscessus-frontend ./frontend

# Build backend
docker build -t abscessus-backend ./backend
```

### Run with Docker Compose

```bash
docker-compose up -d
```

**Services defined in docker-compose.yml:**
- `frontend` - React app on port 3000
- `backend` - FastAPI on port 8000
- `postgres` - PostgreSQL on port 5432
- `mongodb` - MongoDB on port 27017

### Environment Variables for Docker

Create a `.env` file in the project root:

```bash
POSTGRES_USER=abscessus
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=abscessus_db
MONGODB_URL=mongodb://mongodb:27017
SECRET_KEY=your-secret-key
DEBUG=False
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and commit (`git commit -m 'Add amazing feature'`)
4. Push to your branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:
- Code style and formatting
- Testing requirements
- Commit message conventions
- Pull request process

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For inquiries, bug reports, or feature requests:

- **GitHub Issues**: [Project Issues](https://github.com/spartan124/m-abscessus-tolerance-platform/issues)
- **GitHub Discussions**: [Project Discussions](https://github.com/spartan124/m-abscessus-tolerance-platform/discussions)
- **Author**: [@spartan124](https://github.com/spartan124)

## 🔗 Additional Resources

- [Backend Documentation](./backend/README.md)
- [Frontend Documentation](./frontend/README.md)
- [API Documentation](http://localhost:8000/docs) (when running locally)
- [Contributing Guidelines](./CONTRIBUTING.md)

---

**Happy coding! 🚀**
