import os
import json
from dotenv import load_dotenv

load_dotenv()
ADMINS = json.loads(os.getenv("ADMINS"))