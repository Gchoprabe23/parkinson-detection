#!/bin/bash
# deploy.sh - Deployment script

echo "🚀 Starting Parkinson's Disease Detection AI Deployment..."

# Create .env from .env.example if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration!"
fi

# Create virtual environment
echo "🔧 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# Initialize database
echo "🗄️  Initializing database..."
python create_admin.py

echo "✅ Deployment setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Update .env file with your configuration"
echo "2. Run the backend:   uvicorn backend.main:app --reload --port 8000"
echo "3. Run the frontend:  streamlit run frontend/app.py"
