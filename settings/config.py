from os import getenv

from dotenv import load_dotenv

load_dotenv()

MY_USER_ID = getenv('MY_USER_ID')

API_KEY = getenv('API_KEY')

ADMINS = map(int, [MY_USER_ID])

SERVER_URL = 'http://localhost:8000/graphql/'
