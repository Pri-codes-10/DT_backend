# app/utils/reset_utils.py
from itsdangerous import URLSafeTimedSerializer
import os

SECRET_KEY = "your-secret"
serializer = URLSafeTimedSerializer(SECRET_KEY)

def generate_reset_token(email):
    return serializer.dumps(email)

def verify_reset_token(token, max_age=3600):
    try:
        email = serializer.loads(token, max_age=max_age)
        return email
    except:
        return None