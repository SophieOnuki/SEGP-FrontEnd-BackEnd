from app.ffb_pipeline import load_model, preprocess, postprocess, depth_to_pointcloud, ellipsoid_mass_from_points
import numpy as np

def get_bag_streams(file_path):
    import pyrealsense2 as rs
    bag = rs.bagfile(file_path)
    streams = {}
    for topic, stream_profile in bag.get_device().query_sensors()[0].get_stream_profiles():
        if stream_profile.stream_type() == rs.stream.color:
            video = stream_profile.as_video_stream_profile()
            streams['color'] = {
                'width': video.width(),
                'height': video.height(),
                'format': video.format(),
                'fps': video.fps()
            }
        elif stream_profile.stream_type() == rs.stream.depth:
            video = stream_profile.as_video_stream_profile()
            streams['depth'] = {
                'width': video.width(),
                'height': video.height(),
                'format': video.format(),
                'fps': video.fps()
            }
    bag.close()
    return streams

def process_bag_file(file_path: str, conf_threshold=0.15, step=2):
    import pyrealsense2 as rs
    # Load the pre-trained model
    session = load_model()
    inp_name = session.get_inputs()[0].name
    out_names = [o.name for o in session.get_outputs()]

    # Open bag file with rs.playback
    pipeline = rs.pipeline()
    config = rs.config()

    # Get actual bag streams
    streams = get_bag_streams(file_path)
    if 'color' not in streams or 'depth' not in streams:
        raise ValueError("Bag file must contain both color and depth streams")

    color = streams['color']
    depth = streams['depth']

    config.enable_device_from_file(file_path, repeat_playback=False)
    config.enable_stream(rs.stream.color,
                         color['width'], color['height'],
                         color['format'], color['fps'])
    config.enable_stream(rs.stream.depth,
                         depth['width'], depth['height'],
                         depth['format'], depth['fps'])

    profile = pipeline.start(config)

    align = rs.align(rs.stream.color)
    color_stream = profile.get_stream(rs.stream.color).as_video_stream_profile()
    intr = color_stream.get_intrinsics()

    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()

    fx, fy = intr.fx, intr.fy
    cx, cy = intr.ppx, intr.ppy

    masses = []
    volumes = []
    confidences = []

    try:
        while True:
            try:
                frames = pipeline.wait_for_frames(timeout_ms=1000)
            except RuntimeError:
                # End of bag playback
                break

            frames = align.process(frames)
            color_f = frames.get_color_frame()
            depth_f = frames.get_depth_frame()
            if not color_f or not depth_f:
                continue

            bgr = np.asanyarray(color_f.get_data())
            depth = np.asanyarray(depth_f.get_data())

            inp, scale = preprocess(bgr)
            outputs = session.run(out_names, {inp_name: inp})
            boxes, scores = postprocess(outputs, scale, bgr.shape, conf_thresh=conf_threshold)

            if not boxes:
                continue

            best_idx = int(np.argmax(scores))
            x1, y1, x2, y2 = boxes[best_idx]
            best_conf = float(scores[best_idx])

            mask = np.zeros(depth.shape, dtype=np.uint8)
            mask[y1:y2, x1:x2] = 255

            depth_masked = depth.copy()
            depth_masked[mask == 0] = 0

            points = depth_to_pointcloud(depth_masked, fx, fy, cx, cy, depth_scale, step=step)
            result = ellipsoid_mass_from_points(points)
            if result is None:
                continue

            mass, volume, _axes = result
            masses.append(float(mass))
            volumes.append(float(volume))
            confidences.append(best_conf)

    finally:
        pipeline.stop()

    if not masses:
        raise ValueError("No valid detections/point clouds found in bag file.")

    return {
        "mass": float(np.mean(masses)),
        "volume": float(np.mean(volumes)),
        "confidence": float(np.mean(confidences))
    }

