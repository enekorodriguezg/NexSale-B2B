# seed_user.py
from server.core.security import generate_hashed_password, generate_salt
from server.database import SessionLocal
from server.models import User

db = SessionLocal()

username = "admin"
password = "password123"
role = "admin"

# Usar exactamente la misma lógica de hashing del proyecto
salt = generate_salt()
hashed_pw = generate_hashed_password(plain_password=password, salt=salt)

# Comprobar si ya existe para evitar errores de clave única
existing_user = db.query(User).filter(User.username == username).first()

if not existing_user:
  new_user = User(
      username=username, hashed_password=hashed_pw, salt=salt, role=role
  )
  db.add(new_user)
  db.commit()
  print(f"Usuario '{username}' creado correctamente con rol '{role}'.")
else:
  print(f"El usuario '{username}' ya existe.")

db.close()