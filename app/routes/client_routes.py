from flask import Blueprint, jsonify, request, send_file
from app.utils.encryption import generate_secure_token, verify_secure_token
from bson import ObjectId
from app import mongo
import gridfs
import io

client_bp = Blueprint("client", __name__, url_prefix="/client")

@client_bp.route('/list', methods=['GET'])
def list_files():
    files = mongo.db.fs.files.find()
    return jsonify([{"filename": f["filename"], "id": str(f["_id"])} for f in files])

@client_bp.route('/download-link/<file_id>', methods=['GET'])
def get_download_link(file_id):
    token = generate_secure_token(file_id)
    return jsonify({"download-link": f"/client/download/{token}", "message": "success"})

@client_bp.route('/download/<token>', methods=['GET'])
def download_file(token):
    try:
        file_id = verify_secure_token(token)
        fs = gridfs.GridFS(mongo.db)
        file = fs.get(ObjectId(file_id))
        return send_file(io.BytesIO(file.read()), download_name=file.filename, as_attachment=True)
    except Exception:
        return jsonify({"message": "Unauthorized or expired link"}), 403
