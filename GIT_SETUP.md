# 🔧 Git & GitHub Setup Guide

> Complete git commands and GitHub deployment for Parkinson's Detection AI

---

## ⚠️ Large Files & Git LFS

### Do You Need Git LFS?

**YES - Your project has large files:**

| File | Size | Needs LFS? |
|------|------|-----------|
| `model/parkinsons_detector.keras` | ~200-300MB | ✅ **YES** |
| `dataset/train/healthy/*.jpg` | ~50-100 each | ⚠️ Optional |
| `dataset/test/parkinson/*.jpg` | ~50-100 each | ⚠️ Optional |
| `.env` | <1KB | ❌ No (ignored) |
| `venv/` | N/A | ❌ No (ignored) |
| `parkinsons.db` | Variable | ❌ No (ignored) |

**Recommendation:** 
- ✅ Use Git LFS for `.keras` model files
- ✅ Use Git LFS if including dataset images (optional)
- ❌ Don't track `venv/`, `.db`, or `.env` (already ignored)

---

## 🚀 STEP 1: Install Git LFS

### Windows:
```bash
# Using Chocolatey (if installed)
choco install git-lfs

# OR download from: https://git-lfs.github.com
# Download and run installer
```

### Mac:
```bash
brew install git-lfs
```

### Linux:
```bash
# Debian/Ubuntu
sudo apt-get install git-lfs

# Fedora
sudo dnf install git-lfs

# Red Hat
sudo yum install git-lfs
```

### Verify Installation:
```bash
git lfs version
# Should show: git-lfs/3.x.x (or similar)
```

---

## 🎯 STEP 2: Initialize Git & LFS

### Initialize Git Repository:
```bash
cd /path/to/Parkinson-Project-main
git init
```

### Initialize Git LFS:
```bash
git lfs install
```

### Track Large Files with LFS:
```bash
# Track model files
git lfs track "*.keras"

# Track large image files (optional)
git lfs track "dataset/**/*.jpg"
git lfs track "dataset/**/*.png"

# Verify tracking
cat .gitattributes
```

**Expected output in `.gitattributes`:**
```
*.keras filter=lfs diff=lfs merge=lfs -text
dataset/**/*.jpg filter=lfs diff=lfs merge=lfs -text
dataset/**/*.png filter=lfs diff=lfs merge=lfs -text
```

---

## 📝 STEP 3: Verify & Update .gitignore

Your `.gitignore` looks good, but verify it includes:

```gitignore
# Already included ✅
venv/
.env
*.db
*.sqlite
__pycache__/

# Make sure to add these if missing:
parkinsons.db
temp*.jpg
*.pyc
.DS_Store
```

### Check what will be committed:
```bash
git status

# This shows:
# - Green (will commit): source code, requirements.txt, frontend/app.py, etc.
# - Ignored (gray): venv/, .env, *.db
# - Untracked: model files (if LFS tracking setup)
```

---

## 🔄 STEP 4: Add Files & Commit

### Add Everything (Respects .gitignore):
```bash
git add .
```

### Check what will be committed:
```bash
git status
```

**Expected:**
```
Changes to be committed:
  new file: backend/main.py
  new file: frontend/app.py
  new file: model/main.py
  new file: model/parkinsons_detector.keras (pointer to LFS)
  ...
```

### First Commit:
```bash
git commit -m "Initial commit: Parkinson's Detection AI system"
```

---

## 🌐 STEP 5: Connect to GitHub

### Create GitHub Repository

1. Go to https://github.com/new
2. **Repository name:** `Parkinson-Project` (or your preferred name)
3. **Description:** "AI-powered Parkinson's disease detection using spiral drawing analysis"
4. **Visibility:** Public (for Streamlit Cloud deployment)
5. **DO NOT initialize** with README/gitignore (we have these)
6. Click "Create repository"

### Add Remote & Push

Copy the commands from GitHub after creating repo. They look like:

```bash
# Add remote (replace with your username/repo)
git remote add origin https://github.com/YOUR_USERNAME/Parkinson-Project.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**First push with LFS might take longer** (uploading model file)

---

## 📋 Complete Git Workflow

### Initial Setup (One Time)
```bash
# 1. Navigate to project
cd Parkinson-Project-main

# 2. Initialize git & LFS
git init
git lfs install

# 3. Track large files
git lfs track "*.keras"

# 4. Add all files
git add .

# 5. First commit
git commit -m "Initial commit: Parkinson's Detection AI"

# 6. Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/Parkinson-Project.git

# 7. Push to GitHub
git push -u origin main
```

### Daily Workflow (After Changes)

```bash
# 1. Check status
git status

# 2. Add changes
git add .

# 3. Commit with message
git commit -m "Fixed confidence score display"

# 4. Push to GitHub
git push
```

### One-Liner Commit:
```bash
git add . && git commit -m "Your message" && git push
```

---

## 🚀 Common Git Commands

### Status & Info
```bash
git status                    # See what's changed
git log                       # See commit history
git log --oneline             # Compact commit history
git diff                      # See specific changes
git show HEAD                 # See last commit details
```

### Making Changes
```bash
git add .                     # Stage all changes
git add file.py               # Stage specific file
git commit -m "message"       # Commit with message
git push                      # Push to GitHub
git pull                      # Pull latest from GitHub
```

### Branches
```bash
git branch                    # List branches
git branch -a                 # List all (local + remote)
git checkout -b feature-name  # Create new branch
git checkout main             # Switch to main
git merge feature-name        # Merge branch into current
```

### Undo Changes
```bash
git restore file.py           # Undo changes to file
git reset HEAD~1              # Undo last commit (keep changes)
git reset --hard HEAD~1       # Undo last commit (delete changes)
git revert HEAD               # Create new commit that undoes last
```

---

## 🔐 GitHub Authentication

### Option 1: HTTPS with Personal Access Token (Recommended)

1. **Create Personal Access Token (PAT):**
   - Go to https://github.com/settings/tokens
   - Click "Generate new token"
   - Give it permissions: `repo`, `read:org`
   - Copy the token (save it somewhere safe!)

2. **Use token when pushing:**
   ```bash
   # First push (will ask for credentials)
   git push -u origin main
   
   # Enter:
   # Username: YOUR_GITHUB_USERNAME
   # Password: YOUR_PERSONAL_ACCESS_TOKEN (not your actual password!)
   ```

3. **Optional: Save credentials**
   ```bash
   git config --global credential.helper store
   # Next push will save credentials
   ```

### Option 2: SSH Key (More Secure)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy key to GitHub
# 1. Go to https://github.com/settings/keys
# 2. Click "New SSH key"
# 3. Paste your public key (from ~/.ssh/id_ed25519.pub)

# Use SSH remote instead
git remote set-url origin git@github.com:YOUR_USERNAME/Parkinson-Project.git
```

---

## 📊 GitHub Files Checklist

Your repository should include:

### ✅ Essential Source Code
```
backend/
  ├── main.py              # FastAPI application
  ├── models.py            # Database models
  ├── database.py          # Database config
  └── requirements.txt
  
frontend/
  ├── app.py               # Streamlit app
  └── requirements.txt
  
model/
  ├── main.py              # Training script
  └── parkinsons_detector.keras (LFS tracked)
  
dataset/
  ├── train/
  │   ├── healthy/
  │   └── parkinson/
  └── test/
      ├── healthy/
      └── parkinson/
```

### ✅ Documentation
```
README.md                           # Project overview
DEPLOYMENT.md                       # Deployment guide
STREAMLIT_DEPLOYMENT.md             # Streamlit guide
STREAMLIT_QUICK_CHECKLIST.md        # Quick checklist
TROUBLESHOOTING.md                  # Troubleshooting
FIXES_APPLIED.md                    # What was fixed
DEPLOYMENT_INDEX.md                 # Navigation
DEPLOYMENT_CHECKLIST.md             # Changes summary
```

### ✅ Configuration
```
.env.example                        # Env template
.gitignore                          # Git ignore rules
docker-compose.yml                  # Docker config
Dockerfile                          # Container definition
```

### ✅ Scripts
```
create_admin.py                     # Admin creation
startup.py                          # Startup checks
deploy.bat                          # Windows deploy script
deploy.sh                           # Linux/Mac script
```

### ❌ NOT Included (Ignored)
```
venv/                               # Virtual environment
.env                                # Sensitive variables
*.db                                # Database files
__pycache__/                        # Python cache
.idea/, .vscode/                    # IDE files
temp*.jpg                           # Temp files
```

---

## 🎯 Complete Setup (Copy-Paste)

### For Windows:
```bash
# 1. Install Git LFS
choco install git-lfs
# OR download from https://git-lfs.github.com

# 2. Navigate to project
cd C:\Users\chopr\Downloads\Parkinson-Project-main\Parkinson-Project-main

# 3. Initialize
git init
git lfs install
git lfs track "*.keras"
git add .gitattributes

# 4. First commit
git add .
git commit -m "Initial commit: Parkinson's Detection AI"

# 5. Add GitHub remote (replace YOUR_USERNAME/REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/Parkinson-Project.git
git branch -M main

# 6. Push
git push -u origin main
```

### For Mac/Linux:
```bash
# 1. Install Git LFS
brew install git-lfs      # Mac
# OR: sudo apt-get install git-lfs  # Ubuntu/Debian

# 2. Navigate to project
cd ~/Downloads/Parkinson-Project-main

# 3. Initialize
git init
git lfs install
git lfs track "*.keras"
git add .gitattributes

# 4. First commit
git add .
git commit -m "Initial commit: Parkinson's Detection AI"

# 5. Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/Parkinson-Project.git
git branch -M main

# 6. Push
git push -u origin main
```

---

## ✅ Verify GitHub Setup

After pushing to GitHub:

1. **Visit your repository:**
   ```
   https://github.com/YOUR_USERNAME/Parkinson-Project
   ```

2. **Check files are there:**
   - ✅ backend/ folder
   - ✅ frontend/ folder
   - ✅ model/ folder (with .keras file)
   - ✅ README.md
   - ✅ DEPLOYMENT.md

3. **Check LFS is working:**
   ```bash
   git lfs ls-files
   # Should show: *.keras (LFS pointer)
   ```

4. **Verify ignored files:**
   - ❌ venv/ should NOT be there
   - ❌ .env should NOT be there
   - ❌ *.db should NOT be there

---

## 🚀 Deploy from GitHub (Streamlit Cloud)

Once your code is on GitHub:

1. Go to https://share.streamlit.io
2. Click "New app"
3. Select:
   - **Repository:** YOUR_USERNAME/Parkinson-Project
   - **Branch:** main
   - **File path:** frontend/app.py
4. Click "Deploy"
5. Add secrets in "Advanced settings":
   ```toml
   SECRET_KEY = "your_secret_key"
   DATABASE_URL = "sqlite:///./parkinsons.db"
   BACKEND_URL = "https://your-backend-url.com"
   ```

---

## 📊 Git Commands Quick Reference

```bash
# Setup
git init                              # Initialize repo
git remote add origin <url>           # Add GitHub
git remote -v                         # Verify remote

# Daily work
git status                            # Check changes
git add .                             # Stage changes
git commit -m "message"               # Commit
git push                              # Push to GitHub
git pull                              # Pull from GitHub

# LFS
git lfs install                       # Initialize LFS
git lfs track "*.keras"               # Track file type
git lfs ls-files                      # List LFS files

# Branches
git checkout -b feature               # Create branch
git checkout main                     # Switch to main
git merge feature                     # Merge branch
git branch -d feature                 # Delete branch

# History
git log --oneline                     # Commit history
git show <commit>                     # Show commit
git diff                              # See changes
```

---

## 🔧 Troubleshooting Git

### Issue: "fatal: not a git repository"
```bash
git init
git remote add origin <url>
```

### Issue: "Git LFS not initialized"
```bash
git lfs install
git lfs track "*.keras"
```

### Issue: "Permission denied" when pushing
```bash
# Use personal access token instead of password
# Go to https://github.com/settings/tokens
# Use token as password
```

### Issue: Large file rejected
```bash
# Make sure LFS is tracking it
git lfs track "*.keras"
git add .gitattributes
git commit -m "Track large files with LFS"
# Try push again
```

### Issue: ".env is tracked but shouldn't be"
```bash
# Remove from git (but keep locally)
git rm --cached .env
git commit -m "Remove .env from tracking"
```

---

## 📋 Pre-GitHub Checklist

Before your first push:

- [ ] Git installed and working
- [ ] Git LFS installed: `git lfs version`
- [ ] Model trained: `model/parkinsons_detector.keras` exists (>100MB)
- [ ] `.gitignore` in place (with venv/, .env, *.db)
- [ ] `.gitattributes` created (tracks *.keras)
- [ ] Project initialized: `git init`
- [ ] Files added: `git add .`
- [ ] First commit: `git commit -m "Initial commit"`
- [ ] GitHub repo created (empty, no README)
- [ ] Remote added: `git remote add origin ...`
- [ ] Ready to push: `git push -u origin main`

---

## ✨ After First Push

Your repository is now on GitHub! Next:

1. **Share link:** `https://github.com/YOUR_USERNAME/Parkinson-Project`
2. **Deploy to Streamlit Cloud:** Follow STREAMLIT_DEPLOYMENT.md Step 10
3. **Invite collaborators:** GitHub → Settings → Collaborators
4. **Set up CI/CD:** (Optional) Add GitHub Actions for auto-testing

---

## 🎯 Common Workflows

### When you make changes locally:
```bash
# Make your changes, then:
git add .
git commit -m "Fixed login bug"
git push
```

### When working with team:
```bash
# Before starting work
git pull

# Make changes
git add .
git commit -m "Added new feature"
git push

# If conflict:
git pull
# Fix conflicts manually
git add .
git commit -m "Resolved merge conflict"
git push
```

### When creating a new feature:
```bash
# Create feature branch
git checkout -b feature/add-export-pdf

# Make changes
git add .
git commit -m "Add PDF export feature"
git push -u origin feature/add-export-pdf

# When ready, merge to main
git checkout main
git pull
git merge feature/add-export-pdf
git push
```

---

**Ready to push to GitHub?** Follow the "Complete Setup" section above! 🚀
