# create_admin.py - Script to create an admin user
from backend.database import SessionLocal, engine
from backend import models
from passlib.context import CryptContext
import sys

# Setup Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create tables
models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

def create_super_admin(username="admin", password="admin123"):
    """Create a super admin user for the system"""
    try:
        # Check if admin exists
        existing = db.query(models.User).filter(models.User.username == username).first()
        if existing:
            print(f"⚠️ Admin user '{username}' already exists!")
            return False

        # Create Admin
        hashed_pw = pwd_context.hash(password)
        admin_user = models.User(
            username=username,
            password_hash=hashed_pw,
            role="admin"
        )

        db.add(admin_user)
        db.commit()
        print(f"✅ Success! Admin created.")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        print(f"⚠️ IMPORTANT: Change this password after first login!")
        return True
    except Exception as e:
        print(f"❌ Error creating admin: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        username = sys.argv[1]
        password = sys.argv[2]
        create_super_admin(username, password)
    else:
        # Default admin
        create_super_admin()