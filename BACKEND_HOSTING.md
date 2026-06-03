# 🚀 Backend Hosting - Do You Need It?

> Guide to hosting your FastAPI backend alongside Streamlit frontend

---

## ❓ Simple Answer

### **YES - You need to host the backend** ✅

**Why?**
- Streamlit Cloud runs in the cloud (their servers)
- Your local machine can't stay on 24/7
- Streamlit app needs to communicate with backend
- If backend is on your local machine, it dies when you close laptop

---

## 🏗️ Architecture Breakdown

### ❌ Don't Do This (Frontend on Cloud, Backend Local):
```
┌─ Your Laptop ─────────┐
│  Backend: localhost   │  ← Goes offline when you close laptop
└───────────────────────┘
           ↓
┌─ Streamlit Cloud ─────┐
│  Frontend (deployed)  │  ← Can't reach backend!
└───────────────────────┘
```

### ✅ Do This (Both Deployed):
```
┌─ Streamlit Cloud ─────────────┐
│  Frontend (deployed)          │
└───────────────────────────────┘
           ↓ REST API
┌─ Render/Heroku/etc ──────────┐
│  Backend (deployed)           │
│  + Model                      │
│  + Database                   │
└───────────────────────────────┘
```

---

## 📊 Deployment Options

### Option 1: **Render.com** (⭐ RECOMMENDED - Free Tier)

**Pros:**
- ✅ Free tier available
- ✅ Easy deployment from GitHub
- ✅ Automatic deployments on git push
- ✅ Good for hobby projects
- ✅ Faster than Heroku free

**Cons:**
- ❌ Free tier spins down after 15 min inactivity
- ❌ First request is slow (needs to wake up)

**Cost:** Free (with limitations) or $7/month for always-on

**Setup:** 5 minutes (connect GitHub, deploy)

### Option 2: **Heroku** (Traditional, Being Phased Out)

**Pros:**
- ✅ Very easy to deploy
- ✅ Good documentation
- ✅ Industry standard

**Cons:**
- ❌ Free tier REMOVED (as of Nov 2022)
- ❌ Cheapest paid: $5/month
- ❌ Slower than alternatives

**Cost:** $5/month minimum

**Setup:** 10 minutes

### Option 3: **Railway.app** (Modern, Better Than Heroku)

**Pros:**
- ✅ $5 free monthly credit
- ✅ Pay-as-you-go
- ✅ Fast, reliable
- ✅ Easy GitHub integration

**Cons:**
- ❌ Credit runs out (~3-4 months for hobby)
- ❌ Then you pay per usage

**Cost:** Free credit ($5/month) + pay-as-you-go

**Setup:** 5 minutes

### Option 4: **AWS/Azure/GCP** (Enterprise)

**Pros:**
- ✅ Unlimited scalability
- ✅ Always on
- ✅ Professional grade

**Cons:**
- ❌ Complex setup
- ❌ Billing can be confusing
- ❌ Overkill for hobby project

**Cost:** $5-50+/month depending on usage

**Setup:** 30+ minutes

### Option 5: **Local (During Development Only)**

**Pros:**
- ✅ Free
- ✅ No deployment needed

**Cons:**
- ❌ Only works while laptop is on
- ❌ Not suitable for public use
- ❌ Internet must be stable

**Use Case:** Local testing only

---

## 🎯 Recommendation for Your Project

### **Best Option: Render.com** ✅

**Why:**
- Free tier available
- Super easy setup
- GitHub integration (auto-deploy on git push)
- Perfect for hobby/academic projects
- Can upgrade to paid if needed

**Setup Steps:**
1. Push backend to GitHub (via Git LFS)
2. Go to https://render.com
3. Create new "Web Service"
4. Connect GitHub repo
5. Select branch and main file
6. Deploy
7. Get deployed URL (e.g., `https://your-api.onrender.com`)
8. Update Streamlit `.env` with new URL

**Cost:** Free (with wake-up delay) or $7/month for always-on

---

## 🔄 How Frontend & Backend Communicate

### In `.env` file (Frontend):

```env
# During development
BACKEND_URL=http://localhost:8000

# After backend deployed to Render
BACKEND_URL=https://your-api.onrender.com
```

The frontend automatically uses this URL for all API calls:
```python
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Later in code
response = requests.post(f"{BACKEND_URL}/predict", ...)
```

### On Streamlit Cloud (Frontend):

1. Deploy frontend to Streamlit Cloud
2. In Streamlit Cloud settings → "Secrets"
3. Add:
   ```toml
   BACKEND_URL = "https://your-api.onrender.com"
   ```

---

## 📋 Comparison Table

| Platform | Free Tier | Always On | Setup Time | Cost |
|----------|-----------|-----------|-----------|------|
| **Render** | ✅ Yes | ❌ 15 min (wake-up) | 5 min | Free/$7 |
| **Railway** | ✅ $5/mo | ✅ Yes | 5 min | Free+Pay |
| **Heroku** | ❌ No | ✅ Yes | 10 min | $5+/mo |
| **Fly.io** | ⚠️ Limited | ✅ Yes | 15 min | $3+/mo |
| **AWS/Azure** | ⚠️ Limited | ✅ Yes | 30+ min | $5+/mo |
| **Local** | ✅ Yes | ❌ Manual | 0 min | Free |

---

## 🚀 Quick Deployment (Render.com)

### Step 1: Prepare Backend for Deployment

Add `Procfile` to project root:
```
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Add to `backend/requirements.txt`:
```
uvicorn==0.24.0
gunicorn==21.2.0
```

### Step 2: Push to GitHub

```bash
git add Procfile
git commit -m "Add Procfile for deployment"
git push
```

### Step 3: Deploy on Render

1. Go to https://render.com
2. Sign up / Log in with GitHub
3. Click "New +" → "Web Service"
4. Select your repository
5. Configure:
   - **Name:** `parkinson-api` (or your choice)
   - **Environment:** Python 3
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables:
   ```
   BACKEND_URL=http://localhost:8000  (this is for local, keep it)
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///./parkinsons.db
   MODEL_PATH=model/parkinsons_detector.keras
   ```
7. Click "Create Web Service"
8. Wait 3-5 minutes for deployment
9. Get your URL: `https://your-service-name.onrender.com`

### Step 4: Update Frontend

In `.env` (for Streamlit Cloud):
```env
BACKEND_URL=https://your-service-name.onrender.com
```

In Streamlit Cloud secrets (Settings → Secrets):
```toml
BACKEND_URL = "https://your-service-name.onrender.com"
```

---

## 💰 Cost Breakdown

### Scenario: Hobby Project (Low Traffic)

| Component | Platform | Cost |
|-----------|----------|------|
| **Frontend** | Streamlit Cloud | Free |
| **Backend** | Render (Free) | Free (15-min wake delay) |
| **Database** | SQLite (free) | Free |
| **Model** | Included in backend | Free |
| **Total** | - | **$0/month** |

### Scenario: Production (Moderate Traffic)

| Component | Platform | Cost |
|-----------|----------|------|
| **Frontend** | Streamlit Cloud | Free |
| **Backend** | Render (Always-on) | $7/month |
| **Database** | PostgreSQL (free) | Free |
| **Model** | Included | Free |
| **Total** | - | **$7/month** |

---

## 🔄 Workflow Summary

### For Development (Local):
```bash
# Terminal 1: Backend on localhost:8000
uvicorn backend.main:app --reload --port 8000

# Terminal 2: Frontend on localhost:8501
streamlit run frontend/app.py
```

Frontend `.env`:
```env
BACKEND_URL=http://localhost:8000
```

### For Production (Deployed):
```
Frontend: https://your-app.streamlit.app
Backend: https://your-api.onrender.com
Database: PostgreSQL (optional upgrade)
```

Frontend Streamlit Cloud secrets:
```toml
BACKEND_URL = "https://your-api.onrender.com"
```

---

## ✅ Complete Deployment Checklist

### Before Deploying Backend:

- [ ] Backend code pushed to GitHub (with Git LFS)
- [ ] Model file exists: `model/parkinsons_detector.keras`
- [ ] `Procfile` created in project root
- [ ] `.env.example` has all required variables
- [ ] `backend/requirements.txt` has all dependencies
- [ ] Tested locally: backend works on `localhost:8000`

### Deploying Backend (Render):

- [ ] Create Render account
- [ ] Connect GitHub
- [ ] Create new Web Service
- [ ] Select repository and branch
- [ ] Set environment variables
- [ ] Deploy and get URL
- [ ] Test API: `https://your-api.onrender.com/health`
- [ ] Should return: `{"status":"ok","model_loaded":true}`

### Deploying Frontend (Streamlit Cloud):

- [ ] Create Streamlit account
- [ ] Go to https://share.streamlit.io
- [ ] Create new app from GitHub repo
- [ ] Select `frontend/app.py`
- [ ] Go to "Settings" → "Secrets"
- [ ] Add: `BACKEND_URL = "https://your-api.onrender.com"`
- [ ] Deploy
- [ ] Test predictions

---

## 🎯 Decision: Local Backend vs Deployed?

### Use Local Backend If:
- ✅ Just testing/developing
- ✅ Not sharing with others yet
- ✅ Working on your laptop only

### Deploy Backend If:
- ✅ Sharing app with team/public
- ✅ Want it available 24/7
- ✅ Production use
- ✅ **Deploying frontend to Streamlit Cloud** ← This requires it!

---

## 🚀 Recommended Path

### Step 1: Develop Locally
```bash
# Both running on localhost
# Frontend: localhost:8501
# Backend: localhost:8000
```

### Step 2: Deploy Backend (to Render)
```
Backend: https://your-api.onrender.com
Frontend: Still local (localhost:8501)
```

### Step 3: Deploy Frontend (to Streamlit Cloud)
```
Frontend: https://your-app.streamlit.app
Backend: https://your-api.onrender.com
```

---

## 📚 Next Steps

1. **For backend deployment:** See backend deployment guide
2. **For frontend deployment:** [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) → Step 10
3. **Combining both:** See this file for environment variables

---

## 💡 Pro Tips

### Tip 1: Keep Same Code for Both Local & Deployed
```python
# Works for both localhost and deployed backend
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
```

### Tip 2: Test Deployed Backend Before Frontend
```bash
# After deploying backend to Render, test it:
curl https://your-api.onrender.com/health

# Should return:
# {"status":"ok","model_loaded":true}
```

### Tip 3: Render Wake-Up Delay
- Free tier: First request takes 30-60 seconds (service wakes up)
- Subsequent requests: Fast
- Solution: Upgrade to paid tier ($7/month) for always-on

### Tip 4: Database Options
- **Local:** SQLite (included, no setup)
- **Cloud:** PostgreSQL (free tier on Render)
- For production, use PostgreSQL

---

## 🆘 Common Issues

### Issue: "Connection refused" when frontend tries to reach backend
**Cause:** Backend URL wrong or backend not running
**Solution:**
1. Check `BACKEND_URL` in `.env`
2. Test URL manually: `curl https://your-api.onrender.com/health`
3. Verify backend deployed: https://dashboard.render.com

### Issue: Model file not found on deployed backend
**Cause:** Model uploaded but not tracked with Git LFS
**Solution:**
1. Push model with Git LFS: See [GIT_LFS_GUIDE.md](GIT_LFS_GUIDE.md)
2. Re-deploy on Render

### Issue: Slow predictions on Render free tier
**Cause:** Backend wakes up from sleep
**Solution:**
- Upgrade to Render paid ($7/month), or
- Keep free and wait for first request to warm up

---

## 📊 Architecture After Deployment

```
Users
  ↓
┌──────────────────────────────────┐
│ Streamlit Cloud                  │
│ https://yourapp.streamlit.app    │
│ (Frontend: frontend/app.py)      │
└──────────────────────────────────┘
  ↓ REST API (via BACKEND_URL)
┌──────────────────────────────────┐
│ Render.com                       │
│ https://your-api.onrender.com    │
│ (Backend: backend/main.py)       │
├──────────────────────────────────┤
│ - TensorFlow Model               │
│ - SQLite Database                │
│ - FastAPI Server                 │
└──────────────────────────────────┘
```

---

## ✨ Summary

| Question | Answer |
|----------|--------|
| Do I need to host backend? | ✅ YES (if deploying frontend) |
| Can backend stay on laptop? | ❌ NO (goes offline) |
| Best free option? | ✅ Render.com |
| Cost for free tier? | ✅ $0 (with wake-up delay) |
| Cost for always-on? | 💰 $7-10/month |
| Easiest setup? | ✅ Render.com (5 min) |
| Can I test locally first? | ✅ YES |

---

## 🎯 Next Steps

1. **Test backend locally first:**
   - Follow [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) Step 6-7

2. **Push to GitHub:**
   - Follow [GIT_COPYPASTE.md](GIT_COPYPASTE.md)

3. **Deploy backend to Render:**
   - Follow backend deployment guide (coming soon)

4. **Deploy frontend to Streamlit Cloud:**
   - Follow [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) Step 10

5. **Test both together:**
   - Make prediction in Streamlit app
   - Should see high confidence score

---

**Ready to deploy?** Start with: [GIT_COPYPASTE.md](GIT_COPYPASTE.md) → [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) → Backend Hosting Guide (see next document)

