"""Creates (or resets) the demo users. Passwords use a rule-based salt and a random pepper (R25)."""

from sqlalchemy import select

from server.core.security import generate_hashed_password, verify_password
from server.database import SessionLocal
from server.models import User

USERS_TO_SEED = [
    {"username": "admin", "plain_password": "admin", "role": "admin"},
    {"username": "user_com", "plain_password": "user_com", "role": "commercial"},
    {"username": "user_ware", "plain_password": "user_ware", "role": "warehouse"},
]


def seed_database():
    db = SessionLocal()
    print("[*] Seeding demo users...")

    try:
        for user_data in USERS_TO_SEED:
            username = user_data["username"]
            plain_pass = user_data["plain_password"]
            role = user_data["role"]

            user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
            if user is None:
                user = User(username = username, role = role, hashed_password = "")
                db.add(user)
                db.flush() #INSERT inside the transaction -> the id exists, so the salt can be derived
                action = "CREATED"
            else:
                user.role = role
                action = "UPDATED"

            user.hashed_password = generate_hashed_password(plain_pass, user.id)

            #Sanity check: the right password verifies, a wrong one does not
            if not verify_password(plain_pass, user.id, user.hashed_password) or verify_password("WrongPassword", user.id, user.hashed_password):
                raise RuntimeError(f"Password hashing check failed for {username}")

            print(f"[{action}] {username} ({role}) -> hash {user.hashed_password[:16]}...")

        db.commit()
        print("[+] Seeding completed.")

    except Exception as e:
        db.rollback()
        print(f"[!] Error while seeding: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()