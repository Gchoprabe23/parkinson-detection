# 🚀 Complete Streamlit Deployment Guide

> This guide covers deploying your Parkinson's Detection AI system with Streamlit frontend and FastAPI backend.

---

## 📋 Prerequisites Checklist

Before you start, ensure you have:

- ✅ Python 3.9+ installed
- ✅ Git installed
- ✅ Model trained: `model/parkinsons_detector.keras` exists
- ✅ Virtual environment ready (see below)
- ✅ Internet connection for package downloads

---

## 🔧 STEP 1: Prepare Your Environment

### Option A: Create New Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### Option B: Use Existing Virtual Environment

If you see `venv/` folder already exists:
```bash
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

**Verify activation:** You should see `(venv)` at the start of your terminal prompt.

---

## 🤖 STEP 2: Train the Model (CRITICAL!)

**If you haven't trained the model yet, do this FIRST:**

```bash
cd model
python main.py
```

⏱️ **Expected time:** 5-15 minutes depending on dataset size

✅ **Success indicators:**
- See "Training Loss and Accuracy" graph
- Final message: `[SUCCESS] Training complete!`
- File created: `model/parkinsons_detector.keras`

❌ **If training fails:**
- Verify dataset structure: `dataset/train/{healthy,parkinson}/` and `dataset/test/{healthy,parkinson}/`
- Ensure images are .jpg or .png format
- Check for corrupt image files

---

## 📦 STEP 3: Install Dependencies

Still with `(venv)` activated:

```bash
# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies  
pip install -r frontend/requirements.txt

# Install model training dependencies (if not already)
pip install -r model/requirements.txt 2>/dev/null || echo "Already installed"
```

⏱️ **Expected time:** 2-5 minutes

✅ **Verify installation:**
```bash
pip list | grep -E "streamlit|fastapi|tensorflow"
```

---

## 🗄️ STEP 4: Configure Environment

### Create `.env` file (if it doesn't exist)

```bash
# Copy from template
cp .env.example .env
```

### Edit `.env` with your settings

```env
# Security - CHANGE THESE IN PRODUCTION!
SECRET_KEY=your_super_secret_key_change_this_in_production
ALGORITHM=HS256

# Database - Default is SQLite for local, use PostgreSQL for production
DATABASE_URL=sqlite:///./parkinsons.db

# Backend Configuration
BACKEND_URL=http://localhost:8000

# Model Path
MODEL_PATH=model/parkinsons_detector.keras

# Frontend Configuration  
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=false
```

---

## 👤 STEP 5: Create Admin Account

```bash
python create_admin.py
```

**Follow the prompts:**
```
Enter admin username: admin
Enter admin password: admin123
```

✅ **Success message:** `Admin user created successfully`

**Default credentials:**
- Username: `admin`
- Password: `admin123`

⚠️ **IMPORTANT:** Change this password after first login!

---

## 🚀 STEP 6: Start the Backend (Terminal 1)

Keep `(venv)` activated in this terminal:

```bash
uvicorn backend.main:app --reload --port 8000
```

✅ **Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
[INFO] Model loaded successfully from model/parkinsons_detector.keras
```

❌ **If model fails to load:**
- Verify `parkinsons_detector.keras` exists in project root
- Check model file size (>100MB typical)
- Re-train the model

✅ **Verify API is working:**
```bash
# In a new terminal (keep backend running):
curl http://localhost:8000/health
```

Expected response: `{"status":"ok","model_loaded":true}`

---

## 🎨 STEP 7: Start Streamlit Frontend (Terminal 2)

Open a **NEW terminal** with `(venv)` activated:

```bash
streamlit run frontend/app.py
```

✅ **Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

A browser window should open automatically. If not, manually visit: **http://localhost:8501**

---

## ✅ STEP 8: Test the Application

### Test 1: Guest Prediction
1. Go to Frontend (http://localhost:8501)
2. Click "👤 Guest Mode" tab
3. Upload a spiral test image
4. Click "🚀 Analyze Image"
5. ✅ Verify you see:
   - Prediction result (Healthy or Parkinson)
   - Confidence percentage (should be >80% if model trained well)
   - **Detailed Analysis** with both class probabilities

### Test 2: User Registration & Login
1. Click "📝 Register" tab
2. Create test account (e.g., `testdoctor` / `password123`)
3. Click "🔐 Login" tab
4. Login with your test account
5. Upload image and verify prediction saves to history

### Test 3: Admin Dashboard
1. Login as `admin` (default credentials)
2. Should redirect to Admin Panel
3. Verify system stats display

### Test 4: Check API Documentation
1. Visit http://localhost:8000/docs
2. Should see interactive API documentation
3. Try `/health` endpoint to verify model is loaded

---

## 🐳 STEP 9: Optional - Docker Deployment

If you want to run everything in containers:

```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

✅ Access:
- Frontend: http://localhost:8501
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🌐 STEP 10: Deploy to Streamlit Cloud (Optional)

### Prerequisites:
- GitHub repository (push your project)
- Streamlit account (free at streamlit.io)

### Deploy:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Parkinson Detection AI deployment"
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Sign up / Log in with GitHub
   - Click "New app"
   - Select repository, branch, and file (`frontend/app.py`)

3. **Configure Secrets** (in Streamlit Cloud dashboard)
   ```toml
   # Click "Advanced settings" → "Secrets"
   SECRET_KEY = "your_secret_key"
   DATABASE_URL = "sqlite:///./parkinsons.db"
   BACKEND_URL = "https://your-backend-url.com"
   ```

4. **Deploy!**
   - Click "Deploy"
   - Wait 2-3 minutes for build
   - Your app is now live!

---

## 🚨 Troubleshooting

### Issue: "Model not found" error

**Solution:**
```bash
cd model
python main.py  # Re-train the model
```

### Issue: Port 8000/8501 already in use

**Solution (Windows):**
```bash
# Find process using port
netstat -ano | findstr :8000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F
```

**Solution (Linux/Mac):**
```bash
# Find and kill
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Issue: "Can't connect to backend"

**Check:**
1. Is backend running? (Terminal should show running message)
2. Is port 8000 correct? (Check `.env` BACKEND_URL)
3. Network firewall blocking connections?

### Issue: Very low confidence scores (<60%)

**This means model not trained properly:**
```bash
# Re-train model
cd model
python main.py
```

**Check accuracy during training:**
- Look for "Accuracy: 0.XX" in output
- Should be >75% for good model
- If <70%, dataset might be too small/unbalanced

### Issue: Predictions not saving to database

**Check:**
- Are you logged in? (Guest mode doesn't save)
- Is admin user created? (`python create_admin.py`)
- Is database file writable? (Check `parkinsons.db` permissions)

---

## 📊 Expected Results After Deployment

### ✅ Good Setup:
```
✓ Backend running on http://localhost:8000
✓ Frontend running on http://localhost:8501
✓ Model loaded successfully
✓ Can upload image and get prediction
✓ Confidence score >80% on valid test images
✓ Both class probabilities displayed
✓ Predictions save to history (when logged in)
```

### UI Should Show:
- **Guest Mode:** Quick predictions without login
- **Doctor Dashboard:** Diagnosis tab, History tab, Stats tab
- **Admin Dashboard:** System statistics
- **Detailed Analysis:** Both "Healthy Confidence %" and "Parkinson Confidence %"

---

## 🔒 Production Checklist

Before going live, ensure:

- ✅ Change `SECRET_KEY` in `.env` to random secure key
- ✅ Use PostgreSQL instead of SQLite (set `DATABASE_URL`)
- ✅ Update `BACKEND_URL` to your production domain
- ✅ Set `STREAMLIT_SERVER_HEADLESS=true` for servers
- ✅ Enable HTTPS/SSL certificates
- ✅ Set up CORS properly (don't use `["*"]` in production)
- ✅ Enable logging and monitoring
- ✅ Regular database backups
- ✅ Test all authentication flows
- ✅ Verify model performance on real data

---

## 📝 Quick Reference Commands

```bash
# Activate environment
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Train model (from project root)
cd model && python main.py

# Start backend (Terminal 1)
uvicorn backend.main:app --reload --port 8000

# Start frontend (Terminal 2)  
streamlit run frontend/app.py

# Create admin
python create_admin.py

# Docker start
docker-compose up -d

# Check health
curl http://localhost:8000/health

# View API docs
# Browser: http://localhost:8000/docs
```

---

## 📚 Additional Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Streamlit Docs:** https://docs.streamlit.io/
- **Deployment Guide:** See `DEPLOYMENT.md`
- **Fixes Applied:** See `FIXES_APPLIED.md` (confidence score improvements)
- **Architecture Overview:** See `README_DEPLOYMENT.md`

---

## ✨ Next Steps

1. ✅ Complete steps 1-7 above
2. ✅ Test the application (Step 8)
3. ✅ Deploy to Streamlit Cloud (Step 10) - Optional
4. 📊 Monitor predictions and collect real data
5. 🔄 Periodically re-train model with new data
6. 📈 Analyze metrics to improve accuracy

---

**Need Help?** Check the troubleshooting section or refer to `DEPLOYMENT.md` for more details.
