# backend/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status, Form, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from . import models, database
import tensorflow as tf
import os
from typing import Optional
from dotenv import load_dotenv
import keras

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "parkinsons_detector.h5")

CLASSES = ["Healthy", "Parkinson"]
SECRET_KEY = os.getenv("SECRET_KEY", "my_super_secret_key_for_final_year_project")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="Parkinson Detection API", description="AI-powered Parkinson's disease detection system")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific URLs in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
model = None


# --- HELPERS ---
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_user_optional(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Optional authentication - allows guest access if token is missing"""
    if token is None:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    user = db.query(models.User).filter(models.User.username == username).first()
    return user


def validate_spiral_image(image_rgb: np.ndarray) -> bool:
    """
    Validate that the uploaded image appears to be a spiral/wave test image.
    Checks for sufficient edge content (handwriting characteristic).
    Returns True if image looks like a valid test, False otherwise.
    """
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        
        # Detect edges using Canny
        edges = cv2.Canny(gray, 50, 150)
        
        # Calculate edge density
        edge_density = np.sum(edges > 0) / edges.size
        
        # Valid spiral/wave images should have edge density between 2% and 50%
        # Too low = blank image, too high = noise/artifact
        is_valid = 0.02 <= edge_density <= 0.50
        
        if not is_valid:
            print(f"[WARNING] Image edge density ({edge_density:.2%}) outside valid range. Likely not a spiral test image.")
        
        return is_valid
    except Exception as e:
        print(f"[WARNING] Could not validate image: {e}")
        return False


@app.on_event("startup")
def load_ai_model():
    global model
    try:
        if not os.path.exists(MODEL_PATH):
            print(f"[ERROR] Model not found at {MODEL_PATH}")
            print(f"[ERROR] Please train the model using model/main.py before starting the server.")
            model = None
            return
        
        try:
            model = tf.keras.models.load_model(MODEL_PATH)
            print(f"[INFO] Model loaded successfully from {MODEL_PATH}")
        except Exception as load_error:
            print(f"[ERROR] Could not load model from file: {load_error}")
            print(f"[ERROR] Please ensure the model file is valid and re-train if necessary.")
            model = None
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        model = None


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "model_loaded": model is not None}


# --- AUTH ROUTES ---

# In backend/main.py

@app.post("/register")
def register_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # ✅ TC1 SECURITY FIX: bcrypt 72-byte safe handling
    # raw_password = form_data.password
    # safe_password = raw_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")

    # hashed_password = pwd_context.hash(safe_password)

    hashed_password = pwd_context.hash(form_data.password)


    new_user = models.User(
        username=form_data.username,
        password_hash=hashed_password,
        role="doctor"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}



@app.post("/token")
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    # raw_password = form_data.password
    # safe_password = raw_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")

    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role
    }



# --- DOCTOR ROUTES ---

@app.get("/history")
def get_prediction_history(current_user: models.User = Depends(get_current_user)):
    """Get prediction history for authenticated user"""
    predictions = current_user.predictions
    return [{
        "id": p.id, 
        "patient_name": p.patient_name, 
        "patient_age": p.patient_age, 
        "label": p.label, 
        "confidence": p.confidence,
        "created_at": p.created_at
    } for p in predictions]


@app.post("/predict")
async def predict(
        patient_name: str = Form(...),
        patient_age: int = Form(...),
        file: UploadFile = File(...),
        current_user: Optional[models.User] = Depends(get_current_user_optional),
        db: Session = Depends(get_db)
):
    """Make predictions - works for both authenticated and guest users"""
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Model not trained or loaded. Please train the model using model/main.py first."
        )
    
    try:
        # 1. Load and decode image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file. Please upload a valid image.")
        
        # 2. Validate it's a spiral/wave test image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if not validate_spiral_image(image):
            raise HTTPException(
                status_code=400, 
                detail="Image does not appear to be a valid Parkinson's test (spiral/wave). Please upload a clear test image."
            )
        
        # 3. Preprocess for model
        image = cv2.resize(image, (224, 224))
        image = image.astype("float32") / 255.0
        image = np.expand_dims(image, axis=0)

        # 4. Get predictions
        preds = model.predict(image)
        idx = np.argmax(preds, axis=1)[0]
        label = CLASSES[idx]
        
        # Get confidences for both classes
        healthy_conf = float(preds[0][0] * 100)  # Healthy confidence
        parkinson_conf = float(preds[0][1] * 100)  # Parkinson's confidence
        predicted_conf = float(preds[0][idx] * 100)  # Predicted class confidence
        
        # Round to 2 decimal places
        healthy_conf = round(healthy_conf, 2)
        parkinson_conf = round(parkinson_conf, 2)
        predicted_conf = round(predicted_conf, 2)

        # 5. Save to database if authenticated
        if current_user:
            db_record = models.Prediction(
                user_id=current_user.id,
                patient_name=patient_name,
                patient_age=patient_age,
                filename=file.filename,
                label=label,
                confidence=predicted_conf
            )
            db.add(db_record)
            db.commit()
        
        # 6. Return comprehensive response with dual confidences
        return {
            "patient": patient_name,
            "prediction": label,
            "confidence": predicted_conf,
            "healthy_confidence": healthy_conf,
            "parkinson_confidence": parkinson_conf,
            "model_ready": True
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# --- NEW ADMIN ROUTES ---

@app.get("/admin/stats")
def get_system_stats(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if user is actually an admin
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized. Admin access required.")

    # Calculate Stats
    total_users = db.query(models.User).count()
    total_predictions = db.query(models.Prediction).count()
    parkinson_count = db.query(models.Prediction).filter(models.Prediction.label == "Parkinson").count()
    healthy_count = db.query(models.Prediction).filter(models.Prediction.label == "Healthy").count()

    return {
        "total_users": total_users,
        "total_predictions": total_predictions,
        "parkinson_cases": parkinson_count,
        "healthy_cases": healthy_count
    }