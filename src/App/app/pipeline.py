import os
import glob
import json
import csv
from pathlib import Path
import cv2
import numpy as np
import pyrealsense2 as rs
import onnxruntime as ort
import open3d as o3d


# =====================================================
# CONFIGURATION
# =====================================================

YOLO_MODEL_PATH = "C:/Users/Navya/Desktop/Github files/SEGP-FrontEnd-BackEnd/src/App/ffb_detection/ffb_detection/runs/detect/train2/weights/best.onnx"

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
                print(f"[DEBUG] Raw det[0:4] = x={x:.4f}, y={y:.4f}, bw={bw:.4f}, bh={bh:.4f}")

                x1 = float((x - bw / 2) * w / 640)
                y1 = float((y - bh / 2) * h / 640)
                x2 = float((x + bw / 2) * w / 640)
                y2 = float((y + bh / 2) * h / 640)

                print(f"[DEBUG] Box pixels: ({x1:.0f},{y1:.0f}) → ({x2:.0f},{y2:.0f}) | image={w}x{h}")

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


# =====================================================
# ELLIPSOID FITTING + MASS ESTIMATION
# =====================================================
def ellipsoid_mass_from_ply(ply_path):
    """
    Estimate ellipsoid volume and mass from point cloud.
    Returns:
        mass, volume, (a, b, c)
    """
    pcd = o3d.io.read_point_cloud(ply_path)
    points = np.asarray(pcd.points)

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

def video_from_frames(frames_dir, frame_mass_dict, output_filename="ffb_prediction_video.mp4"):
    """
    Create a video from RGB frames with mask overlay and mass annotations.
    Returns path to video or None if failed.
    """
    import imageio

    output_path = os.path.join(frames_dir, output_filename)
    print(f"[DEBUG] video_from_frames: output_path={output_path}")

    rgb_files = sorted(glob.glob(os.path.join(frames_dir, "rgb_*.png")))
    print(f"[DEBUG] Found {len(rgb_files)} RGB files")

    if not rgb_files:
        print("[WARN] No RGB frames found for video creation.")
        return None

    # Read first frame to get dimensions
    sample_img = cv2.imread(rgb_files[0])
    if sample_img is None:
        print(f"[ERROR] Cannot read first RGB frame: {rgb_files[0]}")
        return None

    h, w = sample_img.shape[:2]

    #Load bounding boxes from detection CSV
    det_csv = os.path.join(frames_dir, "detections_onnx.csv")
    frame_boxes = {}

    if os.path.exists(det_csv):
        with open(det_csv, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    fname = row["frame"]
                    x1 = int(float(row["x1"]))
                    y1 = int(float(row["y1"]))
                    x2 = int(float(row["x2"]))
                    y2 = int(float(row["y2"]))
                    conf = float(row["conf"])
                except (ValueError, KeyError):
                    continue
                if conf < CONF_THRESHOLD:
                    continue

                # ── Calculate for bounding boxes ──
                x1 = int(max(0, float(row["x1"]) * 8))
                y1 = int(max(0, float(row["y1"]) * 8))
                x2 = int(min(w, float(row["x2"]) * 8))
                y2 = int(min(h, float(row["y2"]) * 8))

                frame_boxes.setdefault(fname, []).append((x1, y1, x2, y2, conf))
            print(f"[INFO] Loaded bounding boxes for {len(frame_boxes)} frames from {det_csv}.")
    else:
        print("[WARN] detection_onnx.csv does not exist. No bounding boxes found.")

    frames_list = []
    for i, rgb_path in enumerate(rgb_files):
        # Include ALL frames in video for smooth playback
        img = cv2.imread(rgb_path)
        if img is None:
            continue

        frame_basename = os.path.basename(rgb_path)
        frame_index = os.path.basename(rgb_path).split("_")[1].split(".")[0]

        # Draw mask overlay (only exists for pipeline frames)
        mask_path = os.path.join(frames_dir, "masks", f"mask_{frame_index}.png")
        if os.path.exists(mask_path):
            mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
            if mask is not None:
                if mask.shape[:2] != (h, w):
                    mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_NEAREST)
                colour_mask = np.zeros_like(img)
                colour_mask[:, :, 1] = mask
                img = cv2.addWeighted(img, 0.7, colour_mask, 0.3, 0)

        # Only draw bounding box on frames that were processed by the pipeline
        if frame_basename in frame_boxes and os.path.exists(mask_path):
            best_box = max(frame_boxes[frame_basename], key=lambda b: b[4])
            x1, y1, x2, y2, conf = best_box
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(img, f"{conf:.2f}", (x1, max(y1 - 5, 0)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        # Mass annotation (only for pipeline frames, blank for others)
        if frame_index in frame_mass_dict:
            mass = frame_mass_dict[frame_index]
            cv2.putText(img, f"Mass: {mass:.2f} kg", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frames_list.append(img_rgb)

    if not frames_list:
        print(f"[WARN] No frames found for video creation.")
        return None

    #Write H.264 MP4 video using imageio
    imageio.mimwrite(output_path, frames_list, fps=3, codec='libx264', quality=8)
    print(f"[INFO] Video created with imageio: {output_path} ({len(frames_list)} frames")

    return output_path


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

    video_path = video_from_frames(frames_dir, frame_mass_dict)
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