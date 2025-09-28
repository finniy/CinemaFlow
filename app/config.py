import os
import json
from dotenv import load_dotenv

load_dotenv()

ADMINS = json.loads(os.getenv("ADMINS"))
SECRET_KEY_ADMIN = os.getenv("SECRET_KEY_ADMIN")
SECRET_KEY_USER = os.getenv("SECRET_KEY_USER")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES"))
