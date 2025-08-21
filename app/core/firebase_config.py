from app.core.config import settings
import firebase_admin
from firebase_admin import credentials, auth

if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

def get_firebase_auth():
    return auth

def get_web_api_key() -> str:
    return settings.FIREBASE_WEB_API_KEY