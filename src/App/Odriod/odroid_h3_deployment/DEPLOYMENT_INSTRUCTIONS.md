# Odroid H3+ Deployment Guide

## 1. Model Export
Models have been exported to this directory:
- ffb_yolo.onnx (Recommended for Odroid H3+)
- ffb_yolo.tflite (Alternative, smaller size)
- ffb_yolo.mlmodel (Alternative)

## 2. Transfer to Odroid H3+
```bash
# From your computer, copy models to Odroid H3+:
scp odroid_h3_deployment/ffb_yolo.onnx odroid@odroid.local:~/ffb_detector/
# Or use SCP with IP address:
scp odroid_h3_deployment/ffb_yolo.onnx odroid@<IP_ADDRESS>:~/ffb_detector/
```

## 3. Install Dependencies on Odroid H3+

### Option A: ONNX Runtime (Recommended)
```bash
# On Odroid H3+ (x86_64 - uses standard packages)
sudo apt update
sudo apt install python3-pip python3-dev
pip3 install onnxruntime opencv-python numpy pillow
# Note: Can use regular opencv-python (not headless) since H3+ has display support
```

### Option B: TensorFlow Lite
```bash
# For Odroid H3+ (x86_64), use full TensorFlow
pip3 install tensorflow opencv-python numpy pillow
```

## 4. Performance Optimization

### For Faster Inference:
1. Odroid H3+ can handle 640x640 input size well (better than Raspberry Pi)
2. Can reduce to 416x416 or 320x320 for faster inference if needed
3. Use ONNX Runtime with optimizations
4. Odroid H3+ has Intel N5105 CPU with better performance than Pi
5. Use USB 3.0 camera for faster image capture

### Expected Performance:
- Odroid H3+ (Intel N5105): ~50-150ms per image (ONNX, 640x640)
- With optimizations: Can achieve ~30-100ms
- Much faster than Raspberry Pi due to x86_64 architecture

## 5. Camera Setup
Connect USB camera (Odroid H3+ supports standard USB cameras)
Note: Odroid H3+ doesn't have a dedicated camera port like Raspberry Pi

## 6. Run Inference
See raspberry_pi_inference.py for example code (works on Odroid H3+)
