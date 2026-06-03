# 🔧 Troubleshooting & Confidence Score Guide

> Solutions for common deployment issues and the confidence score fixes applied.

---

## 🎯 Confidence Score Issues

### Issue: Confidence is very low (~50-60%)

**Cause:** Model not trained properly OR using untrained test model

**Solution:**

1. **Re-train the model:**
   ```bash
   cd model
   python main.py
   ```

2. **Watch for these in the training output:**
   ```
   Training epoch 1/100...
   [... training progress ...]
   
   ==================================================
   [METRICS] Model Evaluation:
   Test Accuracy: 0.8543  ✅ This should be >75%
   
   Classification Report:
   ...
   
   Confusion Matrix:
   [[85  5]
    [ 8 92]]
   ==================================================
   ```

3. **Restart backend** (Ctrl+C and re-run):
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```
   
   **Check for this message:**
   ```
   [INFO] Model loaded successfully from model/parkinsons_detector.keras
   ```

### Issue: Model accuracy very low during training (<70%)

**Possible causes:**
- Dataset too small (need at least 50 images per class)
- Dataset unbalanced (very different number of healthy vs parkinson images)
- Images are corrupted or wrong format
- Images are not actual spiral/wave tests

**Solution:**

1. **Check dataset structure:**
   ```
   dataset/
   ├── train/
   │   ├── healthy/ (count: ?)
   │   └── parkinson/ (count: ?)
   └── test/
       ├── healthy/
       └── parkinson/
   ```

2. **Count images:**
   ```bash
   # Windows:
   dir /s dataset\train\healthy | find /c "File"
   dir /s dataset\train\parkinson | find /c "File"
   
   # Mac/Linux:
   find dataset/train/healthy -type f | wc -l
   find dataset/train/parkinson -type f | wc -l
   ```

3. **Ensure balance:** 
   - Healthy images ≈ Parkinson images
   - Both should be >50 images ideally

4. **Verify image quality:**
   - Open a few images to ensure they're clear
   - Ensure they're actual spiral or wave test drawings
   - Check file sizes (should be 50KB-500KB typically)

---

## 🖼️ Image Validation Issues

### Issue: "Image does not appear to be a valid Parkinson's test"

**Cause:** Image uploaded is not a spiral/wave test

**Solution:**

1. **Use correct image type:**
   - ✅ Spiral drawing test images
   - ✅ Wave drawing test images
   - ❌ Don't use: regular photos, text documents, unrelated drawings

2. **Ensure image quality:**
   - Image should be clear and not blurry
   - Should show complete spiral or wave
   - Black drawings on white background preferred

3. **If validation is too strict:**
   - Edit `backend/main.py` and modify the edge density thresholds:
   ```python
   # Current: 0.02 <= edge_density <= 0.50
   # Make more lenient:
   is_valid = 0.01 <= edge_density <= 0.60
   ```

---

## 🚀 Deployment Issues

### Issue: Backend fails to start

**Symptoms:** `Error binding to 0.0.0.0:8000`

**Solution:**

1. **Port 8000 is in use:**
   ```bash
   # Windows:
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   
   # Mac/Linux:
   lsof -i :8000 | awk 'NR!=1 {print $2}' | xargs kill -9
   ```

2. **Try different port:**
   ```bash
   uvicorn backend.main:app --reload --port 8001
   ```
   Then update frontend `.env` to match:
   ```env
   BACKEND_URL=http://localhost:8001
   ```

### Issue: Frontend can't connect to backend

**Symptoms:** 
- "Cannot connect to server"
- Error messages in Streamlit app

**Troubleshooting:**

1. **Verify backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status":"ok","model_loaded":true}`

2. **Check BACKEND_URL in frontend:**
   ```bash
   # In .env or terminal before running streamlit:
   echo $BACKEND_URL  # Mac/Linux
   echo %BACKEND_URL%  # Windows
   ```
   Should be: `http://localhost:8000`

3. **Check firewall:**
   - Windows Firewall might block connections
   - Add exception for Python/Uvicorn or disable for testing

4. **Network issue:**
   - Try `localhost` vs `127.0.0.1`
   - Check if running on same machine

### Issue: Streamlit frontend doesn't start

**Symptoms:** Error messages about port 8501

**Solution:**

1. **Port 8501 in use:**
   ```bash
   # Windows:
   netstat -ano | findstr :8501
   taskkill /PID <PID> /F
   
   # Mac/Linux:
   lsof -i :8501 | awk 'NR!=1 {print $2}' | xargs kill -9
   ```

2. **Use different port:**
   ```bash
   streamlit run frontend/app.py --server.port 8502
   ```

### Issue: "Model not found" error on startup

**Symptoms:** Backend says "Model not trained or loaded"

**Solution:**

1. **Verify model file exists:**
   ```bash
   ls model/parkinsons_detector.keras  # Mac/Linux
   dir model\parkinsons_detector.keras  # Windows
   ```

2. **If missing, train model:**
   ```bash
   cd model
   python main.py
   ```

3. **Verify file size:**
   - Model should be >100MB
   - If <50MB, training might have failed

4. **Check MODEL_PATH in .env:**
   ```env
   MODEL_PATH=model/parkinsons_detector.keras
   ```

---

## 🗄️ Database Issues

### Issue: "Failed to fetch history" or predictions not saving

**Symptoms:**
- History tab shows error
- Predictions don't appear after analysis

**Solution:**

1. **Verify you're logged in:**
   - Guest mode doesn't save predictions
   - Must be logged in to save history

2. **Check admin user exists:**
   ```bash
   python create_admin.py
   ```

3. **Verify database file:**
   ```bash
   ls parkinsons.db  # Mac/Linux
   dir parkinsons.db  # Windows
   ```

4. **Reset database (if corrupted):**
   ```bash
   # WARNING: This deletes all predictions!
   rm parkinsons.db  # Mac/Linux
   del parkinsons.db  # Windows
   
   # Restart backend
   uvicorn backend.main:app --reload --port 8000
   ```

### Issue: Permission denied for database

**Solution:**
```bash
# Change permissions (Mac/Linux)
chmod 666 parkinsons.db
chmod 755 .

# Or just re-create:
rm parkingsons.db
# Restart backend to auto-create new one
```

---

## 🔐 Authentication Issues

### Issue: "Incorrect username or password"

**Solution:**

1. **Verify credentials:**
   - Username: `admin`
   - Password: `admin123` (default)

2. **Check admin user exists:**
   ```bash
   python create_admin.py admin admin123
   ```

3. **Clear and retry:**
   ```bash
   rm parkinsons.db
   python create_admin.py admin admin123
   ```

### Issue: Login redirects to registration instead of dashboard

**Solution:**
1. Ensure admin user is created: `python create_admin.py`
2. Clear browser cache (Ctrl+Shift+Delete)
3. Close and reopen frontend

---

## 📊 Confidence Score Debug

### Check what the model is actually outputting

**Add debug code to `backend/main.py`:**

```python
# In the /predict endpoint, after preds = model.predict(image):

print(f"DEBUG - Raw model output shape: {preds.shape}")
print(f"DEBUG - Probabilities: Healthy={preds[0][0]}, Parkinson={preds[0][1]}")
print(f"DEBUG - Softmax sum: {np.sum(preds[0])}")
print(f"DEBUG - Predicted class index: {idx}")
print(f"DEBUG - Predicted confidence: {predicted_conf}%")
```

**Expected output (good model):**
```
DEBUG - Raw model output shape: (1, 2)
DEBUG - Probabilities: Healthy=0.9547, Parkinson=0.0453
DEBUG - Softmax sum: 1.0
DEBUG - Predicted class index: 0
DEBUG - Predicted confidence: 95.47%
```

**Bad output (untrained model):**
```
DEBUG - Raw model output shape: (1, 2)
DEBUG - Probabilities: Healthy=0.5234, Parkinson=0.4766
DEBUG - Softmax sum: 1.0
DEBUG - Predicted class index: 0
DEBUG - Predicted confidence: 52.34%
```

---

## ✅ Verification Checklist

After deployment, verify everything works:

- [ ] Backend runs without errors: `uvicorn backend.main:app --reload --port 8000`
- [ ] Model loaded message appears in backend terminal
- [ ] Frontend runs: `streamlit run frontend/app.py`
- [ ] Visit http://localhost:8501 and see interface
- [ ] Guest mode prediction works
- [ ] Login/registration works
- [ ] Predictions have >80% confidence
- [ ] Detailed analysis shows both class confidences
- [ ] Logged-in predictions save to history
- [ ] Admin dashboard displays stats
- [ ] API docs work: http://localhost:8000/docs

---

## 🐛 Enable Debug Logging

To see more detailed error messages:

**For backend:**
```bash
uvicorn backend.main:app --reload --port 8000 --log-level debug
```

**For frontend:**
```bash
streamlit run frontend/app.py --logger.level=debug
```

---

## 📞 Get More Help

1. **Check existing docs:**
   - [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) - Full deployment guide
   - [FIXES_APPLIED.md](FIXES_APPLIED.md) - What was fixed
   - [DEPLOYMENT.md](DEPLOYMENT.md) - General deployment info

2. **Check logs:**
   - Backend terminal: Shows model loading and API errors
   - Frontend terminal: Shows Streamlit errors
   - Browser console: Press F12, check Console tab

3. **Common fixes:**
   - Restart both backend and frontend
   - Clear browser cache (Ctrl+Shift+Delete)
   - Delete `.streamlit` folder: `rm -rf ~/.streamlit`
   - Re-create virtual environment if packages broken

---

**Still stuck?** Review the full deployment guide or check the error message carefully - it usually indicates the exact problem!
