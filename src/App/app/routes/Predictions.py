from flask import Blueprint, jsonify, send_file
from sqlalchemy.orm import joinedload
from sqlalchemy import text
from app.models import Prediction, File
from app import SessionLocal
import csv
import io
from datetime import datetime

bp = Blueprint('predictions', __name__)

@bp.route('/predictions', methods=['GET'])
def get_predictions():
    
    """Fetch all predictions with associated file data."""
    try:
        db = SessionLocal()
        predictions = db.query(Prediction).options(joinedload(Prediction.file)).order_by(Prediction.created_at.desc()).all()
        
        result = []
        for pred in predictions:
            #for building file dict safely
            file_dict =None
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
            })
            
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
        
@bp.route('/predictions/latest', methods=['GET'])
def get_latest_predictions():
    """ Get the latest predictions """
    
    try:
        db = SessionLocal()
        prediction = db.query(Prediction).options(joinedload(Prediction.file)).order_by(Prediction.created_at.desc()).first()
        if not prediction:
            return jsonify({'message': 'No predictions found'}), 404
        file_dict =None
        if prediction.file:
            file_dict = {
                'file_id': prediction.file.file_id,
                'file_name': prediction.file.file_name,
                'upload_date': prediction.file.upload_date.isoformat()
            }
        result = {
            'prediction_id': prediction.prediction_id,
            'file_id': prediction.file.file_id,
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

@bp.route('/predictions/<int:prediction_id>', methods=['DELETE'])
def delete_prediction(prediction_id):
    """ Delete a prediction by its ID """

    try:
        db = SessionLocal()
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

@bp.route('/predictions', methods=['DELETE'])
def delete_all_predictions():
    """ Delete all predictions """

    try:
        db = SessionLocal()
        num_deleted_count = db.query(Prediction).delete() #delete all records
        db.commit()

        return jsonify({'message': f'Deleted {num_deleted_count} predictions'}), 200

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        db.close()

@bp.route('/predictions/export', methods=['GET'])
def export_predictions():
    """ Export all predictions to a CSV file """

    try:
        db = SessionLocal()
        predictions = db.query(Prediction).all()

        # Create CSV in memory
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

        # Convert to  bytes
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

@bp.route('/health', methods=['GET'])
def health_check():
    """ Health check endpoint """
    try:
        db = SessionLocal()
        db.execute(text('SELECT 1'))
        db.close()
        return jsonify({'status': 'ok', 'camera_connected': True, 'model_loaded': True}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@bp.route('/camera/status', methods=['GET'])
def camera_status():
    """Check camera connection status"""
    # Placeholder implementation
    return jsonify({'camera_connected': True, 'model': 'Intel RealSense D 435', 'streaming': True}), 200

@bp.route('/camera/start', methods=['POST'])
def start_camera():
    """Start manual camera streaming"""
    # Placeholder implementation
    try:
        # This should:
        # 1. Capture frame from RealSense
        # 2. Run AI model on frame
        # 3. Save prediction to database
        # 4. Return the new prediction

        return jsonify({
            'error': 'Manual capture not implemented yet'
        }), 501  # 501 = Not Implemented

    except Exception as e:
        return jsonify({'error': str(e)}), 500
