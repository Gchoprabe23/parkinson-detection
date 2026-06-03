# Parkinson's Disease Detection AI - Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git
- Docker (optional)

### Local Development Setup

#### Windows:
```bash
# Run deployment script
.\deploy.bat
```

#### Linux/Mac:
```bash
# Run deployment script
bash deploy.sh
```

### Manual Setup

1. **Create Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   pip install -r frontend/requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Initialize database and create admin**
   ```bash
   python create_admin.py
   ```

5. **Run backend server** (Terminal 1)
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

6. **Run frontend** (Terminal 2)
   ```bash
   streamlit run frontend/app.py
   ```

7. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)
```bash
docker-compose up -d
```

This will start:
- Backend on http://localhost:8000
- Frontend on http://localhost:8501

### Using Docker Only

**Build:**
```bash
docker build -t parkinsons-ai .
```

**Run:**
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./parkinsons.db \
  -e SECRET_KEY=your_secret_key \
  parkinsons-ai
```

---

## 🔐 Login Credentials

**Default Admin Account:**
- Username: `admin`
- Password: `admin123`

⚠️ **IMPORTANT:** Change the password after first login in production!

---

## 📋 Configuration

Edit `.env` file to customize:

```env
SECRET_KEY=your_super_secret_key_change_this_in_production
DATABASE_URL=sqlite:///./parkinsons.db
BACKEND_URL=http://localhost:8000
MODEL_PATH=model/parkinsons_detector.keras
```

---

## 🌐 Deployment to Production

### Using Render (Recommended)

1. **Push to GitHub**
2. **Create new Web Service on Render**
3. **Connect to repository**
4. **Set environment variables**
5. **Deploy**

### Using Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add buildpack
heroku buildpacks:add heroku/python

# Push
git push heroku main

# View logs
heroku logs --tail
```

### Using AWS/Azure/GCP

Refer to platform-specific deployment guides.

---

## 🧪 Testing

### Test Backend
```bash
# Check health endpoint
curl http://localhost:8000/health

# View API documentation
# Open: http://localhost:8000/docs
```

### Create Test Admin
```bash
python create_admin.py custom_admin secure_password_123
```

---

## 📊 Model Training

To retrain the model with new data:

```bash
python model/main.py
```

The trained model will be saved to `model/parkinsons_detector.keras`

---

## 🛠️ API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /token` - Login (returns JWT token)

### Predictions (Authenticated & Guest)
- `POST /predict` - Make prediction on image
- `GET /health` - Check system health

### Doctor Routes (Authenticated)
- `GET /history` - Get user's prediction history

### Admin Routes (Admin only)
- `GET /admin/stats` - Get system statistics

---

## 🐛 Troubleshooting

### Model not loading
```
Error: [ERROR] Could not load model
```
- Ensure `model/parkinsons_detector.keras` exists
- Check file path in `.env`

### Database errors
```
Error: database disk image is malformed
```
- Delete `parkinsons.db` and restart
- Or use PostgreSQL in production

### Connection refused
```
Error: Cannot connect to server
```
- Ensure backend is running on correct port
- Check `BACKEND_URL` in `.env`

### CORS errors
- Update `allow_origins` in `backend/main.py`
- Example: `allow_origins=["https://yourdomain.com"]`

---

## 📚 Documentation

- **API Docs:** http://localhost:8000/docs (Swagger UI)
- **ReDoc:** http://localhost:8000/redoc
- **Code:** See inline comments in source files

---

## 🚀 Performance Tips

1. **Enable caching** for predictions
2. **Use PostgreSQL** instead of SQLite in production
3. **Deploy with Gunicorn** instead of Uvicorn
4. **Use CDN** for frontend assets
5. **Enable HTTPS/SSL** for all connections

---

## 📝 License

See LICENSE file for details.

---

## 👥 Support

For issues, create a GitHub issue or contact the development team.

---

**Version:** 1.0.0
**Last Updated:** June 2026
