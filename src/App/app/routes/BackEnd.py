import sys

from flask import request, jsonify, Blueprint
import os
from app import SessionLocal
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

bp = Blueprint('back_end', __name__)

@bp.route('/upload', methods=['POST'])
def upload_file():
    logger.info('='*50)
    logger.info("Received file upload request")
    logger.info('=' * 50)
    from app.models import File  # Import inside function to avoid circular import

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

    db = SessionLocal()
    try:
        new_file = File(
            file_name=file.filename,
            file_type=file_type,
            file_path=file_path
        )
        db.add(new_file)
        db.commit()
        db.refresh(new_file)

        return jsonify({"message": "File successfully uploaded", "file_id": new_file.file_id}), 200

    except Exception as e:
        db.rollback()
        return jsonify({'error': f'Failed to upload file: {str(e)}'}), 500

    finally:
        db.close()