from flask_mail import Message
from app import mail

def send_verification_email(user_email, token):
    msg = Message("Verify your Email", sender="noreply@file.com", recipients=[user_email])
    msg.body = f"Click this link to verify: http://localhost:5000/auth/verify/{token}"
    mail.send(msg)
