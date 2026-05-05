# Contributing to M. abscessus Tolerance Platform

Thank you for your interest in contributing! This document explains how to get
involved and the standards we follow.

## Code of Conduct

Be respectful and constructive. We follow the [Contributor Covenant](https://www.contributor-covenant.org/).

## Getting Started

1. **Fork** the repository and clone your fork.
2. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Set up your local environment (see [README.md](README.md)).
4. Make your changes with clear, focused commits.
5. Run the test suite before submitting:
   ```bash
   cd backend && pytest
   ```
6. Open a **Pull Request** against `main` with a clear description.

## Development Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit as needed
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local   # optional
npm start
```

### Docker (full stack)

```bash
cp .env.example .env   # edit secrets
docker compose up --build
```

## Pull Request Guidelines

- Keep PRs small and focused on a single concern.
- Write or update tests for any changed behaviour.
- Ensure `pytest` passes and there are no linting errors.
- Update documentation (README, docstrings) where relevant.
- Reference any related issues in the PR description.

## Coding Style

### Python (backend)
- Follow [PEP 8](https://peps.python.org/pep-0008/).
- Use type annotations.
- Format with `black` and lint with `ruff`.

### TypeScript (frontend)
- Use functional components and hooks.
- Prefer explicit types over `any`.
- Format with `prettier`.

## Reporting Bugs

Open a GitHub issue with:
- A clear title and description.
- Steps to reproduce.
- Expected vs. actual behaviour.
- Environment details (OS, Python/Node version).

## Feature Requests

Open a GitHub issue tagged `enhancement` with a description of the feature
and its motivation.
