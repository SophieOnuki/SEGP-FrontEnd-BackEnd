import sys
import os
import logging

from flask import request, jsonify, Blueprint, send_file
from app import SessionLocal

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

bp = Blueprint('back_end', __name__)
media_bp = Blueprint('media', __name__)


@bp.route('/files', methods=['GET'])
def list_files():
    from app.models import File
    db = SessionLocal()
    try:
        files = db.query(File).order_by(File.upload_date.desc()).all()
        return jsonify([
            {
                'file_id': f.file_id,
                'file_name': f.file_name,
                'file_type': f.file_type,
                'file_path': f.file_path,
                'upload_date': f.upload_date.isoformat() if f.upload_date else None,
            }
            for f in files
        ]), 200
    finally:
        db.close()


@media_bp.route('/video/<int:file_id>')
def get_video(file_id):
    from app.models import File
    db = SessionLocal()
    try:
        file_record = db.query(File).filter_by(file_id=file_id).first()
        if not file_record:
            return jsonify({'error': 'File not found'}), 404
        if not file_record.video_path:
            return jsonify({'error': 'No video generated for this file'}), 404
        if not os.path.exists(file_record.video_path):
            logger.error(f"Video missing at {file_record.video_path}")
            return jsonify({'error': 'Video file missing on server'}), 404
        return send_file(file_record.video_path, mimetype='video/mp4')
    finally:
        db.close()


@bp.route('/upload', methods=['POST'])
def upload_file():
    import os

    logger.info('=' * 50)
    logger.info("Received file upload request")
    logger.info('=' * 50)

    from app.models import File, Prediction
    from app.pipeline import run_ffb_prediction

    file = request.files.get('file')
    file_type = request.form.get('file_type')

    logger.debug(f"📁  File object: {file}")
    logger.debug(f"📝 File type selected: {file_type}")
    logger.debug(f"📋 Request form data: {request.form}")
    logger.debug(f"📋 Request files: {request.files}")

    # VALIDATION
    if not file or not file.filename.endswith(".bag"):
        logger.warning(f"✗ Invalid file type. Filename: {file.filename if file else 'None'}")
        return jsonify({'error': 'Invalid file type. Please upload a .bag file.'}), 400

    if not file_type or file_type not in ["RGB-D", "Depth"]:
        logger.warning(f"✗ Invalid file_type value: {file_type}")
        return jsonify({'error': 'Invalid file type. Please upload a RGB-D or Depth file.'}), 400

    logger.info(f" File validation passed: {file.filename}. Proceeding with upload.")

    # SAVE FILE TO DISK
    upload_dir = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)

    db = SessionLocal()

    try:
        # SAVE FILE RECORD
        new_file = File(
            file_name=file.filename,
            file_type=file_type,
            file_path=file_path
        )
        db.add(new_file)
        db.commit()
        db.refresh(new_file)

        logger.info(f" File saved to database with file_id={new_file.file_id}")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_root = os.path.dirname(current_dir)

        # RUN AI PIPELINE
        logger.info("Starting FFB prediction pipeline...")
        prediction_result = run_ffb_prediction(
            bag_path=file_path,
            ffb_id=new_file.file_id,
            base_dir=app_root
        )

        video_abs_path = prediction_result.get("video_absolute_path")
        if video_abs_path:
            new_file.video_path = video_abs_path
            db.add(new_file)  # mark the file object as modified
            db.commit()  # save the video_path to database
            logger.info(f"Saved video path for file {new_file.file_id}: {video_abs_path}")
        else:
            logger.warning(f"No video path in pipeline result for file {new_file.file_id}")

        video_url = f"/video/{new_file.file_id}"

        logger.info(f" Pipeline completed. Result: {prediction_result}")

        # EXTRACT PREDICTED MASS
        predicted_mass = prediction_result["mean_mass"]

        # SAVE PREDICTION
        new_prediction = Prediction(
            file_id=new_file.file_id,
            mass_prediction=predicted_mass,
            model_version="YOLOv5 + Ellipsoid v1"
        )

        db.add(new_prediction)
        db.commit()
        db.refresh(new_prediction)

        logger.info(f" Prediction saved with prediction_id={new_prediction.prediction_id}")

        # RETURN RESPONSE
        return jsonify({
            "message": "File uploaded and prediction completed successfully",
            "file": {
                "file_id": new_file.file_id,
                "file_name": new_file.file_name,
                "file_type": new_file.file_type,
                "upload_date": new_file.upload_date.isoformat() if new_file.upload_date else None
            },
            "prediction": {
                "prediction_id": new_prediction.prediction_id,
                "mass_prediction": float(new_prediction.mass_prediction),
                "model_version": new_prediction.model_version,
                "created_at": new_prediction.created_at.isoformat() if new_prediction.created_at else None
            },
            "pipeline_result": prediction_result,
            "video_url": video_url
        }), 200

    except Exception as e:
        db.rollback()
        logger.exception("Upload/prediction failed")
        return jsonify({'error': f'Failed to upload and predict: {str(e)}'}), 500

    finally:
        db.close()