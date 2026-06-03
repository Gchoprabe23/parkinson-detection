#!/usr/bin/env python3
"""
startup.py - Application startup script
Initializes database, loads models, and performs pre-flight checks
"""

import os
import sys
from pathlib import Path

def check_model_exists():
    """Check if trained model exists"""
    model_path = os.getenv("MODEL_PATH", "model/parkinsons_detector.keras")
    if not os.path.exists(model_path):
        print(f"⚠️ WARNING: Model not found at {model_path}")
        print("   The application will start but predictions will fail.")
        print("   Run: python model/main.py")
        return False
    print(f"✅ Model found: {model_path}")
    return True

def initialize_database():
    """Initialize database and create tables"""
    try:
        from backend.database import engine
        from backend import models
        
        print("🗄️  Initializing database...")
        models.Base.metadata.create_all(bind=engine)
        print("✅ Database initialized")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        return False

def create_default_admin():
    """Create default admin user if it doesn't exist"""
    try:
        from backend.database import SessionLocal
        from backend import models
        from passlib.context import CryptContext
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        db = SessionLocal()
        
        # Check if admin exists
        admin = db.query(models.User).filter(models.User.role == "admin").first()
        if admin:
            print(f"✅ Admin user exists: {admin.username}")
        else:
            print("⚠️ No admin user found. Run: python create_admin.py")
        
        db.close()
        return True
    except Exception as e:
        print(f"⚠️ Could not check admin user: {str(e)}")
        return True

def check_environment():
    """Check environment configuration"""
    print("📋 Checking environment configuration...")
    
    required_vars = ["SECRET_KEY", "DATABASE_URL"]
    missing = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing.append(var)
        elif var == "SECRET_KEY" and value == "dev-secret-key-change-in-production":
            print(f"⚠️ WARNING: {var} is using default value. Change in production!")
    
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        return False
    
    print("✅ Environment configuration OK")
    return True

def main():
    """Run all startup checks"""
    print("=" * 50)
    print("🚀 Parkinson's Disease Detection AI - Startup")
    print("=" * 50)
    
    checks = [
        ("Environment", check_environment),
        ("Model", check_model_exists),
        ("Database", initialize_database),
        ("Admin User", create_default_admin),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name} check failed: {str(e)}")
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("✅ All checks passed. Application ready!")
        print("=" * 50)
        return 0
    else:
        print("⚠️ Some checks failed. Review above.")
        print("=" * 50)
        return 1

if __name__ == "__main__":
    sys.exit(main())
