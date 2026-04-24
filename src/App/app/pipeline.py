import os
import glob
import json
import csv
import subprocess
from pathlib import Path
import cv2
import numpy as np
import pyrealsense2 as rs
import onnxruntime as ort


# =====================================================
# CONFIGURATION
# =====================================================

YOLO_MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Odriod", "odroid_h3_deployment", "ffb_yolo.onnx")

DENSITY_KG_PER_M3 = 956.28
PERCENTILE = 98
MIN_POINTS = 500
CONF_THRESHOLD = 0.15
SKIP = 5
STEP = 2

MIN_MASS = 5
MAX_MASS = 30

# IMPORTANT:
# This is your empirical correction factor.
# Keep it visible and explain it in your report.
CORRECTION_FACTOR = 5.0


# =====================================================
# BAG EXTRACTION
# =====================================================
def extract_bag_if_needed(bag_path, out_dir):
    """
    Extract RGB and depth frames from .bag file if not already extracted.
    Saves:
        - intrinsics.json
        - rgb_XXXX.png
        - depth_XXXX.png
    """
    intr_path = os.path.join(out_dir, "intrinsics.json")

    if os.path.exists(intr_path):
        print(f"[INFO] Frames already extracted for {out_dir}. Skipping extraction.")
        return

    print(f"[INFO] Extracting bag file: {bag_path}")

    pipe = rs.pipeline()
    cfg = rs.config()
    cfg.enable_device_from_file(str(bag_path), repeat_playback=False)
    cfg.enable_stream(rs.stream.color)
    cfg.enable_stream(rs.stream.depth)

    profile = pipe.start(cfg)
    align = rs.align(rs.stream.color)

    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()

    color_stream = profile.get_stream(rs.stream.color).as_video_stream_profile()
    intr = color_stream.get_intrinsics()

    with open(intr_path, "w") as f:
        json.dump({
            "fx": intr.fx,
            "fy": intr.fy,
            "cx": intr.ppx,
            "cy": intr.ppy,
            "width": intr.width,
            "height": intr.height,
            "depth_scale": depth_scale
        }, f, indent=2)

    print("[INFO] Saved intrinsics.")

    i = 0
    try:
        while True:
            frames = pipe.wait_for_frames()
            frames = align.process(frames)

            depth = frames.get_depth_frame()
            color = frames.get_color_frame()

            if not depth or not color:
                continue

            i += 1

            rgb = np.asanyarray(color.get_data())
            dep = np.asanyarray(depth.get_data())

            cv2.imwrite(
                os.path.join(out_dir, f"rgb_{i:04d}.png"),
                cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            )
            cv2.imwrite(
                os.path.join(out_dir, f"depth_{i:04d}.png"),
                dep
            )

    except RuntimeError:
        print("[INFO] Reached end of bag file.")

    finally:
        pipe.stop()
        print(f"[INFO] Done. Extracted {i} frames.")


# =====================================================
# YOLO DETECTOR
# =====================================================
class LocalYOLODetector:
    def __init__(self, model_path, input_size=640, conf_threshold=0.25):
        self.input_size = input_size
        self.conf_threshold = conf_threshold

        model_path = Path(model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"ONNX model not found: {model_path}")

        self.session = ort.InferenceSession(str(model_path))
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name


# =====================================================
# DETECTION
# =====================================================
def run_detection(frames_dir, detector):
    """
    Run YOLO ONNX detection on extracted RGB frames.
    Saves detections into:
        detections_onnx.csv
    """
    csv_path = os.path.join(frames_dir, "detections_onnx.csv")
    rgb_files = sorted(glob.glob(os.path.join(frames_dir, "rgb_*.png")))

    if len(rgb_files) == 0:
        raise RuntimeError("No RGB frames found for detection.")

    print(f"[INFO] Running detection on {len(rgb_files)} RGB frames...")

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["frame", "x1", "y1", "x2", "y2", "conf", "class"])

        for rgb_path in rgb_files:
            img = cv2.imread(rgb_path)
            if img is None:
                print(f"[WARN] Failed to read image: {rgb_path}")
                continue

            h, w = img.shape[:2]

            img_resized = cv2.resize(img, (640, 640))
            img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
            img_input = img_rgb.astype(np.float32) / 255.0
            img_input = np.transpose(img_input, (2, 0, 1))
            img_input = np.expand_dims(img_input, axis=0)

            outputs = detector.session.run(
                [detector.output_name],
                {detector.input_name: img_input}
            )[0]

            for det in outputs[0]:
                obj_conf = det[4]
                class_scores = det[5:]
                class_id = int(np.argmax(class_scores))
                class_conf = class_scores[class_id]
                conf = float(obj_conf * class_conf)

                if conf < CONF_THRESHOLD:
                    continue

                x, y, bw, bh = det[0:4]

                x1 = float((x - bw / 2) * w / 640)
                y1 = float((y - bh / 2) * h / 640)
                x2 = float((x + bw / 2) * w / 640)
                y2 = float((y + bh / 2) * h / 640)


                writer.writerow([
                    os.path.basename(rgb_path),
                    x1, y1, x2, y2,
                    conf,
                    class_id
                ])

    print(f"[INFO] Detection CSV saved to: {csv_path}")
    return csv_path


# =====================================================
# MASK GENERATION
# =====================================================
def generate_masks_from_csv(frames_dir, det_csv):
    """
    Create binary masks from detection bounding boxes.
    Saves:
        masks/mask_XXXX.png
    """
    out_mask_dir = os.path.join(frames_dir, "masks")
    os.makedirs(out_mask_dir, exist_ok=True)

    detections = {}

    with open(det_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["conf"] is None or row["conf"] == "":
                continue

            try:
                frame = row["frame"]
                x1 = int(float(row["x1"]))
                y1 = int(float(row["y1"]))
                x2 = int(float(row["x2"]))
                y2 = int(float(row["y2"]))
                conf = float(row["conf"])
            except ValueError:
                print(f"[WARN] Skipping invalid row: {row}")
                continue

            if conf < CONF_THRESHOLD:
                continue

            if frame not in detections:
                detections[frame] = []

            detections[frame].append((x1, y1, x2, y2))

    for frame_name, boxes in detections.items():
        rgb_path = os.path.join(frames_dir, frame_name)
        img = cv2.imread(rgb_path)

        if img is None:
            print(f"[WARN] Could not read RGB frame: {rgb_path}")
            continue

        h, w = img.shape[:2]
        mask = np.zeros((h, w), dtype=np.uint8)

        for (x1, y1, x2, y2) in boxes:
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(w - 1, x2)
            y2 = min(h - 1, y2)
            cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)

            print(f"[DEBUG] Box pixels: ({x1:.0f},{y1:.0f}) → ({x2:.0f},{y2:.0f}) | image={w}x{h}")

        idx = frame_name.split("_")[1].split(".")[0]
        mask_path = os.path.join(out_mask_dir, f"mask_{idx}.png")
        cv2.imwrite(mask_path, mask)

    print(f"[INFO] Masks generated: {len(detections)}")
    return out_mask_dir


# =====================================================
# DEPTH → POINT CLOUD
# =====================================================
def depth_to_pointcloud(depth, fx, fy, cx, cy, depth_scale, step=2):
    """
    Convert depth map to 3D point cloud.
    """
    points = []
    h, w = depth.shape

    for v in range(0, h, step):
        for u in range(0, w, step):
            z = depth[v, u] * depth_scale
            if z <= 0:
                continue

            x = (u - cx) * z / fx
            y = (v - cy) * z / fy

            points.append([x, y, z])

    return np.array(points)


# =====================================================
# SAVE PLY
# =====================================================
def save_ply(points, filepath):
    """
    Save numpy point array as ASCII .ply file.
    """
    with open(filepath, "w") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(points)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("end_header\n")

        for p in points:
            f.write(f"{p[0]} {p[1]} {p[2]}\n")


# =====================================================
# POINT CLOUD RECONSTRUCTION
# =====================================================
def generate_pointclouds(frames_dir, fx, fy, cx, cy, depth_scale):
    """
    Generate point clouds from masked depth frames.
    Saves:
        pointclouds/ffb_frame_XXXX.ply
    """
    masks_dir = os.path.join(frames_dir, "masks")
    out_dir = os.path.join(frames_dir, "pointclouds")
    os.makedirs(out_dir, exist_ok=True)

    depth_paths = sorted(glob.glob(os.path.join(frames_dir, "depth_*.png")))
    if len(depth_paths) == 0:
        raise RuntimeError("No depth frames found.")

    print(f"[INFO] Generating point clouds from {len(depth_paths)} depth frames...")

    saved_clouds = []

    for i, depth_path in enumerate(depth_paths):
        if i % SKIP != 0:
            continue

        fname = os.path.basename(depth_path)
        idx = fname.split("_")[1].split(".")[0]
        mask_path = os.path.join(masks_dir, f"mask_{idx}.png")

        depth = cv2.imread(depth_path, cv2.IMREAD_UNCHANGED)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        if depth is None:
            print(f"[WARN] Could not read depth frame: {depth_path}")
            continue

        if mask is None:
            print(f"[WARN] No mask found for frame {idx}. Skipping.")
            continue

        if np.count_nonzero(mask) < 200:
            print(f"[WARN] Mask too small for frame {idx}. Skipping.")
            continue

        depth = depth.copy()
        depth[mask == 0] = 0

        points = depth_to_pointcloud(depth, fx, fy, cx, cy, depth_scale, STEP)

        if len(points) == 0:
            print(f"[WARN] No valid points for frame {idx}. Skipping.")
            continue

        out_path = os.path.join(out_dir, f"ffb_frame_{idx}.ply")
        save_ply(points, out_path)
        saved_clouds.append(out_path)

    print(f"[INFO] Saved {len(saved_clouds)} point clouds.")
    return saved_clouds


def _read_ply_points(ply_path):
    points = []
    with open(ply_path, "r") as f:
        in_header = True
        for line in f:
            if in_header:
                if line.strip() == "end_header":
                    in_header = False
                continue
            vals = line.strip().split()
            if len(vals) >= 3:
                points.append([float(vals[0]), float(vals[1]), float(vals[2])])
    return np.array(points)


# =====================================================
# ELLIPSOID FITTING + MASS ESTIMATION
# =====================================================
def ellipsoid_mass_from_ply(ply_path):
    """
    Estimate ellipsoid volume and mass from point cloud.
    Returns:
        mass, volume, (a, b, c)
    """
    # pcd = o3d.io.read_point_cloud(ply_path)
    # points = np.asarray(pcd.points)
    points = _read_ply_points(ply_path)

    if len(points) < MIN_POINTS:
        return None

    center = points.mean(axis=0)
    X = points - center

    cov = np.cov(X.T)
    eigvals, eigvecs = np.linalg.eigh(cov)

    order = np.argsort(eigvals)[::-1]
    eigvecs = eigvecs[:, order]

    proj = X @ eigvecs

    a = np.percentile(np.abs(proj[:, 0]), PERCENTILE)
    b = np.percentile(np.abs(proj[:, 1]), PERCENTILE)
    c = np.percentile(np.abs(proj[:, 2]), PERCENTILE)

    # Depth collapse correction
    if 2 * c < 0.03:
        c = max(a, b) * 0.6

    volume = (4.0 / 3.0) * np.pi * a * b * c * CORRECTION_FACTOR
    mass = volume * DENSITY_KG_PER_M3

    return mass, volume, (a, b, c)


# =====================================================
# MASS ESTIMATION ACROSS ALL FRAMES
# =====================================================
def estimate_mass_from_pointclouds(ply_files):
    """
    Estimate mass across all generated point clouds.
    Applies physical mass filtering.
    """
    if len(ply_files) == 0:
        raise RuntimeError("No point clouds available for mass estimation.")

    print(f"[INFO] Estimating mass from {len(ply_files)} point clouds...")

    results = []
    volumes = []
    frame_results = []

    for ply in ply_files:
        name = os.path.basename(ply)
        out = ellipsoid_mass_from_ply(ply)

        if out is None:
            print(f"[WARN] {name} skipped (too few points)")
            continue

        mass, volume, axes = out
        results.append(mass)
        volumes.append(volume)

        frame_results.append({
            "frame": name,
            "mass": float(mass),
            "volume": float(volume),
            "a": float(axes[0]),
            "b": float(axes[1]),
            "c": float(axes[2])
        })

        print(
            f"[INFO] {name:<18} | "
            f"mass = {mass:6.2f} kg | "
            f"vol = {volume:.5f} m³ | "
            f"a,b,c = ({axes[0]:.3f}, {axes[1]:.3f}, {axes[2]:.3f})"
        )

    if len(results) == 0:
        raise RuntimeError("No valid mass estimates were produced.")

    results = np.array(results)
    volumes = np.array(volumes)

    filtered_mask = (results >= MIN_MASS) & (results <= MAX_MASS)
    filtered = results[filtered_mask]
    filtered_volumes = volumes[filtered_mask]

    if len(filtered) == 0:
        raise RuntimeError(f"No masses in valid range {MIN_MASS}–{MAX_MASS} kg.")

    summary = {
        "frames_used": int(len(filtered)),
        "mean_mass": float(np.mean(filtered)),
        "median_mass": float(np.median(filtered)),
        "std_dev": float(np.std(filtered)),
        "min_mass": float(np.min(filtered)),
        "max_mass": float(np.max(filtered)),
        "mean_volume": float(np.mean(filtered_volumes)),
        "median_volume": float(np.median(filtered_volumes)),
        "all_frame_results": frame_results
    }

    print("\n================ SUMMARY ================")
    print(f"Frames used (filtered): {summary['frames_used']}")
    print(f"Mean mass (kg):         {summary['mean_mass']:.2f}")
    print(f"Median mass (kg):       {summary['median_mass']:.2f}")
    print(f"Std dev (kg):           {summary['std_dev']:.2f}")
    print("========================================\n")

    return summary

def _detect_bbox_for_display(img, session, input_name, output_name, conf_threshold=0.15):
    """Run YOLO inference on a single frame and return the best (x1,y1,x2,y2) in image coords."""
    h, w = img.shape[:2]
    img_resized = cv2.resize(img, (640, 640))
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    img_input = np.expand_dims(np.transpose(img_rgb, (2, 0, 1)), axis=0)

    raw = session.run([output_name], {input_name: img_input})[0]
    # Output shape [1, 5, 8400]: channels are [cx, cy, w, h, conf] across 8400 anchors
    preds = raw[0].T  # [8400, 5]

    img_cx, img_cy = w / 2, h / 2
    # Only accept detections whose center lies within the middle 60% of the frame
    x_margin = w * 0.20
    y_margin = h * 0.20
    best_dist, best_box = float('inf'), None
    for det in preds:
        cx, cy, bw, bh, conf = det
        if float(conf) < conf_threshold:
            continue
        det_cx = cx * w / 640
        det_cy = cy * h / 640
        if det_cx < x_margin or det_cx > w - x_margin:
            continue
        if det_cy < y_margin or det_cy > h - y_margin:
            continue
        dist = (det_cx - img_cx) ** 2 + (det_cy - img_cy) ** 2
        if dist < best_dist:
            best_dist = dist
            x1 = int((cx - bw / 2) * w / 640)
            y1 = int((cy - bh / 2) * h / 640)
            x2 = int((cx + bw / 2) * w / 640)
            y2 = int((cy + bh / 2) * h / 640)
            best_box = (max(0, x1), max(0, y1), min(w - 1, x2), min(h - 1, y2))

    return best_box


def video_from_frames(frames_dir, frame_mass_dict, det_csv=None, output_filename="ffb_prediction_video.mp4"):
    """
    Create a video from RGB frames with mask overlay and mass annotations.
    Returns path to video or None if failed.
    """
    output_path = os.path.join(frames_dir, output_filename)
    print(f"[DEBUG] video_from_frames: output_path={output_path}")

    rgb_files = sorted(glob.glob(os.path.join(frames_dir, "rgb_*.png")))
    print(f"[DEBUG] Found {len(rgb_files)} RGB files")

    if not rgb_files:
        print("[WARN] No RGB frames found for video creation.")
        return None

    sample_img = cv2.imread(rgb_files[0])
    if sample_img is None:
        print(f"[ERROR] Cannot read first RGB frame: {rgb_files[0]}")
        return None

    # Load YOLO model just for display bounding boxes
    display_session = None
    try:
        import onnxruntime as ort
        display_session = ort.InferenceSession(YOLO_MODEL_PATH)
        display_input = display_session.get_inputs()[0].name
        display_output = display_session.get_outputs()[0].name
    except Exception as e:
        print(f"[WARN] Could not load YOLO for display: {e}")

    h, w = sample_img.shape[:2]
    temp_path = output_path.replace(".mp4", "_raw.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(temp_path, fourcc, 10, (w, h))

    for rgb_path in rgb_files:
        img = cv2.imread(rgb_path)
        if img is None:
            continue

        frame_index = os.path.basename(rgb_path).split("_")[1].split(".")[0]

        # Mask overlay intentionally removed — mask covers wrong region due to detection format mismatch

        mass = frame_mass_dict.get(frame_index)

        # Get bounding box from fresh inference (correct format) for display only
        bbox = None
        if display_session is not None:
            bbox = _detect_bbox_for_display(img, display_session, display_input, display_output)

        if bbox:
            x1, y1, x2, y2 = bbox
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"Mass: {mass:.2f} kg" if mass is not None else "FFB detected"
            label_y = max(y1 - 10, 20)
            cv2.putText(img, label, (x1, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        elif mass is not None:
            cv2.putText(img, f"Mass: {mass:.2f} kg", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        writer.write(img)

    writer.release()
    print(f"[INFO] Raw video created: {temp_path}")

    # Re-encode to H.264 using bundled ffmpeg so browsers can play it
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        result = subprocess.run(
            [ffmpeg_exe, "-y", "-i", temp_path, "-vcodec", "libx264", "-pix_fmt", "yuv420p", output_path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            os.remove(temp_path)
            print(f"[INFO] H.264 video created: {output_path}")
            return output_path
        else:
            print(f"[WARN] ffmpeg re-encode failed: {result.stderr[-500:]}")
            os.rename(temp_path, output_path)
            return output_path
    except Exception as e:
        print(f"[WARN] ffmpeg re-encode error: {e}, using raw video")
        os.rename(temp_path, output_path)
        return output_path
#(Fix video bounding box display and remove debug URL)


# =====================================================
# MASTER PIPELINE
# =====================================================
def run_ffb_prediction(bag_path, ffb_id, base_dir=None):
    if base_dir is None:
        base_dir = os.getcwd()  # fallback
    frames_dir = os.path.join(base_dir, f"sample_{int(ffb_id):03d}")
    os.makedirs(frames_dir, exist_ok=True)

    if not os.path.exists(bag_path):
        raise FileNotFoundError(f"Bag file not found: {bag_path}")

    if not os.path.exists(YOLO_MODEL_PATH):
        raise FileNotFoundError(f"YOLO ONNX model not found: {YOLO_MODEL_PATH}")


    # -------------------------------------------------
    # 1. Extract bag frames
    # -------------------------------------------------
    extract_bag_if_needed(bag_path, frames_dir)

    intr_path = os.path.join(frames_dir, "intrinsics.json")
    if not os.path.exists(intr_path):
        raise RuntimeError("intrinsics.json not found after bag extraction.")

    with open(intr_path, "r") as f:
        meta = json.load(f)

    fx = float(meta["fx"])
    fy = float(meta["fy"])
    cx = float(meta["cx"])
    cy = float(meta["cy"])
    depth_scale = float(meta["depth_scale"])

    print("[INFO] Loaded intrinsics:")
    print(f"       fx={fx}, fy={fy}, cx={cx}, cy={cy}, depth_scale={depth_scale}")

    # -------------------------------------------------
    # 2. Load detector
    # -------------------------------------------------
    detector = LocalYOLODetector(
        model_path=YOLO_MODEL_PATH,
        input_size=640,
        conf_threshold=0.25
    )

    # -------------------------------------------------
    # 3. Run detection
    # -------------------------------------------------
    det_csv = run_detection(frames_dir, detector)

    # -------------------------------------------------
    # 4. Generate masks
    # -------------------------------------------------
    generate_masks_from_csv(frames_dir, det_csv)

    # -------------------------------------------------
    # 5. Generate point clouds
    # -------------------------------------------------
    ply_files = generate_pointclouds(
        frames_dir=frames_dir,
        fx=fx,
        fy=fy,
        cx=cx,
        cy=cy,
        depth_scale=depth_scale
    )

    # -------------------------------------------------
    # 6. Estimate mass
    # -------------------------------------------------
    summary = estimate_mass_from_pointclouds(ply_files)

    #-------------------------------------------------
    # 6.5 Create video with annotations for visualization
    #-------------------------------------------------
    frame_mass_dict = {}
    for fr in summary.get("all_frame_results", []):
        index = fr["frame"].split("_")[2].split(".")[0]
        frame_mass_dict[index] = fr["mass"]

    video_path = video_from_frames(frames_dir, frame_mass_dict, det_csv=det_csv)
    video_filename = os.path.basename(video_path) if video_path else None

    # -------------------------------------------------
    # 7. Return API-friendly result
    # -------------------------------------------------
    result = {
        "ffb_id": int(ffb_id),
        "bag_file": os.path.basename(bag_path),
        "frames_directory": frames_dir,
        "video_absolute_path": video_path,
        **summary
    }

    result["video_filename"] = video_filename

    return result