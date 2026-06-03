# ⚡ Streamlit Deployment - Quick Action Checklist

> Follow these steps in order. Check off each step as you complete it.

---

## 🎯 Pre-Deployment (Do This First!)

### Phase 1: Model Training
- [ ] Navigate to model folder: `cd model`
- [ ] Run training: `python main.py`
- [ ] ⏰ Wait 5-15 minutes for training to complete
- [ ] ✅ Verify file created: `model/parkinsons_detector.keras` (check file size >100MB)
- [ ] ✅ Check output shows "Training complete!" message

**If training fails:**
- [ ] Check dataset exists: `dataset/train/healthy/` and `dataset/train/parkinson/`
- [ ] Verify images are .jpg or .png
- [ ] Check for corrupt/missing image files
- [ ] Run training again

---

### Phase 2: Environment Setup

**Terminal:**
```bash
# Create & activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# OR
source venv/bin/activate       # Mac/Linux
```

- [ ] See `(venv)` in terminal prompt

**Install dependencies:**
```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

- [ ] Wait for installation to complete
- [ ] No red error messages

**Configure environment:**
```bash
cp .env.example .env
```

- [ ] `.env` file created
- [ ] Edit `.env` if needed (optional for local testing)

---

### Phase 3: Database Setup

```bash
python create_admin.py
```

- [ ] When prompted, enter username: `admin`
- [ ] When prompted, enter password: `admin123`
- [ ] See success message: "Admin user created successfully"

---

## 🚀 Deployment (Start Here for Each Session)

### Phase 4: Start Backend (Terminal 1)

```bash
# Make sure (venv) is activated
uvicorn backend.main:app --reload --port 8000
```

**Wait for:**
- [ ] `[INFO] Uvicorn running on http://127.0.0.1:8000`
- [ ] `[INFO] Model loaded successfully from model/parkinsons_detector.keras`
- [ ] See `{"status":"ok","model_loaded":true}` when you visit http://localhost:8000/health

**If model fails to load:**
- [ ] Go back to Phase 1 and re-train model
- [ ] Verify `parkinsons_detector.keras` exists in project root
- [ ] Check file size is >100MB

---

### Phase 5: Start Frontend (Terminal 2)

**Open NEW terminal with venv activated:**
```bash
streamlit run frontend/app.py
```

**Wait for:**
- [ ] Browser opens automatically to http://localhost:8501
- [ ] Or manually open http://localhost:8501
- [ ] See Streamlit interface load

---

## ✅ Testing & Verification

### Phase 6: Verify Everything Works

#### Test 1: API Health Check
- [ ] Visit http://localhost:8000/health
- [ ] See response: `{"status":"ok","model_loaded":true}`

#### Test 2: Guest Prediction
- [ ] Go to http://localhost:8501
- [ ] Click "👤 Guest Mode" tab
- [ ] Upload a spiral test image
- [ ] Click "🚀 Analyze Image"
- [ ] See prediction result (Healthy or Parkinson)
- [ ] See confidence >80% (if model trained well)
- [ ] See "Detailed Analysis" with both confidences

#### Test 3: User Registration
- [ ] Click "📝 Register" tab
- [ ] Create test account: username=`testdoctor`, password=`test123`
- [ ] See success message

#### Test 4: Login & History
- [ ] Click "🔐 Login" tab
- [ ] Login with test account
- [ ] Upload image and analyze
- [ ] Click "📋 Prediction History" tab
- [ ] See prediction saved in history

#### Test 5: Admin Access
- [ ] Click "🔐 Login" tab
- [ ] Login as admin: username=`admin`, password=`admin123`
- [ ] Should see "Admin Panel" with system statistics
- [ ] See "Disease Distribution" chart

#### Test 6: API Documentation
- [ ] Visit http://localhost:8000/docs
- [ ] See Swagger UI with all endpoints
- [ ] Try "POST /predict" endpoint (optional)

---

## 🐳 Optional: Docker Deployment

If you want to run everything in containers:

```bash
docker-compose up -d
```

- [ ] Docker & Docker Compose installed
- [ ] Wait 2-3 minutes for containers to start
- [ ] Backend: http://localhost:8000
- [ ] Frontend: http://localhost:8501

**Stop containers:**
```bash
docker-compose down
```

---

## 🌐 Optional: Deploy to Streamlit Cloud

### Prerequisites:
- [ ] GitHub account
- [ ] Project pushed to GitHub repository
- [ ] Streamlit Cloud account (free at https://share.streamlit.io)

### Steps:
1. [ ] Go to https://share.streamlit.io
2. [ ] Click "New app"
3. [ ] Select your GitHub repository
4. [ ] Select branch: `main` (or your branch)
5. [ ] Select file: `frontend/app.py`
6. [ ] Click "Deploy"
7. [ ] Wait 2-3 minutes for deployment
8. [ ] Your app is live at `https://<app-name>.streamlit.app`

---

## 🚨 Troubleshooting Quick Fixes

### ❌ "Model not found" error
```bash
cd model && python main.py
```
Then restart backend (Ctrl+C and re-run)

### ❌ "Port 8000 already in use"
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### ❌ "Can't connect to backend"
- [ ] Backend terminal shows "Uvicorn running..."?
- [ ] Is model loaded? Check for "[INFO] Model loaded successfully..."
- [ ] Try http://localhost:8000/health

### ❌ "Confidence very low (~50-60%)"
- [ ] Model not trained properly
- [ ] Run: `cd model && python main.py`
- [ ] Check training accuracy in output
- [ ] Should be >75% for good model

### ❌ "Predictions not saving"
- [ ] Are you logged in? (Guest mode doesn't save)
- [ ] Did you run `python create_admin.py`?
- [ ] Check `parkinsons.db` file exists

---

## 📊 Expected Results

### ✅ You Should See:

**Terminal 1 (Backend):**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
[INFO] Model loaded successfully from model/parkinsons_detector.keras
```

**Terminal 2 (Frontend):**
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

**Browser (http://localhost:8501):**
- Login/Register/Guest Mode tabs visible
- Upload button works
- Analysis shows:
  - ✅ Prediction (Healthy or Parkinson)
  - ✅ Confidence % (should be >80%)
  - ✅ Detailed Analysis with both class confidences

---

## 📝 Session Quick Start (After Setup)

Each time you want to work on the project:

```bash
# Terminal 1
venv\Scripts\activate              # Windows
# OR source venv/bin/activate      # Mac/Linux

uvicorn backend.main:app --reload --port 8000
```

```bash
# Terminal 2 (new terminal, activate venv there too)
streamlit run frontend/app.py
```

Then visit: http://localhost:8501

---

## ✨ Reference Links

| Task | Link |
|------|------|
| Full deployment guide | [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) |
| Fixes applied (confidence scores) | [FIXES_APPLIED.md](FIXES_APPLIED.md) |
| Architecture overview | [README_DEPLOYMENT.md](README_DEPLOYMENT.md) |
| Detailed deployment info | [DEPLOYMENT.md](DEPLOYMENT.md) |

---

**Status:** ✅ Ready to deploy!

**Current Step:** Choose the phase above and follow the checklist.
