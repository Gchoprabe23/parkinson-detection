# ⚡ Git Commands - Quick Reference

> Essential git commands for Parkinson's Detection AI

---

## 🎯 TL;DR - Commands to Run RIGHT NOW

### Step 1: Install Git LFS (One time)

**Windows:**
```bash
choco install git-lfs
# OR download from: https://git-lfs.github.com
```

**Mac:**
```bash
brew install git-lfs
```

**Linux:**
```bash
sudo apt-get install git-lfs
```

### Step 2: Initialize Git & LFS

```bash
# Navigate to project
cd "C:\Users\chopr\Downloads\Parkinson-Project-main\Parkinson-Project-main"

# Initialize git
git init

# Initialize LFS
git lfs install

# Track large files
git lfs track "*.keras"
git add .gitattributes
```

### Step 3: First Commit

```bash
# Stage all files (respects .gitignore)
git add .

# Commit
git commit -m "Initial commit: Parkinson's Detection AI system"

# Verify
git status
```

### Step 4: Connect to GitHub & Push

```bash
# 1. Create empty repo on GitHub.com (don't add README)
# 2. Add remote (replace YOUR_USERNAME/REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/Parkinson-Project.git

# 3. Rename branch to main
git branch -M main

# 4. Push to GitHub
git push -u origin main
# On first push, you'll be asked for GitHub credentials (use personal access token)
```

---

## 📋 Git Commands by Task

### Status & Info
```bash
git status              # What changed?
git log --oneline       # Commit history
git remote -v           # Show GitHub connection
git lfs ls-files        # Show LFS tracked files
```

### Making Changes & Pushing
```bash
git add .               # Stage all changes
git commit -m "msg"     # Commit with message
git push                # Push to GitHub
git pull                # Get latest from GitHub
```

### Branches
```bash
git branch              # List branches
git checkout -b name    # Create new branch
git checkout main       # Switch to main
git merge branch-name   # Merge into current
git branch -d name      # Delete branch
```

### Undo Changes
```bash
git restore file.py     # Undo changes to file
git reset HEAD~1        # Undo last commit (keep files)
git reset --hard HEAD~1 # Delete last commit completely
```

---

## ⚡ One-Line Commit

```bash
git add . && git commit -m "Your message" && git push
```

---

## 🔍 Verify Everything Worked

After `git push`:

1. **Check GitHub:**
   ```
   https://github.com/YOUR_USERNAME/Parkinson-Project
   ```
   Should show your code files

2. **Verify LFS tracking:**
   ```bash
   git lfs ls-files
   ```
   Should show: `*.keras (LFS pointer)`

3. **Check nothing sensitive was pushed:**
   - ❌ No venv/ folder
   - ❌ No .env file
   - ❌ No *.db files

---

## 🚀 Daily Workflow (After Setup)

```bash
# Check what changed
git status

# Stage changes
git add .

# Commit
git commit -m "What did you change?"

# Push to GitHub
git push
```

---

## 📊 Files to Commit ✅ vs Ignore ❌

### ✅ COMMIT THESE:
- frontend/app.py
- backend/main.py
- model/main.py
- model/parkinsons_detector.keras (via LFS)
- requirements.txt
- README.md
- Documentation files
- .gitignore
- docker-compose.yml
- Dockerfile

### ❌ DON'T COMMIT THESE:
- venv/ (virtual environment)
- .env (sensitive variables)
- *.db (database files)
- __pycache__/ (Python cache)
- .idea/, .vscode/ (IDE files)
- temp*.jpg (temp files)

---

## 🆘 Quick Troubleshooting

### "fatal: not a git repository"
```bash
git init
```

### "Git LFS not working"
```bash
git lfs install
git lfs track "*.keras"
```

### "Permission denied when pushing"
```bash
# Use GitHub personal access token as password
# Get it from: https://github.com/settings/tokens
```

### "Large file rejected"
```bash
# Make sure it's tracked with LFS
git lfs track "*.keras"
git add .gitattributes
git push
```

---

## 🔐 GitHub Authentication Setup (One Time)

### Option A: Personal Access Token (Easier)

1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scope: `repo`
4. Copy the token
5. When Git asks for password: **paste the token** (not your password)

### Option B: SSH (More Secure)

```bash
# Generate key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub:
# 1. Go to https://github.com/settings/keys
# 2. Paste your public key (~/.ssh/id_ed25519.pub)

# Use SSH for clone/push
git remote set-url origin git@github.com:USERNAME/REPO.git
```

---

## 📝 Commit Message Tips

**Good commit messages:**
```bash
git commit -m "Add dual confidence score display"
git commit -m "Fix model loading error"
git commit -m "Update deployment documentation"
```

**Bad commit messages:**
```bash
git commit -m "fix"
git commit -m "stuff"
git commit -m "asdfgh"
```

---

## 🎯 Complete Setup Sequence

Copy and paste these in order:

```bash
# 1. Install Git LFS (do once per machine)
# Windows: choco install git-lfs
# Mac: brew install git-lfs
# Linux: sudo apt-get install git-lfs

# 2. Navigate to project
cd "C:\Users\chopr\Downloads\Parkinson-Project-main\Parkinson-Project-main"

# 3. Initialize
git init
git lfs install
git lfs track "*.keras"
git add .gitattributes

# 4. First commit
git add .
git commit -m "Initial commit: Parkinson's Detection AI"

# 5. Connect to GitHub (REPLACE with your username)
git remote add origin https://github.com/YOUR_USERNAME/Parkinson-Project.git
git branch -M main

# 6. Push
git push -u origin main
```

---

## ✅ After Push Success

Your repo is now on GitHub! Verify:

```bash
# Check remote
git remote -v
# Output: origin  https://github.com/YOUR_USERNAME/Parkinson-Project.git (fetch)
#         origin  https://github.com/YOUR_USERNAME/Parkinson-Project.git (push)

# Check LFS
git lfs ls-files
# Output: model/parkinsons_detector.keras (oid sha256:...)

# View log
git log --oneline
# Output: xxxx123 Initial commit: Parkinson's Detection AI
```

---

## 🔗 Useful Links

- **GitHub:** https://github.com
- **Git LFS:** https://git-lfs.github.com
- **Create Personal Token:** https://github.com/settings/tokens
- **SSH Keys:** https://github.com/settings/keys
- **Git Docs:** https://git-scm.com/docs

---

## 📚 Full Reference

For detailed explanations, see: [GIT_SETUP.md](GIT_SETUP.md)

This quick reference shows you the **essential commands only**.
