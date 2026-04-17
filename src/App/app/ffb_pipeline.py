#!/usr/bin/env python3
import pyrealsense2 as rs
import os
import sys
import json
import csv
import time
import glob
import threading
from pathlib import Path
import onnxruntime as ort
import cv2
import numpy as np
# import onnxruntime as ort
# import pyrealsense2 as rs
from flask import Flask, Response

# =====================================================
# CONFIGURATION
# =====================================================
FFB_ID           = 19
STREAM_PORT      = 8080
SAVE_DETECTIONS  = True
CONF_THRESHOLD   = 0.15
SHIRT_Y_RATIO    = 0.45
SKIP             = 5
STEP             = 2
DENSITY_KG_PER_M3 = 956.28
PERCENTILE       = 98
MIN_POINTS       = 500
MIN_MASS         = 5
MAX_MASS         = 30

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YOLO_MODEL_PATH  = os.path.join(BASE_DIR, "ffb_yolo.onnx")   # adjust as needed

# =====================================================
# PATHS
# =====================================================
out_dir      = f"sample_{FFB_ID:03d}"
masks_dir    = os.path.join(out_dir, "masks")
clouds_dir   = os.path.join(out_dir, "pointclouds")
vis_dir      = os.path.join(out_dir, "detections_vis")
csv_path     = os.path.join(out_dir, "detections.csv")
intr_path    = os.path.join(out_dir, "intrinsics.json")

for d in [out_dir, masks_dir, clouds_dir, vis_dir]:
    os.makedirs(d, exist_ok=True)

print(f"FFB ID : {FFB_ID}")
print(f"Output : {out_dir}")

# =====================================================
# GLOBALS FOR MJPEG STREAMING
# =====================================================
output_frame = None
frame_lock   = threading.Lock()

# =====================================================
# FLASK MJPEG SERVER
# =====================================================
# app = Flask(__name__)
#
# def generate_frames():
#     global output_frame
#     while True:
#         with frame_lock:
#             if output_frame is None:
#                 time.sleep(0.01)
#                 continue
#             ret, buffer = cv2.imencode(".jpg", output_frame)
#             if not ret:
#                 continue
#         yield (b"--frame\r\n"
#                b"Content-Type: image/jpeg\r\n\r\n" +
#                buffer.tobytes() + b"\r\n")

# @app.route("/")
# def video_feed():
#     return Response(generate_frames(),
#                     mimetype="multipart/x-mixed-replace; boundary=frame")

# =====================================================
# REALSENSE CAMERA SETUP
# =====================================================
def init_realsense():
    pipe    = rs.pipeline()
    cfg     = rs.config()
    cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16,  30)
    profile = pipe.start(cfg)
    align   = rs.align(rs.stream.color)

    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale  = depth_sensor.get_depth_scale()

    color_stream = profile.get_stream(rs.stream.color).as_video_stream_profile()
    intr         = color_stream.get_intrinsics()

    intrinsics = {
        "fx": intr.fx, "fy": intr.fy,
        "cx": intr.ppx, "cy": intr.ppy,
        "width": intr.width, "height": intr.height,
        "depth_scale": depth_scale
    }
    with open(intr_path, "w") as f:
        json.dump(intrinsics, f, indent=2)

    print("RealSense initialized.")
    print("depth_scale:", depth_scale)
    return pipe, align, depth_scale, intrinsics

# =====================================================
# LOAD YOLO MODEL
# =====================================================
def load_model():
    candidates = [YOLO_MODEL_PATH] + sorted(glob.glob("**/*.onnx", recursive=True))
    for p in candidates:
        if os.path.exists(p):
            sess = ort.InferenceSession(p, providers=["CPUExecutionProvider"])
            print(f"Model loaded: {p}")
            return sess
    print("Error: No ONNX model found.")
    sys.exit(1)

# =====================================================
# PREPROCESS (letterbox, BGR->RGB)
# =====================================================
def preprocess(img, size=640):
    h, w  = img.shape[:2]
    scale = size / max(h, w)
    rgb   = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (int(w * scale), int(h * scale)))
    padded  = np.zeros((size, size, 3), dtype=np.uint8)
    padded[:resized.shape[0], :resized.shape[1]] = resized
    x = padded.astype(np.float32) / 255.0
    x = np.transpose(x, (2, 0, 1))[np.newaxis]
    return x, scale

# =====================================================
# POSTPROCESS
# =====================================================
def postprocess(outputs, scale, orig_shape, conf_thresh=None):
    if conf_thresh is None:
        conf_thresh = CONF_THRESHOLD
    preds = outputs[0]
    if preds.ndim == 3:
        preds = preds[0]
    if preds.shape[0] < preds.shape[1]:
        preds = preds.T

    h0, w0 = orig_shape[:2]
    boxes, scores = [], []

    for p in preds:
        # Support both YOLOv8 (cx,cy,w,h,conf) and YOLOv5 (cx,cy,w,h,obj,cls...)
        if p.shape[0] > 5:
            obj_conf     = p[4]
            class_scores = p[5:]
            cls_id       = int(np.argmax(class_scores))
            conf         = float(obj_conf * class_scores[cls_id])
        else:
            conf = float(p[4])

        if conf < conf_thresh:
            continue

        cx, cy, bw, bh = p[:4]
        x1 = int(max(0, min(w0-1, (cx - bw/2) / scale)))
        y1 = int(max(0, min(h0-1, (cy - bh/2) / scale)))
        x2 = int(max(0, min(w0-1, (cx + bw/2) / scale)))
        y2 = int(max(0, min(h0-1, (cy + bh/2) / scale)))

        if x2 > x1 and y2 > y1:
            boxes.append([x1, y1, x2, y2])
            scores.append(conf)

    return boxes, scores

# =====================================================
# DEPTH → POINT CLOUD (numpy only)
# =====================================================
def depth_to_pointcloud(depth, fx, fy, cx, cy, depth_scale, step=2):
    h, w  = depth.shape
    vs, us = np.mgrid[0:h:step, 0:w:step]
    zraw   = depth[vs, us]
    valid  = zraw > 0
    z  = zraw[valid].astype(np.float64) * depth_scale
    u  = us[valid].astype(np.float64)
    v  = vs[valid].astype(np.float64)
    x  = (u - cx) * z / fx
    y  = (v - cy) * z / fy
    return np.column_stack([x, y, z])

# =====================================================
# SAVE PLY
# =====================================================
def save_ply(points, filepath):
    with open(filepath, "w") as f:
        f.write("ply\nformat ascii 1.0\n")
        f.write(f"element vertex {len(points)}\n")
        f.write("property float x\nproperty float y\nproperty float z\nend_header\n")
        for p in points:
            f.write(f"{p[0]:.6f} {p[1]:.6f} {p[2]:.6f}\n")

# =====================================================
# ELLIPSOID MASS (numpy only, no open3d)
# =====================================================
def ellipsoid_mass_from_points(points):
    if len(points) < MIN_POINTS:
        return None

    center  = points.mean(axis=0)
    X       = points - center
    cov     = np.cov(X.T)
    eigvals, eigvecs = np.linalg.eigh(cov)

    order   = np.argsort(eigvals)[::-1]
    eigvecs = eigvecs[:, order]
    proj    = X @ eigvecs

    a = np.percentile(np.abs(proj[:, 0]), PERCENTILE)
    b = np.percentile(np.abs(proj[:, 1]), PERCENTILE)
    c = np.percentile(np.abs(proj[:, 2]), PERCENTILE)

    if 2 * c < 0.03:
        c = max(a, b) * 0.6

    volume = (4.0 / 3.0) * np.pi * a * b * c * 5
    mass   = volume * DENSITY_KG_PER_M3
    return mass, volume, (a, b, c)

# =====================================================
# MAIN LOOP
# =====================================================
def main():
    global output_frame

    pipe, align, depth_scale, meta = init_realsense()
    session   = load_model()
    inp_name  = session.get_inputs()[0].name
    out_names = [o.name for o in session.get_outputs()]

    fx, fy = meta["fx"], meta["fy"]
    cx, cy = meta["cx"], meta["cy"]

    # CSV header
    with open(csv_path, "w", newline="") as f:
        csv.writer(f).writerow(["frame", "x1", "y1", "x2", "y2", "conf", "class"])

    frame_id   = 0
    saved_rgb  = 0
    mass_results = []

    print(f"\nStream  → http://<device-ip>:{STREAM_PORT}")
    print("Running pipeline. Ctrl+C to stop.\n")

    try:
        while True:
            frames  = pipe.wait_for_frames()
            frames  = align.process(frames)
            color_f = frames.get_color_frame()
            depth_f = frames.get_depth_frame()
            if not color_f or not depth_f:
                continue

            bgr   = np.asanyarray(color_f.get_data())   # already BGR from rs.format.bgr8
            depth = np.asanyarray(depth_f.get_data())   # uint16

            # ---- Detection ----
            inp, scale = preprocess(bgr)
            outputs    = session.run(out_names, {inp_name: inp})
            boxes, scores = postprocess(outputs, scale, bgr.shape)

            # ---- Draw detections ----
            display = bgr.copy()
            for (x1, y1, x2, y2), score in zip(boxes, scores):
                cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(display, f"FFB {score:.2f}",
                            (x1, max(y1-10, 0)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.putText(display, f"Frame:{frame_id}  Det:{len(boxes)}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if mass_results:
                arr = np.array(mass_results)
                filt = arr[(arr >= MIN_MASS) & (arr <= MAX_MASS)]
                if len(filt):
                    cv2.putText(display,
                                f"Mass est: {filt.mean():.2f} kg (n={len(filt)})",
                                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

            # ---- Push to MJPEG stream ----
            with frame_lock:
                output_frame = display.copy()

            # ---- Save + reconstruct every SKIP frames ----
            if SAVE_DETECTIONS and len(boxes) > 0 and frame_id % SKIP == 0:
                frame_name = f"rgb_{saved_rgb:04d}.png"
                rgb_save   = os.path.join(out_dir, frame_name)
                dep_save   = os.path.join(out_dir, f"depth_{saved_rgb:04d}.png")

                cv2.imwrite(rgb_save, bgr)
                cv2.imwrite(dep_save, depth)

                # Best box mask
                best  = int(np.argmax(scores))
                x1, y1, x2, y2 = boxes[best]
                mask  = np.zeros(bgr.shape[:2], dtype=np.uint8)
                cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
                cv2.imwrite(os.path.join(masks_dir, f"mask_{saved_rgb:04d}.png"), mask)

                # CSV row
                with open(csv_path, "a", newline="") as f:
                    csv.writer(f).writerow([
                        frame_name, x1, y1, x2, y2, scores[best], 0
                    ])

                # Point cloud
                depth_masked = depth.copy()
                depth_masked[mask == 0] = 0
                points = depth_to_pointcloud(
                    depth_masked, fx, fy, cx, cy, depth_scale, STEP)

                if len(points) >= MIN_POINTS:
                    ply_path = os.path.join(clouds_dir, f"ffb_frame_{saved_rgb:04d}.ply")
                    save_ply(points, ply_path)

                    result = ellipsoid_mass_from_points(points)
                    if result:
                        mass, volume, axes = result
                        mass_results.append(mass)
                        print(f"[{frame_id:05d}] det={len(boxes)} | "
                              f"mass={mass:.2f} kg | "
                              f"vol={volume:.5f} m³ | "
                              f"a,b,c=({axes[0]:.3f},{axes[1]:.3f},{axes[2]:.3f})")

                saved_rgb += 1

            frame_id += 1

    except KeyboardInterrupt:
        print("\nStopped by user.")

    finally:
        pipe.stop()

        # ---- Final summary ----
        if mass_results:
            arr    = np.array(mass_results)
            filt   = arr[(arr >= MIN_MASS) & (arr <= MAX_MASS)]
            print("\n================ SUMMARY ================")
            print(f"Frames used (filtered): {len(filt)}")
            if len(filt):
                print(f"Mean mass   (kg):       {filt.mean():.2f}")
                print(f"Median mass (kg):       {np.median(filt):.2f}")
                print(f"Std dev     (kg):       {filt.std():.2f}")
            print("========================================")

# =====================================================
# ENTRY POINT
# =====================================================
# if __name__ == "__main__":
#     print(f"Starting MJPEG server on port {STREAM_PORT}...")
#     threading.Thread(
#         target=lambda: app.run(
#             host="0.0.0.0",
#             port=STREAM_PORT,
#             debug=False,
#             use_reloader=False
#         ),
#         daemon=True
#     ).start()
#
#     main()