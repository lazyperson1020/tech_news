@echo off
REM Colors and styles for Windows (basic support)
setlocal enabledelayedexpansion

echo.
echo Setting up The Silicon Post...
echo.

REM Backend setup
echo Setting up Backend...
cd backend

if not exist "venv" (
  echo Creating virtual environment...
  python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Creating .env file from example...
if not exist ".env" (
  copy .env.example .env
  echo Please update .env with your configuration
)

echo Running migrations...
python manage.py migrate

echo Backend setup complete!
echo Backend is ready at: http://localhost:8000

REM Frontend setup
echo.
echo Setting up Frontend...
cd ..\frontend

echo Installing dependencies...
call npm install

echo Frontend setup complete!
echo Frontend will be available at: http://localhost:5173

REM Final instructions
echo.
echo ========================
echo Setup Complete!
echo ========================
echo.
echo To start the development servers:
echo.
echo Terminal 1 - Backend:
echo cd backend && venv\Scripts\activate && python manage.py runserver
echo.
echo Terminal 2 - Frontend:
echo cd frontend && npm run dev
echo.
echo Admin panel: http://localhost:8000/admin
echo Frontend: http://localhost:5173
