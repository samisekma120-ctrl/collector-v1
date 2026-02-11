import argparse

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User, UserRole


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an admin user (ops script)")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    args = parser.parse_args()

    db = SessionLocal()
    try:
        existing = db.execute(select(User).where(User.email == args.email)).scalar_one_or_none()
        if existing:
            print(f"[INFO] User already exists: {args.email} (role={existing.role})")
            return

        user = User(
            email=args.email,
            hashed_password=hash_password(args.password),
            role=UserRole.admin,
        )
        db.add(user)
        db.commit()
        print(f"[OK] Admin created: {args.email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
