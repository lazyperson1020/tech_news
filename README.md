<p align="center">
  <img src="docs/logo.png" alt="Project Logo" width="300" style="background: lightblue; border-radius: 15px">
</p>
Welcome to the Tech News project! This repository is designed to help you stay updated with the latest technology news and trends. It provides a simple way to fetch, filter, and display news articles from various sources.



## Features

- User registration and authentication
- Article management with categories
- News aggregation from multiple sources
- AI-powered article summarization
- Bookmarking and commenting system
- Responsive React frontend with Tailwind CSS
- Django REST API backend

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Frontend**: React 19, React Router, Tailwind CSS
- **Database**: SQLite (development) / PostgreSQL (production)
- **AI**: OpenAI API for summarization


## Tests & Linting

The project now includes additional test files. Backend tests are in `tests/backend/`, and frontend tests are in `frontend/__tests__/`.

### Backend

Install backend dev dependencies and run Django tests with coverage:

```bash
cd backend
pip install -r requirements.txt
pytest  # will pick up tests both inside backend/ and ../tests/backend/, including auth, articles, bookmarks, preferences etc.
```

Lint with flake8:

```bash
cd backend
flake8 .
```

Configuration files are available in `backend/pytest.ini`, `backend/.coveragerc`, and `backend/.flake8`.

### Frontend

Install frontend dependencies and run Vitest (ensure test deps are installed):

```bash
cd frontend
npm install
# if you added testing dependencies, they include jsdom
npm run test
```

Vitest will execute tests under `frontend/__tests__/` and provide coverage reports when configured.
Test files are located alongside the source code for easy discovery.


## Continuous Integration

A GitHub Actions workflow is included at `.github/workflows/ci.yml`. On every push or pull request against `main` it will:

1. Install backend Python requirements and run the pytest suite (using SQLite).
2. Install frontend Node packages and execute Vitest.
3. Optionally, run linters for Python and JS.

You can customize the workflow to add building containers, deploying, or using a real database.

## Docker

A `Dockerfile` is provided for each service (backend and frontend) along with a `docker-compose.yml` at the repo root.

To build and run all components:

```bash
# from repository root
docker-compose up --build
```

- Backend available at http://localhost:8000 (uses the `.env` file under `backend/` for configuration)
- Frontend available at http://localhost:3000

You can also run management commands in the backend container:

```bash
docker-compose run --rm backend python manage.py migrate
```

Adjust any environment values before launching if needed.

