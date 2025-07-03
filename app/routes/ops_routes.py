from flask import Blueprint, request, jsonify
from app import mongo
import os
from werkzeug.utils import secure_filename
import gridfs

ALLOWED_EXTENSIONS = {'docx', 'xlsx', 'pptx'}
ops_bp = Blueprint("ops", __name__, url_prefix="/ops")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ops_bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file or not allowed_file(file.filename):
        return jsonify({"message": "File not allowed"}), 400

    fs = gridfs.GridFS(mongo.db)
    fs_id = fs.put(file.read(), filename=file.filename)
    return jsonify({"message": "File uploaded", "file_id": str(fs_id)}), 201
