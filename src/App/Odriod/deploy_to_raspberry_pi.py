#!/usr/bin/env python3
"""
Deploy YOLO model to Odroid H3+ - Optimization and Export Guide
"""

from ultralytics import YOLO
from pathlib import Path

# Configuration
MODEL_PATH = "runs/detect/ffb_yolo/weights/best.pt"
OUTPUT_DIR = Path("odroid_h3_deployment")

def export_for_odroid_h3():
    """
    Export YOLO model in formats optimized for Odroid H3+.
    """
    print("=" * 60)
    print("EXPORTING YOLO MODEL FOR ODROID H3+")
    print("=" * 60)
    
    # Load model
    print(f"\nLoading model: {MODEL_PATH}")
    model = YOLO(MODEL_PATH)
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # 1. Export to ONNX (recommended for Odroid H3+)
    print("\n[1/3] Exporting to ONNX format...")
    try:
        onnx_path = model.export(
            format='onnx',
            imgsz=640,  # Odroid H3+ can handle 640x640 well (can reduce to 416 for faster inference)
            simplify=True,  # Simplify ONNX model
            opset=12  # ONNX opset version
        )
        print(f"[OK] ONNX model saved to: {onnx_path}")
        
        # Copy to output directory
        import shutil
        shutil.copy(onnx_path, OUTPUT_DIR / "ffb_yolo.onnx")
        print(f"[OK] Copied to: {OUTPUT_DIR / 'ffb_yolo.onnx'}")
    except Exception as e:
        print(f"[ERROR] ONNX export failed: {e}")
    
    # 2. Export to TensorFlow Lite (for edge devices)
    print("\n[2/3] Exporting to TensorFlow Lite format...")
    try:
        tflite_path = model.export(
            format='tflite',
            imgsz=640,  # Odroid H3+ can handle larger sizes (can reduce to 416 for faster inference)
            int8=True  # Quantization for smaller model size
        )
        print(f"[OK] TFLite model saved to: {tflite_path}")
        
        import shutil
        shutil.copy(tflite_path, OUTPUT_DIR / "ffb_yolo.tflite")
        print(f"[OK] Copied to: {OUTPUT_DIR / 'ffb_yolo.tflite'}")
    except Exception as e:
        print(f"[WARNING] TFLite export failed (may need TensorFlow): {e}")
    
    # 3. Export to CoreML (for Apple devices, but also works on some Pi setups)
    print("\n[3/3] Exporting to CoreML format...")
    try:
        coreml_path = model.export(
            format='coreml',
            imgsz=416
        )
        print(f"[OK] CoreML model saved to: {coreml_path}")
        
        import shutil
        shutil.copy(coreml_path, OUTPUT_DIR / "ffb_yolo.mlmodel")
        print(f"[OK] Copied to: {OUTPUT_DIR / 'ffb_yolo.mlmodel'}")
    except Exception as e:
        print(f"[WARNING] CoreML export failed: {e}")
    
    # Create deployment instructions
    create_deployment_instructions()
    
    print("\n" + "=" * 60)
    print("EXPORT COMPLETE")
    print("=" * 60)
    print(f"\nModels saved to: {OUTPUT_DIR}")
    print("\nNext steps:")
    print("1. Copy exported model to Odroid H3+")
    print("2. Install required dependencies on Odroid H3+")
    print("3. Use inference script (see raspberry_pi_inference.py)")

def create_deployment_instructions():
    """Create deployment instructions file."""
    instructions = """# Odroid H3+ Deployment Guide

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
"""
    
    with open(OUTPUT_DIR / "DEPLOYMENT_INSTRUCTIONS.md", 'w') as f:
        f.write(instructions)
    
    print(f"\n[OK] Deployment instructions saved to: {OUTPUT_DIR / 'DEPLOYMENT_INSTRUCTIONS.md'}")

if __name__ == "__main__":
    export_for_odroid_h3()

