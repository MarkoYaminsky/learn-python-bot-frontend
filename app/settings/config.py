from os import getenv

from dotenv import load_dotenv

load_dotenv()

MY_USER_ID = getenv("MY_USER_ID")

API_KEY = getenv("API_KEY")

ADMINS = list(map(int, [MY_USER_ID]))

SERVER_URL = getenv("SERVER_URL")

GOOGLE_DISC = getenv("GOOGLE_DISC")
