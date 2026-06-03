# 📑 Git & GitHub Setup - Complete Index

> Navigate all git setup documentation for Parkinson's Detection AI

---

## 🎯 Choose Your Guide

### 🟢 **I Want to Push to GitHub NOW** (5 min)
→ Go to [GIT_COPYPASTE.md](GIT_COPYPASTE.md)
- Just copy-paste commands
- Step-by-step verification
- Done in 5 minutes

### 🟡 **I Want Quick Reference Commands**
→ Go to [GIT_QUICK_REFERENCE.md](GIT_QUICK_REFERENCE.md)
- Common commands organized by task
- Status/Info/Changes/Branches
- Troubleshooting tips

### 🔵 **I Want to Understand Everything**
→ Go to [GIT_SETUP.md](GIT_SETUP.md)
- Full explanations
- Why you need Git LFS
- Authentication options
- Common workflows
- Deployment from GitHub

---

## 📚 Guide Comparison

| Need | Document | Time | Level |
|------|----------|------|-------|
| Just push code | [GIT_COPYPASTE.md](GIT_COPYPASTE.md) | 5 min | Beginner |
| Need quick commands | [GIT_QUICK_REFERENCE.md](GIT_QUICK_REFERENCE.md) | 3 min | Beginner |
| Full setup guide | [GIT_SETUP.md](GIT_SETUP.md) | 15 min | Advanced |
| Just commands | This page | 2 min | Beginner |

---

## ⚡ FASTEST SETUP (Copy-Paste)

```bash
# 1. Install Git LFS (one time)
# Windows: choco install git-lfs
# Mac: brew install git-lfs
# Linux: sudo apt-get install git-lfs

# 2. Navigate to project
cd "C:\Users\chopr\Downloads\Parkinson-Project-main\Parkinson-Project-main"

# 3. Initialize & commit
git init
git lfs install
git lfs track "*.keras"
git add .gitattributes
git add .
git commit -m "Initial commit: Parkinson's Detection AI"

# 4. Connect to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/Parkinson-Project.git
git branch -M main

# 5. Push
git push -u origin main
```

**Total time:** ~5 minutes

For detailed instructions: [GIT_COPYPASTE.md](GIT_COPYPASTE.md)

---

## ✅ Do You Need Git LFS?

**YES** - Your project has:
- ✅ Model file: `parkinsons_detector.keras` (~200-300MB)
- ✅ Large dataset images

**Git LFS is required** for files >100MB

Without it: GitHub will reject your push

---

## 🚀 Quick Command Reference

### Initial Setup (One Time)
```bash
git init                                          # Initialize
git lfs install                                   # Initialize LFS
git lfs track "*.keras"                          # Track model files
git add .                                        # Stage all files
git commit -m "Initial commit"                   # Commit
git remote add origin https://github.com/USER/REPO.git  # Add GitHub
git push -u origin main                          # Push
```

### Daily Workflow (Every Change)
```bash
git add .                                        # Stage changes
git commit -m "Your message"                     # Commit
git push                                         # Push to GitHub
```

### Or One-Liner
```bash
git add . && git commit -m "msg" && git push
```

---

## 📋 Common Tasks

### See Status
```bash
git status                                       # What changed?
git log --oneline                               # Commit history
git remote -v                                    # GitHub connection
git lfs ls-files                                 # LFS tracked files
```

### Create Branch
```bash
git checkout -b feature-name                     # Create new branch
git checkout main                                # Switch to main
git merge feature-name                           # Merge branch
git branch -d feature-name                       # Delete branch
```

### Undo Changes
```bash
git restore file.py                              # Undo changes
git reset HEAD~1                                 # Undo last commit
git reset --hard HEAD~1                          # Delete last commit
```

---

## 🆘 Troubleshooting

### Git not initialized?
```bash
git init
```

### Git LFS not working?
```bash
git lfs install
git lfs track "*.keras"
```

### Permission denied?
- Use personal access token: https://github.com/settings/tokens
- Paste token as password (not your GitHub password)

### Large file rejected?
```bash
git lfs track "*.keras"
git add .gitattributes
git push
```

For more help: [GIT_SETUP.md](GIT_SETUP.md) → Troubleshooting

---

## 🔐 Authentication

### Option 1: Personal Access Token (Recommended)
1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scope: `repo`
4. Copy token
5. When Git asks for password: **paste token** (not password)

### Option 2: SSH (More Secure)
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Add public key to: https://github.com/settings/keys
git remote set-url origin git@github.com:USERNAME/REPO.git
```

---

## 📊 What Gets Uploaded?

### ✅ Uploaded to GitHub:
- backend/ (source code)
- frontend/ (source code)
- model/ (including .keras file via LFS)
- dataset/ (images)
- Documentation files
- docker-compose.yml
- Dockerfile
- All .txt and .md files

### ❌ NOT Uploaded (Ignored):
- venv/ (virtual environment)
- .env (secrets)
- *.db (database)
- __pycache__ (cache)
- .idea/, .vscode/ (IDE)

---

## 🎯 Decision Tree

```
Want to push code to GitHub?
    │
    ├─→ "Just give me commands" 
    │   └─→ [GIT_COPYPASTE.md](GIT_COPYPASTE.md)
    │
    ├─→ "I need help with setup"
    │   └─→ [GIT_SETUP.md](GIT_SETUP.md)
    │
    ├─→ "I want a quick reference"
    │   └─→ [GIT_QUICK_REFERENCE.md](GIT_QUICK_REFERENCE.md)
    │
    └─→ "Something went wrong"
        └─→ See Troubleshooting section below
```

---

## 🔧 Troubleshooting Flowchart

```
Error occurred?
    │
    ├─→ "fatal: not a git repository"
    │   └─→ Run: git init
    │
    ├─→ "git lfs version" not found
    │   └─→ Install Git LFS (see GIT_SETUP.md)
    │
    ├─→ "Permission denied" when pushing
    │   └─→ Use personal access token (see GIT_SETUP.md)
    │
    ├─→ "Large file rejected"
    │   └─→ Track with LFS: git lfs track "*.keras"
    │
    ├─→ "Could not resolve host"
    │   └─→ Check internet connection
    │
    └─→ Other issues
        └─→ See full troubleshooting in [GIT_SETUP.md](GIT_SETUP.md)
```

---

## ✨ Next Steps After Pushing

Once your code is on GitHub:

1. **Share repo link:**
   ```
   https://github.com/YOUR_USERNAME/Parkinson-Project
   ```

2. **Deploy to Streamlit Cloud:**
   - See [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) → Step 10
   - Takes ~2-3 minutes

3. **Invite collaborators:**
   - GitHub → Settings → Collaborators

4. **Set up CI/CD (Optional):**
   - Add GitHub Actions for testing

---

## 📚 Related Guides

| Guide | Purpose |
|-------|---------|
| [GIT_COPYPASTE.md](GIT_COPYPASTE.md) | Copy-paste commands |
| [GIT_QUICK_REFERENCE.md](GIT_QUICK_REFERENCE.md) | Quick reference |
| [GIT_SETUP.md](GIT_SETUP.md) | Full setup guide |
| [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) | Deployment guide |
| [DEPLOYMENT_INDEX.md](DEPLOYMENT_INDEX.md) | Master index |

---

## 🎯 Your Starting Point

### If this is your first time with Git:
1. ✅ Read this page (you're here)
2. ✅ Go to [GIT_COPYPASTE.md](GIT_COPYPASTE.md)
3. ✅ Copy-paste commands
4. ✅ Done!

### If you need reference later:
→ Come back to this page and choose a guide

### If something breaks:
→ Check troubleshooting or visit [GIT_SETUP.md](GIT_SETUP.md)

---

## 📊 Git Commands by Frequency

### Most Common (Use Daily)
```bash
git add .
git commit -m "message"
git push
```

### Common (Use Weekly)
```bash
git status
git log --oneline
git pull
```

### Less Common (Use When Needed)
```bash
git checkout -b branch
git merge branch
git reset
```

### Rare (Special Cases)
```bash
git rebase
git cherry-pick
git stash
```

---

## ✅ Verification Checklist

After running git push:

- [ ] No errors in terminal
- [ ] See output like: "Branch 'main' set up to track..."
- [ ] Can view repo on GitHub: https://github.com/YOUR_USERNAME/Parkinson-Project
- [ ] All source code files visible on GitHub
- [ ] model/parkinsons_detector.keras shows as "LFS pointer"
- [ ] venv/, .env, *.db NOT visible on GitHub

---

## 🚀 You're All Set!

**Your project is now version controlled and on GitHub!**

### Next: Deploy to Streamlit Cloud
See [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) → Step 10

### Or: Continue developing
```bash
# Make changes
git add .
git commit -m "Your message"
git push
```

---

**Questions?** Choose a guide above or check [GIT_SETUP.md](GIT_SETUP.md) for detailed explanations.

**Ready?** Start with [GIT_COPYPASTE.md](GIT_COPYPASTE.md) 🚀
