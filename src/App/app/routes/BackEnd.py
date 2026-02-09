from flask import Flask, request, jsonify, Blueprint
import os
from app.models import File
from app import SessionLocal

bp = Blueprint('back_end', __name__)

@bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    file_type = request.form.get('file_type')

    if not file or not file.filename.endswith(".bag"):
        return jsonify({'error': 'Invalid file type. Please upload a .bag file.'}), 400
    if not file_type or file_type not in ["RGB-D", "Depth"]:
        return jsonify({'error': 'Invalid file type. Please upload a RGB-D or Depth file.'}), 400

    upload_dir = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)

    try:
        db = SessionLocal()
        new_file = File(
            file_name=file.filename,
            file_type=file_type,
            file_path=file_path
        )
        db.add(new_file)
        db.commit()
        db.refresh(new_file)

        return jsonify({"message": "File successfully uploaded", "file_id": new_file.file_id})

    except Exception as e:
        return jsonify({'error': f'Failed to upload file: {str(e)}'}), 500

    finally:
        db.close()