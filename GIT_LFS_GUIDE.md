# 🎯 Git LFS & Large Files - Summary

> Everything you need to know about handling large files in your project

---

## ❓ Do You NEED Git LFS?

### Short Answer: **YES** ✅

Your project has files **too large for regular Git:**

| File | Size | Status | Action |
|------|------|--------|--------|
| `model/parkinsons_detector.keras` | ~200-300MB | **EXCEEDS LIMIT** ✅ Use LFS |
| `dataset/train/healthy/*.jpg` | ~50-100KB each | Within limit | OK without LFS |
| `dataset/test/parkinson/*.jpg` | ~50-100KB each | Within limit | OK without LFS |
| `temp*.jpg` | ~1-2MB | Within limit | Ignored anyway |

**GitHub's hard limit:** 100MB per file
**GitHub's recommended max:** 50MB per file

Your `.keras` file is **2-6x too large** for regular Git!

---

## 🚨 What Happens Without Git LFS?

### ❌ Without Git LFS:
```
$ git push

remote: error: File is too large. This exceeds GitHub's file size
limit of 100 MB

remote: error: Use Git Large File Storage to handle this file.
```

**Result:** Push fails, code doesn't go to GitHub

### ✅ With Git LFS:
```
$ git push

Uploading LFS objects: 100% (1/1), 250 MB | 0 B/s, done.
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**Result:** Everything works, model uploaded

---

## 🔧 How Git LFS Works

### What is Git LFS?

Git LFS = Git Large File Storage

Instead of storing the actual large file, Git stores a **pointer file** (small text file):

```
version https://git-lfs.github.com/spec/v1
oid sha256:f2cc1dac8a5a86d926a3c17fa6e00e6c0f8c5d9e2c1b3a4f5d6c7e8b9a0f1c2
size 250000000
```

**Benefits:**
- ✅ Fast git clone (small pointer, not huge files)
- ✅ Saves bandwidth
- ✅ Allows >100MB files
- ✅ Transparent to user (looks like normal file)

---

## 📥 Installation

### Check if Already Installed:
```bash
git lfs version
# If you see version number: ✅ Installed
# If "command not found": ❌ Not installed
```

### Install Git LFS:

**Windows:**
```bash
# Option 1: Chocolatey (if you have it)
choco install git-lfs

# Option 2: Download installer
# Visit: https://git-lfs.github.com
# Download .exe and run
```

**Mac:**
```bash
brew install git-lfs
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install git-lfs

# Fedora
sudo dnf install git-lfs

# Red Hat
sudo yum install git-lfs
```

### Verify Installation:
```bash
git lfs version
# Should output: git-lfs/3.x.x (hash) ... 
```

---

## 🎯 Using Git LFS in Your Project

### Step 1: Initialize LFS
```bash
git lfs install
```

This sets up Git LFS in your repository (one time only).

### Step 2: Track File Types
```bash
# Track all .keras files
git lfs track "*.keras"

# Track image files (optional)
git lfs track "dataset/**/*.jpg"
git lfs track "dataset/**/*.png"
```

This creates `.gitattributes` file:
```
*.keras filter=lfs diff=lfs merge=lfs -text
dataset/**/*.jpg filter=lfs diff=lfs merge=lfs -text
dataset/**/*.png filter=lfs diff=lfs merge=lfs -text
```

### Step 3: Add .gitattributes
```bash
git add .gitattributes
git commit -m "Configure Git LFS for large files"
```

### Step 4: Track Your Large Files
```bash
git add model/parkinsons_detector.keras
git commit -m "Add trained model"
git push
```

### Verify LFS Tracking:
```bash
git lfs ls-files
# Output: model/parkinsons_detector.keras (oid sha256:... size 250M)
```

---

## 📊 Your Project File Sizes

### Estimated Sizes:

```
model/
├── parkinsons_detector.keras    ~250MB    ← NEEDS LFS ✅
├── main.py                      ~50KB
└── plot.png                     ~500KB

dataset/
├── train/
│   ├── healthy/ (50-100 images)  ~5-10MB
│   └── parkinson/ (50-100 images) ~5-10MB
└── test/
    ├── healthy/                ~2-5MB
    └── parkinson/              ~2-5MB

backend/
├── main.py                      ~30KB
├── models.py                    ~10KB
├── database.py                  ~5KB
└── requirements.txt             ~1KB

frontend/
├── app.py                       ~50KB
└── requirements.txt             ~1KB
```

**Total with LFS:** ~250MB (mostly model)
**Total without LFS:** Would fail (model >100MB)

---

## ✅ Git LFS Workflow

### First Time Setup:
```bash
git init
git lfs install
git lfs track "*.keras"
git add .gitattributes
git add .
git commit -m "Initial commit with LFS"
git remote add origin <url>
git push -u origin main
```

### Daily Work:
```bash
git add .
git commit -m "message"
git push
# LFS handles large files automatically
```

### No extra steps needed! LFS is transparent.

---

## 🔍 How to Verify LFS is Working

### Check Files Tracked:
```bash
git lfs ls-files
# Output example:
# model/parkinsons_detector.keras (oid sha256:abc123... size 250M)
```

### Check LFS Status:
```bash
git lfs status
# Output: On branch main
#         LFS objects to be committed: 1
```

### After Push, Verify on GitHub:
```
Visit: https://github.com/YOUR_USERNAME/Parkinson-Project
Click on: model/parkinsons_detector.keras
Should say: "This file is stored with Git LFS"
```

---

## 🚨 Common Issues with LFS

### Issue: "Git LFS is not installed"
**Solution:**
```bash
# Install Git LFS first
# Then: git lfs install
```

### Issue: "Large file rejected"
**Solution:**
```bash
# Make sure it's tracked with LFS
git lfs track "*.keras"
git add .gitattributes
git commit -m "Add LFS tracking"
git push
```

### Issue: "Still getting file size error"
**Solution:**
```bash
# Remove from git cache first
git rm --cached model/parkinsons_detector.keras
git add .gitattributes
git add model/parkinsons_detector.keras
git commit -m "Add model with LFS"
git push
```

### Issue: ".gitattributes not created"
**Solution:**
```bash
git lfs track "*.keras"
# This should create .gitattributes
cat .gitattributes  # Verify it exists
git add .gitattributes
```

---

## 💾 GitHub LFS Storage Limits

### Free Account:
- **1GB free LFS storage** per repository
- **1GB free LFS bandwidth** per month

Your model (~250MB) uses:
- Storage: 25% of free limit ✅
- Bandwidth: Small % of monthly limit ✅

### If You Exceed:
- You can buy more: $5/month per 100GB
- Or delete old versions: `git lfs prune`

---

## 🎯 What NOT to Track with LFS

### Too Small (Don't Use LFS):
```bash
# NOT needed - files are small
*.py
*.txt
*.md
*.json
docker-compose.yml
Dockerfile
```

### Already Ignored (Don't Track):
```bash
# Already in .gitignore, so no need
venv/
.env
*.db
__pycache__/
```

### Use LFS Only For:
```bash
# Large files that need to be in repo
*.keras       # Model files
*.h5          # Model backups
*.tar.gz      # Compressed datasets (if needed)
*.zip         # Archives
```

---

## 📋 Recommended LFS Setup for Your Project

```bash
# ONLY track these:
git lfs track "*.keras"

# That's it!
# Everything else is small enough
```

**Why?**
- Model files are the only >100MB files
- Dataset images are <100KB each (small enough)
- All code files are <100KB each
- Database files are ignored anyway

---

## ✨ Pro Tips

### Tip 1: Clone Faster (Sparse Checkout)
```bash
# Clone without large files
git clone --depth 1 <url>
```

### Tip 2: Delete Old Large Files
```bash
# Free up LFS storage
git lfs prune
```

### Tip 3: See LFS Usage
```bash
# Check LFS bandwidth usage
# Go to: https://github.com/settings/billing
```

---

## 🔄 Git LFS vs Alternative Solutions

| Solution | Pros | Cons | Best For |
|----------|------|------|----------|
| **Git LFS** | ✅ Works with GitHub | ❌ Need to install | **This project** |
| **Git Submodules** | ✅ Flexible | ❌ Complex | Large team projects |
| **Separate Storage** | ✅ Unlimited | ❌ Manual process | Data science |
| **.gitignore** | ✅ Simple | ❌ Can't share files | Local only |

**Recommendation:** Use Git LFS (simplest for your project)

---

## 📚 Quick Reference

```bash
# Install
git lfs install

# Track files
git lfs track "*.keras"

# Verify
git lfs ls-files

# Status
git lfs status

# Clean up
git lfs prune

# Check what's tracked
cat .gitattributes
```

---

## ✅ Before You Push to GitHub

Checklist:

- [ ] Git LFS installed: `git lfs version` works
- [ ] LFS initialized: `git lfs install` run
- [ ] Files tracked: `*.keras` tracked
- [ ] .gitattributes exists: `git add .gitattributes`
- [ ] Model file exists: `model/parkinsons_detector.keras` (>100MB)
- [ ] All staged: `git add .`
- [ ] Committed: `git commit -m "..."`
- [ ] Remote added: `git remote add origin ...`
- [ ] Ready to push: `git push -u origin main`

---

## 🎯 Next Steps

1. **Install Git LFS:**
   ```bash
   # Windows: choco install git-lfs
   # Mac: brew install git-lfs
   # Linux: sudo apt-get install git-lfs
   ```

2. **Follow [GIT_COPYPASTE.md](GIT_COPYPASTE.md):**
   - Copy-paste commands in order
   - Push to GitHub
   - Done!

3. **Verify on GitHub:**
   - Visit your repo
   - Check `model/parkinsons_detector.keras`
   - Should say "This file is stored with Git LFS"

---

## 🚀 Ready?

**Next:** Go to [GIT_COPYPASTE.md](GIT_COPYPASTE.md) and start pushing!

**Questions?** See [GIT_SETUP.md](GIT_SETUP.md) for detailed explanations.

---

**Key Takeaway:** ✅ Yes, you NEED Git LFS. Install it and follow [GIT_COPYPASTE.md](GIT_COPYPASTE.md) - that's it!
