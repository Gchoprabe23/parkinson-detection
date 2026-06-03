# Parkinson's Disease Detection AI

🧠 An AI-powered system for early detection of Parkinson's disease using spiral drawing analysis.

## 🎯 Features

- ✅ **VGG16 Deep Learning Model** - Pre-trained neural network for accurate detection
- ✅ **Secure Authentication** - JWT-based login with password hashing
- ✅ **Guest Mode** - Test predictions without account creation
- ✅ **Doctor Dashboard** - Patient records and prediction history
- ✅ **Admin Dashboard** - System statistics and monitoring
- ✅ **REST API** - Fast and secure backend API
- ✅ **Responsive UI** - Built with Streamlit for easy access
- ✅ **Production Ready** - Docker support and deployment guides

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│     Streamlit Frontend (Port 8501)      │
│  - User authentication                  │
│  - Image upload & prediction            │
│  - Doctor & Admin dashboards            │
└────────────────┬────────────────────────┘
                 │ REST API
                 ▼
┌─────────────────────────────────────────┐
│     FastAPI Backend (Port 8000)         │
│  - Prediction engine                    │
│  - JWT authentication                   │
│  - Database management                  │
└────────────────┬────────────────────────┘
                 │ SQLAlchemy
                 ▼
         ┌───────────────────┐
         │   SQLite/        │
         │   PostgreSQL DB  │
         └───────────────────┘
                 │ TensorFlow
                 ▼
        ┌─────────────────────┐
        │  VGG16 ML Model     │
        │  (parkinsons_       │
        │   detector.keras)   │
        └─────────────────────┘
```

## 📊 Model Performance

- **Accuracy:** ~94%
- **Precision:** 93%
- **Recall:** 94%
- **F1-Score:** 0.93

*Training on 204 samples with 80/20 train-test split*

## 🚀 Quick Start

### Option 1: Docker (Recommended)
```bash
docker-compose up
```

### Option 2: Local Setup
```bash
# Windows
.\deploy.bat

# Linux/Mac
bash deploy.sh
```

### Default Credentials
- Username: `admin`
- Password: `admin123`

📖 **Full deployment guide:** See [DEPLOYMENT.md](DEPLOYMENT.md)

## 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Model** | TensorFlow/Keras, VGG16 |
| **Backend** | FastAPI, Python 3.10 |
| **Frontend** | Streamlit |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) |
| **Authentication** | JWT, bcrypt |
| **Deployment** | Docker, Docker Compose |

## 📁 Project Structure

```
Parkinson-Project-main/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── database.py          # Database connection
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── app.py               # Streamlit application
│   └── requirements.txt
├── model/
│   ├── main.py              # Model training script
│   └── parkinsons_detector.keras  # Trained model
├── dataset/
│   ├── train/               # Training images
│   └── test/                # Test images
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── deploy.sh / deploy.bat
└── DEPLOYMENT.md
```

## 🎮 Usage

### 1. Login/Register
- Create an account or use guest mode
- All features available with/without login

### 2. Upload Spiral Image
- Use high-quality image of spiral drawing
- Supports JPG, PNG formats

### 3. Get Prediction
- Model analyzes image
- Shows prediction: Healthy/Parkinson
- Displays confidence percentage

### 4. View History (Authenticated Users)
- Access prediction records
- Export data if needed

## 🔐 Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token-based authentication
- ✅ CORS protection
- ✅ SQL injection prevention with SQLAlchemy
- ✅ Environment variable secrets management
- ✅ Optional authentication for predictions

## 📈 API Endpoints

### Public
- `POST /register` - Register user
- `POST /token` - Login
- `POST /predict` - Make prediction
- `GET /health` - Health check

### Authenticated
- `GET /history` - User predictions

### Admin
- `GET /admin/stats` - System statistics

Full API docs: http://localhost:8000/docs

## 🧪 Testing

```bash
# Backend test
curl http://localhost:8000/health

# Create admin user
python create_admin.py admin_user strong_password

# Train model
python model/main.py
```

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Model not found | Check `model/parkinsons_detector.keras` exists |
| Connection refused | Ensure backend running on port 8000 |
| Database error | Delete `parkinsons.db` and restart |
| CORS error | Update `allow_origins` in `backend/main.py` |

## 📚 Documentation

- [Deployment Guide](DEPLOYMENT.md)
- [API Documentation](http://localhost:8000/docs)
- [Model Training](model/main.py)

## 🎓 Educational Purpose

This project is designed for educational purposes to demonstrate:
- Deep learning with TensorFlow/Keras
- FastAPI backend development
- Streamlit frontend creation
- Authentication and security
- Docker containerization
- Full-stack machine learning deployment

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💻 Author

Developed as a final year project for educational purposes.

## 🙏 Acknowledgments

- TensorFlow and Keras communities
- Streamlit framework
- FastAPI documentation

---

**Status:** ✅ Production Ready  
**Version:** 1.0.0  
**Last Updated:** June 2026  

For questions or support, please open an issue on GitHub.
