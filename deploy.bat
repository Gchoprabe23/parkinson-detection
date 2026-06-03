@echo off
REM deploy.bat - Deployment script for Windows

echo 🚀 Starting Parkinson's Disease Detection AI Deployment...

REM Create .env from .env.example if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from .env.example...
    copy .env.example .env
    echo ⚠️  Please update .env with your configuration!
)

REM Create virtual environment
echo 🔧 Setting up Python virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
pip install -r frontend\requirements.txt

REM Initialize database
echo 🗄️  Initializing database...
python create_admin.py

echo ✅ Deployment setup complete!
echo.
echo 📋 Next steps:
echo 1. Update .env file with your configuration
echo 2. Run the backend:   uvicorn backend.main:app --reload --port 8000
echo 3. Run the frontend:  streamlit run frontend/app.py
