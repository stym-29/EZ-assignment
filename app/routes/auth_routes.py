from flask import Blueprint, request, jsonify
from app.models.user_model import insert_user, find_user_by_email
from app.utils.encryption import generate_secure_token
from app.utils.email_utils import send_verification_email
import bcrypt

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data['email']
    password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
    role = "client"

    token = generate_secure_token(email)
    user = {"email": email, "password": password, "role": role, "verified": False}
    insert_user(user)
    send_verification_email(email, token)

    return jsonify({"encrypted-url": f"/auth/verify/{token}"}), 201

@auth_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    from app.utils.encryption import verify_secure_token
    try:
        email = verify_secure_token(token)
        mongo.db.users.update_one({"email": email}, {"$set": {"verified": True}})
        return jsonify({"message": "Email Verified"}), 200
    except Exception:
        return jsonify({"message": "Invalid or Expired Link"}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = find_user_by_email(data['email'])

    if user and bcrypt.checkpw(data['password'].encode(), user['password']):
        return jsonify({"message": "Login successful", "role": user['role']}), 200
    return jsonify({"message": "Invalid credentials"}), 401
