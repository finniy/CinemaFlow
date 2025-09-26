import os
import json
from dotenv import load_dotenv

load_dotenv()
ADMINS = json.loads(os.getenv("ADMINS"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES"))