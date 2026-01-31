from sqlalchemy.orm import Session

from app.core.database import SessionLocal, engine
from app.models.user import User
from app.core import security

def init_db(db: Session) -> None:
    # Check if demo user exists
    user = db.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        user = User(
            email="admin@example.com",
            hashed_password=security.get_password_hash("password"),
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print("Demo user created")
    else:
        print("Demo user already exists")

def main() -> None:
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
