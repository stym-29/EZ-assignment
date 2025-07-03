from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_secure_token(file_id):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(file_id, salt="file-share")

def verify_secure_token(token, max_age=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.loads(token, salt="file-share", max_age=max_age)
