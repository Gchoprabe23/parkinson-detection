# 🎯 Git Setup - Copy & Paste Commands

> Just copy-paste these commands in order. Replace `YOUR_USERNAME` with your GitHub username.

---

## ✅ Prerequisites

- [ ] Git installed (https://git-scm.com)
- [ ] Git LFS installed
  - Windows: `choco install git-lfs` OR download from https://git-lfs.github.com
  - Mac: `brew install git-lfs`
  - Linux: `sudo apt-get install git-lfs`
- [ ] GitHub account (https://github.com/signup)

Verify:
```bash
git --version
git lfs version
```

---

## 🚀 COMMAND SEQUENCE (Copy-Paste)

### Command 1: Initialize Git & LFS

```bash
cd "C:\Users\chopr\Downloads\Parkinson-Project-main\Parkinson-Project-main"
git init
git lfs install
git lfs track "*.keras"
git add .gitattributes
```

### Command 2: First Commit

```bash
git add .
git commit -m "Initial commit: Parkinson's Detection AI system"
```

### Command 3: Verify Status

```bash
git status
git log --oneline
git lfs ls-files
```

**Should show:**
- ✅ Nothing to commit (working tree clean)
- ✅ Your commit in the log
- ✅ `model/parkinsons_detector.keras` in LFS files

### Command 4: Create GitHub Repo & Connect

**DO THIS IN BROWSER:**
1. Go to https://github.com/new
2. **Repository name:** `Parkinson-Project`
3. **Visibility:** Public
4. **DO NOT** add README/License/gitignore
5. Click "Create repository"

**THEN RUN THESE:**

```bash
git remote add origin https://github.com/YOUR_USERNAME/Parkinson-Project.git
git branch -M main
git push -u origin main
```

> When prompted for password: Use your **personal access token** (not password)
> 
> Get token: https://github.com/settings/tokens

### Command 5: Verify on GitHub

```bash
# Just check your browser at:
# https://github.com/YOUR_USERNAME/Parkinson-Project
```

Should show your files!

---

## 📋 COMMAND REFERENCE

### One-Time Setup (First Time Only)
```bash
# Navigate to project
cd "C:\Users\chopr\Downloads\Parkinson-Project-main\Parkinson-Project-main"

# Initialize
git init
git lfs install
git lfs track "*.keras"
git add .gitattributes

# First commit
git add .
git commit -m "Initial commit: Parkinson's Detection AI system"

# Connect to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/Parkinson-Project.git
git branch -M main

# Push
git push -u origin main
```

### Daily Workflow (Every Time You Make Changes)
```bash
# Check what changed
git status

# Stage changes
git add .

# Commit
git commit -m "What you changed"

# Push to GitHub
git push
```

### Or One-Liner:
```bash
git add . && git commit -m "Your message" && git push
```

---

## 🔍 VERIFICATION STEPS

After you run all commands, verify each step:

### ✅ Step 1: Git Initialized?
```bash
git status
# Should NOT say: "fatal: not a git repository"
```

### ✅ Step 2: Files Committed?
```bash
git log --oneline
# Should show: "xxxxx Initial commit: Parkinson's Detection AI system"
```

### ✅ Step 3: LFS Working?
```bash
git lfs ls-files
# Should show: "model/parkinsons_detector.keras (oid sha256:...)"
```

### ✅ Step 4: Remote Connected?
```bash
git remote -v
# Should show:
# origin  https://github.com/YOUR_USERNAME/Parkinson-Project.git (fetch)
# origin  https://github.com/YOUR_USERNAME/Parkinson-Project.git (push)
```

### ✅ Step 5: On GitHub?
```
Visit: https://github.com/YOUR_USERNAME/Parkinson-Project
Should show your files (backend/, frontend/, model/, etc.)
```

---

## 🆘 TROUBLESHOOTING

### ❌ "fatal: not a git repository"
```bash
git init
```

### ❌ "git lfs version" command not found
**Install Git LFS:**
- Windows: https://git-lfs.github.com (download installer)
- Mac: `brew install git-lfs`
- Linux: `sudo apt-get install git-lfs`

### ❌ "Permission denied" when pushing
**Use personal access token instead of password:**
1. Go to https://github.com/settings/tokens
2. Create new token
3. When Git asks for password, paste the token

### ❌ "Could not resolve host"
- Check your internet connection
- Verify GitHub is not blocked by firewall

### ❌ "Already exists" when pushing
```bash
# Remote already added, try:
git push
```

---

## 📊 WHAT GETS UPLOADED

### ✅ These WILL be on GitHub:
```
backend/
  ├── main.py
  ├── models.py
  ├── database.py
  └── requirements.txt
frontend/
  ├── app.py
  └── requirements.txt
model/
  ├── main.py
  └── parkinsons_detector.keras  ← VIA GIT LFS
dataset/train/...                 ← All images
dataset/test/...                  ← All images
README.md
DEPLOYMENT.md
etc.
```

### ❌ These will NOT be uploaded (ignored):
```
venv/                 ← Virtual env
.env                  ← Secrets
*.db                  ← Database
__pycache__/          ← Python cache
.idea/, .vscode/      ← IDE files
```

---

## 🎯 QUICK START (Copy-Paste Everything Below)

```bash
# ==========================================
# STEP 1: Initialize Git & LFS
# ==========================================
cd "C:\Users\chopr\Downloads\Parkinson-Project-main\Parkinson-Project-main"
git init
git lfs install
git lfs track "*.keras"
git add .gitattributes

# ==========================================
# STEP 2: Create & Commit
# ==========================================
git add .
git commit -m "Initial commit: Parkinson's Detection AI system"

# ==========================================
# STEP 3: Verify (Should all show output)
# ==========================================
git status
git log --oneline
git lfs ls-files

# ==========================================
# STEP 4: Connect to GitHub
# (Replace YOUR_USERNAME with your GitHub username)
# ==========================================
git remote add origin https://github.com/YOUR_USERNAME/Parkinson-Project.git
git branch -M main

# ==========================================
# STEP 5: Push to GitHub
# (When asked for password: use personal access token from https://github.com/settings/tokens)
# ==========================================
git push -u origin main

# ==========================================
# STEP 6: Verify on GitHub
# Visit: https://github.com/YOUR_USERNAME/Parkinson-Project
# ==========================================
```

---

## 🔑 Getting Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Give it a name: "Git Local"
4. Check: `repo` (full control of private repositories)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)
7. When Git asks for password: Paste this token

---

## 📝 AFTER SETUP - MAKING CHANGES

Each time you modify code:

```bash
# 1. See what changed
git status

# 2. Stage changes
git add .

# 3. Commit with message
git commit -m "Fixed bug in backend"

# 4. Push to GitHub
git push

# Done! Check GitHub to verify
```

---

## ✨ YOU'RE DONE!

Your project is now on GitHub! 

**Next steps:**
1. Share your GitHub link: `https://github.com/YOUR_USERNAME/Parkinson-Project`
2. Deploy to Streamlit Cloud (see STREAMLIT_DEPLOYMENT.md Step 10)
3. Invite collaborators (if team project)

---

## 📚 Need More Help?

- **Full Git guide:** See [GIT_SETUP.md](GIT_SETUP.md)
- **Quick reference:** See [GIT_QUICK_REFERENCE.md](GIT_QUICK_REFERENCE.md)
- **Git docs:** https://git-scm.com/docs
- **GitHub help:** https://docs.github.com

---

**Just follow the "QUICK START" section above and you'll be done in 5 minutes!** ✨
