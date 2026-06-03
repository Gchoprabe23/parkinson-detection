# 🚀 Deploy Backend to Render.com - Quick Guide

> Fast, easy backend deployment using Render (recommended)

---

## ⚡ TL;DR

1. ✅ Push backend to GitHub (with Git LFS)
2. ✅ Create Render account
3. ✅ Deploy in 5 minutes
4. ✅ Get URL: `https://your-api.onrender.com`
5. ✅ Update frontend with URL

---

## 📋 Prerequisites

- ✅ Backend code on GitHub (via [GIT_COPYPASTE.md](GIT_COPYPASTE.md))
- ✅ Model file exists: `model/parkinsons_detector.keras`
- ✅ Backend works locally: `uvicorn backend.main:app --reload --port 8000`

---

## 🎯 Step-by-Step Deployment

### Step 1: Create Procfile (Project Root)

Create file: `Procfile` (no extension)

```
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

### Step 2: Update requirements.txt (Backend)

Make sure `backend/requirements.txt` includes:

```
fastapi==0.104.1
uvicorn==0.24.0
python-jose==3.3.0
python-multipart==0.0.6
sqlalchemy==2.0.23
pydantic==2.5.0
email-validator==2.1.0
requests==2.31.0
python-dotenv==1.0.0
numpy==1.26.2
Pillow==10.1.0
tensorflow==2.14.0
imutils==0.5.4
opencv-python-headless==4.8.1.78
passlib==1.7.4
bcrypt==4.1.1
python-multipart==0.0.6
```

### Step 3: Push Changes to GitHub

```bash
git add Procfile backend/requirements.txt
git commit -m "Add Render deployment config"
git push
```

### Step 4: Create Render Account

1. Go to https://render.com
2. Click "Sign up"
3. Choose "GitHub" for login
4. Authorize Render to access your GitHub

### Step 5: Create New Web Service

1. In Render dashboard, click "New +" button
2. Select "Web Service"
3. Connect to your GitHub repository
4. Select: **Parkinson-Project** (or your repo name)
5. Select branch: **main**

### Step 6: Configure Deployment

Fill in the form:

**Basic Settings:**
- **Name:** `parkinson-api` (your choice)
- **Environment:** Python 3
- **Region:** Leave default (closest to you)
- **Branch:** main

**Build & Deploy:**
- **Build Command:** `pip install -r backend/requirements.txt`
- **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

### Step 7: Add Environment Variables

Scroll down to "Environment" section and add:

```
KEY                 VALUE
────────────────────────────────────────────
SECRET_KEY          your_super_secret_key_here
DATABASE_URL        sqlite:///./parkinsons.db
MODEL_PATH          model/parkinsons_detector.keras
BACKEND_URL         http://localhost:8000
```

**Note:** These values don't really matter for the backend, they're just defaults

### Step 8: Select Plan

- ✅ Leave default (Free tier)
- ⚠️ Free tier: Goes to sleep after 15 min inactivity
- 💰 Paid: $7/month for always-on

### Step 9: Deploy!

Click "Create Web Service"

**Wait 3-5 minutes** while Render:
- Installs dependencies (including TensorFlow ~500MB)
- Builds Docker image
- Starts the service
- Assigns domain

---

## ✅ Verify Deployment

### Check Status:
1. Go to your Render dashboard: https://dashboard.render.com
2. Click your service name
3. Watch "Deploy log" for progress
4. Wait until status says "Live" ✅

### Get Your URL:
Your URL will be: `https://parkinson-api.onrender.com` (or whatever name you chose)

**Check it displays as:**
```
The service is live at: https://your-service-name.onrender.com
```

### Test API Health:

```bash
curl https://your-service-name.onrender.com/health

# Should return:
# {"status":"ok","model_loaded":true}
```

Or visit in browser:
```
https://your-service-name.onrender.com/health
```

---

## 📊 Deployment Times

| Step | Time |
|------|------|
| Dependencies install | 2-3 min |
| Docker build | 1-2 min |
| Service start | 30 sec |
| **Total** | **3-5 min** |

**First deployment is slower** due to TensorFlow installation

---

## 🔄 Update Frontend

### Option A: Local Testing

Update `.env`:
```env
BACKEND_URL=https://your-service-name.onrender.com
```

Restart frontend:
```bash
streamlit run frontend/app.py
```

### Option B: Streamlit Cloud Deployment

1. Go to https://share.streamlit.io
2. Deploy frontend as usual (see [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) Step 10)
3. After deployed, click "Settings" (gear icon)
4. Click "Secrets"
5. Add:
   ```toml
   BACKEND_URL = "https://your-service-name.onrender.com"
   ```
6. Streamlit auto-restarts with new URL

---

## 🆘 Troubleshooting

### Issue: Deploy fails - "No such file"
**Check:** Make sure `backend/requirements.txt` exists and has all dependencies

### Issue: "Model not found" error after deployment
**Check:** Model file uploaded with Git LFS (see [GIT_LFS_GUIDE.md](GIT_LFS_GUIDE.md))

### Issue: Build errors (Pillow, pandas, zlib, etc.)
**Fix:** See [DEPLOYMENT_FIXES.md](DEPLOYMENT_FIXES.md) for all solutions
**TL;DR:** These are already fixed! Just push your latest code

### Issue: Slow first response (30+ seconds)
**Normal:** Free tier has 15-min inactivity sleep
**Solution:** Send ping request before frontend makes actual request

### Issue: "Address already in use"
**Not applicable** - Render manages ports automatically

### Issue: Still shows deployment log but no "Live"
**Wait:** Sometimes takes 5-10 minutes for complex builds
**Check logs:** Look for error messages in deploy log

### Issue: Python 3.14 compatibility errors
**SOLVED:** Updated requirements to work with Python 3.11
**What changed:** See [DEPLOYMENT_FIXES.md](DEPLOYMENT_FIXES.md#️-critical-issues--solutions)

---

## 📈 After Deployment

### Monitor Your Service:
- Dashboard: https://dashboard.render.com
- View logs: Click service → "Logs"
- Check health: API endpoint → `/health`

### Update Code:
```bash
# Make changes locally
git add .
git commit -m "Your changes"
git push

# Render auto-deploys on push!
```

### Scale Up (Optional):
- Go to Settings → "Instance Type"
- Upgrade from Free to Starter ($7/month)
- Always-on (no sleep)

---

## 💰 Pricing

| Tier | Cost | Features |
|------|------|----------|
| **Free** | $0 | Sleep after 15 min |
| **Starter** | $7/mo | Always on |
| **Standard** | $12/mo | More memory |

---

## 🎯 Your Backend URL

After deployment, you'll have a URL like:

```
https://parkinson-api.onrender.com
```

**Use this URL everywhere:**
- Frontend `.env`: `BACKEND_URL=https://parkinson-api.onrender.com`
- Streamlit Cloud secrets: `BACKEND_URL = "https://parkinson-api.onrender.com"`
- Tests: `curl https://parkinson-api.onrender.com/health`

---

## ✅ Deployment Checklist

- [ ] Procfile created in project root
- [ ] backend/requirements.txt complete
- [ ] Changes pushed to GitHub
- [ ] Render account created
- [ ] Web Service created
- [ ] Environment variables added
- [ ] Deployment started
- [ ] Status shows "Live" ✅
- [ ] Health check passes: `/health` returns ok
- [ ] Frontend updated with BACKEND_URL

---

## 🔗 Auto-Deployment

**Bonus:** Render auto-deploys on git push!

```bash
# Make changes
# Push to GitHub
git push

# Render automatically:
# 1. Detects new push
# 2. Starts deployment
# 3. Rebuilds and restarts
# 4. Updates live endpoint

# You're done! No manual deployment needed
```

---

## 📚 Next Steps

1. ✅ Deploy backend (this guide)
2. ✅ Test API: `https://your-api.onrender.com/health`
3. ✅ Update frontend URL
4. ✅ Deploy frontend to Streamlit Cloud: [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) Step 10
5. ✅ Test end-to-end (frontend → backend → predictions)

---

## 🚀 From Here

**If everything works:**
- ✅ Frontend: https://your-app.streamlit.app
- ✅ Backend: https://your-api.onrender.com
- ✅ **You're live!** 🎉

**Share your app:**
```
Frontend URL: https://your-app.streamlit.app
Users can make predictions without setup!
```

---

## 💡 Pro Tips

### Tip 1: Check Logs
```
Render Dashboard → Your Service → Logs
See all errors and activity
```

### Tip 2: Manual Redeploy
```
If needed: Click "Manual Deploy" button
Forces a fresh deployment
```

### Tip 3: Environment Variables
```
Can be changed in Settings → Environment
Auto-restarts with new values
```

### Tip 4: Custom Domain (Optional)
```
Settings → Custom Domain
Add your own domain instead of onrender.com
```

---

## ✨ You're Done!

Your backend is now **live and accessible**!

Share the URL:
```
https://your-service-name.onrender.com
```

Next: Deploy frontend to Streamlit Cloud (see [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md))

---

**Questions?** See [BACKEND_HOSTING.md](BACKEND_HOSTING.md) for more deployment options

