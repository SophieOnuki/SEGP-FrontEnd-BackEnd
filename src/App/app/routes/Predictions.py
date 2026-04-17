from flask import Blueprint, jsonify, send_file, request, current_app
from sqlalchemy.orm import joinedload
from sqlalchemy import text
from app.models import Prediction, File
from app import SessionLocal
from app.pipeline import run_ffb_prediction
import csv
import io
import os
from datetime import datetime
import subprocess
import sys
bp = Blueprint('predictions', __name__)


# =====================================================
# GET ALL PREDICTIONS
# =====================================================
@bp.route('/predictions', methods=['GET'])
def get_predictions():
    """Fetch all predictions with associated file data."""
    db = SessionLocal()
    try:
        predictions = (
            db.query(Prediction)
            .options(joinedload(Prediction.file))
            .order_by(Prediction.created_at.desc())
            .all()
        )

        result = []
        for pred in predictions:
            file_dict = None
            if pred.file:
                file_dict = {
                    'file_id': pred.file.file_id,
                    'file_name': pred.file.file_name,
                    'upload_date': pred.file.upload_date.isoformat()
                }

            result.append({
                'prediction_id': pred.prediction_id,
                'file_id': pred.file_id,
                'mass_prediction': float(pred.mass_prediction),
                'model_version': pred.model_version,
                'created_at': pred.created_at.isoformat(),
                'file': file_dict
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        db.close()


# =====================================================
# GET LATEST PREDICTION
# =====================================================
@bp.route('/predictions/latest', methods=['GET'])
def get_latest_predictions():
    """Get the latest prediction."""
    db = SessionLocal()
    try:
        prediction = (
            db.query(Prediction)
            .options(joinedload(Prediction.file))
            .order_by(Prediction.created_at.desc())
            .first()
        )

        if not prediction:
            return jsonify({'message': 'No predictions found'}), 404

        file_dict = None
        if prediction.file:
            file_dict = {
                'file_id': prediction.file.file_id,
                'file_name': prediction.file.file_name,
                'upload_date': prediction.file.upload_date.isoformat()
            }

        result = {
            'prediction_id': prediction.prediction_id,
            'file_id': prediction.file_id,
            'mass_prediction': float(prediction.mass_prediction),
            'model_version': prediction.model_version,
            'created_at': prediction.created_at.isoformat(),
            'file': file_dict
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        db.close()


# =====================================================
# DELETE ONE PREDICTION
# =====================================================
@bp.route('/predictions/<int:prediction_id>', methods=['DELETE'])
def delete_prediction(prediction_id):
    """Delete a prediction by ID."""
    db = SessionLocal()
    try:
        prediction = db.query(Prediction).filter_by(prediction_id=prediction_id).first()

        if not prediction:
            return jsonify({'message': 'Prediction not found'}), 404

        db.delete(prediction)
        db.commit()

        return jsonify({'message': 'Prediction deleted'}), 200

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        db.close()


# =====================================================
# DELETE ALL PREDICTIONS
# =====================================================
@bp.route('/predictions', methods=['DELETE'])
def delete_all_predictions():
    """Delete all predictions."""
    db = SessionLocal()
    try:
        num_deleted_count = db.query(Prediction).delete()
        db.commit()

        return jsonify({'message': f'Deleted {num_deleted_count} predictions'}), 200

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        db.close()


# =====================================================
# EXPORT PREDICTIONS CSV
# =====================================================
@bp.route('/predictions/export', methods=['GET'])
def export_predictions():
    """Export all predictions to CSV."""
    db = SessionLocal()
    try:
        predictions = db.query(Prediction).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Prediction ID', 'File ID', 'Mass Prediction', 'Model Version', 'Created At'])

        for pred in predictions:
            writer.writerow([
                pred.prediction_id,
                pred.file_id,
                float(pred.mass_prediction),
                pred.model_version,
                pred.created_at.isoformat()
            ])

        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'predictions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        db.close()


# =====================================================
# HEALTH CHECK
# =====================================================
@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    db = SessionLocal()
    try:
        db.execute(text('SELECT 1'))
        return jsonify({
            'status': 'ok',
            'camera_connected': True,
            'model_loaded': True
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

    finally:
        db.close()


# =====================================================
# CAMERA STATUS
# =====================================================
@bp.route('/camera/status', methods=['GET'])
def camera_status():
    """Check camera connection status."""
    return jsonify({
        'camera_connected': True,
        'model': 'Intel RealSense D435',
        'streaming': False
    }), 200


# =====================================================
# RUN ACTUAL PREDICTION PIPELINE
# =====================================================
@bp.route('/camera/start', methods=['POST'])
def start_camera():
    """Run prediction pipeline for an uploaded .bag file"""
    db = SessionLocal()

    try:
        data = request.get_json()
        file_id = data.get("file_id")

        if not file_id:
            return jsonify({"error": "file_id is required"}), 400

        uploaded_file = db.query(File).filter_by(file_id=file_id).first()

        if not uploaded_file:
            return jsonify({"error": "File not found"}), 404

        bag_path = uploaded_file.file_path

        if not os.path.exists(bag_path):
            return jsonify({"error": f"Bag file not found: {bag_path}"}), 404

        # Run pipeline.py as a subprocess
        pipeline_path = os.path.join(os.getcwd(), "app", "pipeline.py")

        result = subprocess.run(
            [sys.executable, pipeline_path, bag_path],
            capture_output=True,
            text=True
        )

        print("PIPELINE STDOUT:\n", result.stdout)
        print("PIPELINE STDERR:\n", result.stderr)

        if result.returncode != 0:
            return jsonify({
                "error": "Pipeline failed",
                "details": result.stderr
            }), 500

        # Expect pipeline to print only the final predicted mass
        try:
            predicted_mass = float(result.stdout.strip().splitlines()[-1])
        except:
            return jsonify({
                "error": "Could not parse pipeline output",
                "raw_output": result.stdout
            }), 500

        # Save prediction to database
        new_prediction = Prediction(
            file_id=file_id,
            mass_prediction=predicted_mass,
            model_version="v1.0"
        )

        db.add(new_prediction)
        db.commit()
        db.refresh(new_prediction)

        return jsonify({
            "message": "Prediction completed successfully",
            "prediction_id": new_prediction.prediction_id,
            "file_id": file_id,
            "mass_prediction": predicted_mass,
            "model_version": new_prediction.model_version,
            "created_at": new_prediction.created_at.isoformat()
        }), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()