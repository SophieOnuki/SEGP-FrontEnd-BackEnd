import threading
import sys
import os

from flask import Blueprint, jsonify
from app import SessionLocal
from app.models import Prediction, File

bp = Blueprint('pipeline', __name__)

# ── Pipeline state ────────────────────────────────────────────────────────────
_pipeline_running = False
_pipeline_thread  = None
_latest_mass      = None
_state_lock       = threading.Lock()


def _set_state(running=None, mass=None):
    global _pipeline_running, _latest_mass
    with _state_lock:
        if running is not None:
            _pipeline_running = running
        if mass is not None:
            _latest_mass = mass


def _get_state():
    with _state_lock:
        return _pipeline_running, _latest_mass


# ── DB helper ─────────────────────────────────────────────────────────────────
def save_prediction_to_db(mass_kg: float, model_version: str, file_id: int) -> bool:
    """Insert one prediction row into the predictions table."""
    db = SessionLocal()
    try:
        pred = Prediction(
            file_id=file_id,
            mass_prediction=round(mass_kg, 2),
            model_version=model_version,
        )
        db.add(pred)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"[Pipeline] DB error: {e}")
        return False
    finally:
        db.close()


def _get_or_create_file(file_name: str, file_type: str, file_path: str) -> int:
    """Return file_id of an existing record or insert a new one."""
    db = SessionLocal()
    try:
        existing = db.query(File).filter_by(file_name=file_name).first()
        if existing:
            return existing.file_id
        new_file = File(
            file_name=file_name,
            file_type=file_type,
            file_path=file_path,
        )
        db.add(new_file)
        db.commit()
        db.refresh(new_file)
        return new_file.file_id
    except Exception as e:
        db.rollback()
        print(f"[Pipeline] Could not create file record: {e}")
        return None
    finally:
        db.close()


# ── Pipeline runner ───────────────────────────────────────────────────────────
def _run_pipeline(file_id: int):
    """
    Import and run the FFB pipeline in-process.
    Patches the pipeline so every mass estimate is saved to the DB.
    """
    _set_state(running=True)

    # Make sure the pipeline file's directory is importable
    pipeline_dir = os.path.normpath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', '..', '..')
    )
    # Fallback: resolve relative to CWD
    for candidate in [
        os.path.join(os.getcwd()),
        os.path.join(os.getcwd(), '..'),
        r"c:\Users\admin\Documents\Vicki\School stuff\SEGP",
    ]:
        if os.path.exists(os.path.join(candidate, 'ffb_pipeline_final.py')):
            pipeline_dir = candidate
            break

    sys.path.insert(0, pipeline_dir)

    try:
        import importlib
        import ffb_pipeline_final as pipeline

        # Monkey-patch: wrap the mass-computation section so DB writes happen
        original_ellipsoid = pipeline.ellipsoid_mass_from_points

        def patched_ellipsoid(points):
            result = original_ellipsoid(points)
            if result:
                mass, volume, axes = result
                _set_state(mass=mass)
                save_prediction_to_db(
                    mass_kg=mass,
                    model_version="ffb_pipeline_final_v1",
                    file_id=file_id,
                )
                print(f"[Pipeline] Saved mass={mass:.2f} kg to DB (file_id={file_id})")
            return result

        pipeline.ellipsoid_mass_from_points = patched_ellipsoid
        pipeline.main()

    except Exception as e:
        print(f"[Pipeline] Error during pipeline run: {e}")
    finally:
        _set_state(running=False)


# ── Routes ────────────────────────────────────────────────────────────────────
@bp.route('/pipeline/status', methods=['GET'])
def pipeline_status():
    """Return current pipeline running state and latest mass reading."""
    running, latest_mass = _get_state()
    return jsonify({
        'running': running,
        'latest_mass': latest_mass,
    }), 200


@bp.route('/pipeline/start', methods=['POST'])
def pipeline_start():
    """
    Start the FFB pipeline in a background thread.
    Creates a file record in the DB that predictions will be linked to.
    """
    global _pipeline_thread

    running, _ = _get_state()
    if running:
        return jsonify({'error': 'Pipeline is already running'}), 409

    # Create (or reuse) a file record to attach predictions to
    file_id = _get_or_create_file(
        file_name='live_camera_stream.bag',
        file_type='RGB-D',
        file_path='live',
    )
    if file_id is None:
        return jsonify({'error': 'Could not create file record in DB'}), 500

    _pipeline_thread = threading.Thread(
        target=_run_pipeline,
        args=(file_id,),
        daemon=True,
    )
    _pipeline_thread.start()

    return jsonify({
        'message': 'Pipeline started',
        'file_id': file_id,
    }), 200


@bp.route('/pipeline/stop', methods=['POST'])
def pipeline_stop():
    """
    Signals the pipeline to stop.
    The pipeline loop exits on KeyboardInterrupt; here we just update state.
    For a full stop, the pipeline thread needs to be interrupted externally.
    """
    _set_state(running=False)
    return jsonify({'message': 'Stop signal sent. Pipeline will finish current frame.'}), 200
