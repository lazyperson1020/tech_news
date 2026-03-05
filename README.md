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

Backend test and lint commands (run from the project root):

 - Install backend dev dependencies:

```bash
cd backend
pip install -r requirements.txt
```

 - Run tests with coverage:

```bash
cd backend
pytest
```

 - Run flake8 linting:

```bash
cd backend
flake8 .
```

The repository includes `backend/pytest.ini`, `backend/.coveragerc`, and `backend/.flake8` for default pytest/coverage/flake8 behavior.

