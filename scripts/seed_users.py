"""Script para inicializar usuarios de prueba con Salt y Pepper en la base de datos."""

from sqlalchemy import select
from server.core.security import (
    generate_hashed_password,
    generate_salt,
    verify_password,
)
from server.database import SessionLocal
from server.models import User

USERS_TO_SEED = [
    {
        "username": "admin@nexsale.com",
        "plain_password": "AdminPassword123!",
        "role": "admin",
    },
    {
        "username": "commercial@nexsale.com",
        "plain_password": "CommercialPassword123!",
        "role": "commercial",
    },
]


def seed_database():
  db = SessionLocal()
  print("[*] Iniciando el proceso de seeding de usuarios...\n")

  try:
    for user_data in USERS_TO_SEED:
      username = user_data["username"]
      plain_pass = user_data["plain_password"]
      role = user_data["role"]

      # 1. Comprobar si el usuario ya existe para no duplicarlo
      stmt = select(User).where(User.username == username)
      existing_user = db.execute(stmt).scalar_one_or_none()

      # 2. Generar Salt criptográfico individual
      salt = generate_salt()

      # 3. Generar Hash combinando password + salt + PEPPER global
      hashed_pass = generate_hashed_password(plain_pass, salt)

      # 4. Verificación previa de sanidad (Sanity Check)
      is_valid = verify_password(plain_pass, salt, hashed_pass)
      is_invalid_checked = not verify_password(
          "PasswordIncorrecta", salt, hashed_pass
      )

      if not (is_valid and is_invalid_checked):
        raise RuntimeError(
            f"Fallo en la prueba criptográfica para {username}. Abortando."
        )

      if existing_user:
        # Actualizar credenciales si ya existe
        existing_user.hashed_password = hashed_pass #type:ignore
        existing_user.salt = salt #type:ignore
        existing_user.role = role #type:ignore
        print(f"[ACTUALIZADO] Usuario: {username} | Rol: {role}")
      else:
        # Crear nuevo usuario
        new_user = User(
            username=username,
            hashed_password=hashed_pass,
            salt=salt,
            role=role,
        )
        db.add(new_user)
        print(f"[CREADO] Usuario: {username} | Rol: {role}")

      print(f"  -> Sal única (hex 16 bytes): {salt}")
      print(f"  -> Hash SHA-256 (64 chars) : {hashed_pass[:20]}...[recortado]")
      print(f"  -> Verificación interna    : {'OK (Válida)' if is_valid else 'FALLO'}\n")

    db.commit()
    print("[+] Seeding completado y transacciones confirmadas en MySQL.")

  except Exception as e:
    db.rollback()
    print(f"[!] Error durante el proceso: {e}")
  finally:
    db.close()


if __name__ == "__main__":
  seed_database()