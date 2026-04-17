#!/usr/bin/env python3
"""
Odroid H3+ Inference Script for FFB Detection
Optimized for edge device deployment
"""

import cv2
import numpy as np
import time
from pathlib import Path

# Try to import ONNX Runtime (recommended)
try:
    import onnxruntime as ort
    USE_ONNX = True
except ImportError:
    USE_ONNX = False
    print("[WARNING] ONNX Runtime not found. Install with: pip3 install onnxruntime")

# Try TensorFlow Lite as fallback (full TensorFlow for x86_64)
try:
    import tensorflow as tf
    USE_TFLITE = True
except ImportError:
    USE_TFLITE = False

class FFBYOLOInference:
    def __init__(self, model_path, input_size=640, conf_threshold=0.25):
        """
        Initialize FFB YOLO inference.
        
        Args:
            model_path: Path to ONNX or TFLite model
            input_size: Input image size (640 recommended for Odroid H3+, 416 or 320 for faster inference)
            conf_threshold: Confidence threshold for detections
        """
        self.model_path = Path(model_path)
        self.input_size = input_size
        self.conf_threshold = conf_threshold
        
        # Determine model format
        if model_path.endswith('.onnx'):
            self.load_onnx_model()
        elif model_path.endswith('.tflite'):
            self.load_tflite_model()
        else:
            raise ValueError("Model must be .onnx or .tflite format")
    
    def load_onnx_model(self):
        """Load ONNX model."""
        if not USE_ONNX:
            raise ImportError("ONNX Runtime not installed. Install with: pip3 install onnxruntime")
        
        # Create ONNX Runtime session (compatible with very old versions)
        try:
            # Try newer ONNX Runtime API
            self.session = ort.InferenceSession(str(self.model_path))
        except:
            # Try even older API
            import onnx
            model = onnx.load(str(self.model_path))
            self.session = ort.InferenceSession(model.SerializeToString())
        
        # Get input/output details
        self.input_name = self.session.get_inputs()[0].name
        self.output_names = [output.name for output in self.session.get_outputs()]
        
        print(f"[OK] ONNX model loaded: {self.model_path}")
        print(f"    Input size: {self.input_size}x{self.input_size}")
    
    def load_tflite_model(self):
        """Load TensorFlow Lite model."""
        if not USE_TFLITE:
            raise ImportError("TensorFlow not installed. Install with: pip3 install tensorflow")
        
        # For x86_64 (Odroid H3+), use full TensorFlow
        self.interpreter = tf.lite.Interpreter(model_path=str(self.model_path))
        self.interpreter.allocate_tensors()
        
        # Get input/output details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        print(f"[OK] TFLite model loaded: {self.model_path}")
    
    def preprocess_image(self, image):
        """Preprocess image for inference."""
        # Resize to model input size
        img_resized = cv2.resize(image, (self.input_size, self.input_size))
        
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        
        # Normalize to [0, 1]
        img_normalized = img_rgb.astype(np.float32) / 255.0
        
        # Add batch dimension and transpose to NCHW format
        img_input = np.expand_dims(img_normalized, axis=0)
        img_input = np.transpose(img_input, (0, 3, 1, 2))
        
        return img_input
    
    def postprocess_detections(self, outputs, original_shape):
        """Post-process model outputs to get bounding boxes.

        Notes:
        - Ultralytics YOLOv8 ONNX export commonly outputs shape (1, 5, 8400) for single-class:
          5 = [x, y, w, h, conf] in *input-size pixels* (not normalized).
        - Older logic treated these as normalized -> produced huge/invalid boxes, so nothing was drawn.
        """

        def _sigmoid(x: np.ndarray) -> np.ndarray:
            return 1.0 / (1.0 + np.exp(-x))

        detections: list[dict] = []
        h_orig, w_orig = original_shape[:2]
        scale_x = w_orig / float(self.input_size)
        scale_y = h_orig / float(self.input_size)

        output = outputs[0] if isinstance(outputs, list) else outputs
        output = np.asarray(output)

        # Squeeze batch dim if present
        if output.ndim == 3 and output.shape[0] == 1:
            output = output[0]

        # Common YOLOv8 ONNX single-class: (5, 8400) -> transpose to (8400, 5)
        if output.ndim == 2 and output.shape[0] <= 10 and output.shape[1] > output.shape[0]:
            output = output.T

        if output.ndim != 2 or output.shape[1] < 5:
            # Unknown output format
            return detections

        # Parse scores
        # If we have class columns: [x, y, w, h, obj, cls...]
        if output.shape[1] > 5:
            obj = output[:, 4].astype(np.float32)
            cls_scores = output[:, 5:].astype(np.float32)
            if np.max(obj) > 1.0:
                obj = _sigmoid(obj)
            if np.max(cls_scores) > 1.0:
                cls_scores = _sigmoid(cls_scores)
            cls_ids = np.argmax(cls_scores, axis=1)
            cls_conf = cls_scores[np.arange(cls_scores.shape[0]), cls_ids]
            scores = obj * cls_conf
        else:
            scores = output[:, 4].astype(np.float32)
            if np.max(scores) > 1.0:
                scores = _sigmoid(scores)
            cls_ids = np.zeros((output.shape[0],), dtype=np.int64)

        # Candidate boxes in model-input pixel space
        x = output[:, 0].astype(np.float32)
        y = output[:, 1].astype(np.float32)
        w = output[:, 2].astype(np.float32)
        h = output[:, 3].astype(np.float32)

        # Convert center->top-left in input space
        x1_in = x - w / 2.0
        y1_in = y - h / 2.0
        w_in = w
        h_in = h

        # Filter by confidence threshold
        keep = scores >= float(self.conf_threshold)
        if not np.any(keep):
            return detections

        x1_in = x1_in[keep]
        y1_in = y1_in[keep]
        w_in = w_in[keep]
        h_in = h_in[keep]
        scores_k = scores[keep]
        cls_ids_k = cls_ids[keep]

        # Scale to original image space
        x1 = x1_in * scale_x
        y1 = y1_in * scale_y
        w1 = w_in * scale_x
        h1 = h_in * scale_y

        # NMS (per class, but we only have 1 class in this project)
        boxes_for_nms = [[float(x1[i]), float(y1[i]), float(w1[i]), float(h1[i])] for i in range(len(scores_k))]
        indices = cv2.dnn.NMSBoxes(
            bboxes=boxes_for_nms,
            scores=[float(s) for s in scores_k],
            score_threshold=float(self.conf_threshold),
            nms_threshold=0.45,
        )

        if indices is None or len(indices) == 0:
            return detections

        # cv2 may return [[i], [j]] or [i, j]
        if isinstance(indices, (tuple, list, np.ndarray)) and len(np.asarray(indices).shape) == 2:
            indices = [int(i[0]) for i in indices]
        else:
            indices = [int(i) for i in np.asarray(indices).flatten()]

        for i in indices:
            x1i = int(max(0, min(w_orig - 1, round(x1[i]))))
            y1i = int(max(0, min(h_orig - 1, round(y1[i]))))
            x2i = int(max(0, min(w_orig - 1, round(x1[i] + w1[i]))))
            y2i = int(max(0, min(h_orig - 1, round(y1[i] + h1[i]))))

            if x2i <= x1i or y2i <= y1i:
                continue

            detections.append(
                {
                    "bbox": [x1i, y1i, x2i, y2i],
                    "confidence": float(scores_k[i]),
                    "class": int(cls_ids_k[i]),
                }
            )

        return detections
    
    def detect(self, image):
        """
        Detect FFBs in image.
        
        Args:
            image: Input image (BGR format, numpy array)
        
        Returns:
            List of detections with bbox, confidence, class
        """
        original_shape = image.shape
        img_input = self.preprocess_image(image)
        
        # Run inference
        if hasattr(self, 'session'):  # ONNX
            outputs = self.session.run(self.output_names, {self.input_name: img_input})
        else:  # TFLite
            self.interpreter.set_tensor(self.input_details[0]['index'], img_input)
            self.interpreter.invoke()
            outputs = [self.interpreter.get_tensor(output['index']) for output in self.output_details]
        
        # Post-process
        detections = self.postprocess_detections(outputs, original_shape)
        
        return detections
    
    def draw_detections(self, image, detections):
        """Draw bounding boxes on image."""
        img_with_boxes = image.copy()
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            conf = det['confidence']
            h, w = img_with_boxes.shape[:2]
            x1 = int(max(0, min(w - 1, x1)))
            y1 = int(max(0, min(h - 1, y1)))
            x2 = int(max(0, min(w - 1, x2)))
            y2 = int(max(0, min(h - 1, y2)))
            if x2 <= x1 or y2 <= y1:
                continue
            
            # Draw rectangle
            cv2.rectangle(img_with_boxes, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label
            label = f"FFB {conf:.2f}"
            cv2.putText(img_with_boxes, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return img_with_boxes

def test_with_camera():
    """Test inference with Odroid H3+ camera."""
    print("=" * 60)
    print("FFB DETECTION - ODROID H3+ CAMERA TEST")
    print("=" * 60)
    
    # Initialize model - try multiple possible paths
    model_path = None
    for path in ["ffb_yolo.onnx", "odroid_h3_deployment/ffb_yolo.onnx", "runs/detect/ffb_yolo/weights/best.onnx"]:
        if Path(path).exists():
            model_path = path
            break
    
    if model_path is None:
        print("[ERROR] Model not found. Please export model first using deploy_to_raspberry_pi.py")
        return
    
    print(f"Using model: {model_path}")
    
    detector = FFBYOLOInference(model_path, input_size=640, conf_threshold=0.25)
    
    # Initialize camera
    # For USB camera: camera = cv2.VideoCapture(0)
    # Odroid H3+ supports standard USB cameras
    try:
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("[ERROR] Could not open camera")
            return
    except Exception as e:
        print(f"[ERROR] Camera initialization failed: {e}")
        return
    
    print("\n[OK] Camera initialized")
    print("Press 'q' to quit, 's' to save current frame")
    
    frame_count = 0
    fps_times = []
    
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        
        # Run detection
        start_time = time.time()
        detections = detector.detect(frame)
        inference_time = time.time() - start_time
        fps_times.append(inference_time)
        
        # Draw detections
        frame_with_boxes = detector.draw_detections(frame, detections)
        
        # Display FPS
        fps = 1.0 / inference_time if inference_time > 0 else 0
        avg_fps = 1.0 / np.mean(fps_times[-30:]) if len(fps_times) > 0 else 0
        
        cv2.putText(frame_with_boxes, f"FPS: {fps:.1f} (avg: {avg_fps:.1f})", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame_with_boxes, f"Detections: {len(detections)}", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Show image
        cv2.imshow('FFB Detection', frame_with_boxes)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            filename = f"detection_{frame_count}.jpg"
            cv2.imwrite(filename, frame_with_boxes)
            print(f"[OK] Saved: {filename}")
        
        frame_count += 1
    
    camera.release()
    cv2.destroyAllWindows()
    
    print(f"\n[OK] Processed {frame_count} frames")
    if fps_times:
        print(f"Average inference time: {np.mean(fps_times)*1000:.1f}ms")
        print(f"Average FPS: {1.0/np.mean(fps_times):.1f}")

def test_with_image(image_path):
    """Test inference on a single image."""
    print(f"\nTesting on image: {image_path}")
    
    # Try multiple possible model paths
    model_path = None
    for path in ["ffb_yolo.onnx", "odroid_h3_deployment/ffb_yolo.onnx", "runs/detect/ffb_yolo/weights/best.onnx"]:
        if Path(path).exists():
            model_path = path
            break
    
    if model_path is None:
        print("[ERROR] Model not found. Please export model first using deploy_to_raspberry_pi.py")
        return
    detector = FFBYOLOInference(model_path, input_size=640)
    
    # Load image
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"[ERROR] Could not load image: {image_path}")
        return
    
    # Detect
    start_time = time.time()
    detections = detector.detect(image)
    inference_time = time.time() - start_time
    
    print(f"Detections: {len(detections)}")
    print(f"Inference time: {inference_time*1000:.1f}ms")
    
    for i, det in enumerate(detections):
        print(f"  FFB {i+1}: confidence={det['confidence']:.3f}, bbox={det['bbox']}")
    
    # Draw and save
    result = detector.draw_detections(image, detections)
    output_path = "detection_result.jpg"
    cv2.imwrite(output_path, result)
    print(f"[OK] Result saved to: {output_path}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Test on image
        test_with_image(sys.argv[1])
    else:
        # Test with camera
        test_with_camera()

