# Odroid H3+ Deployment Checklist

## Step 1: Export Models (Run on your computer)

Run the export script to generate model files:
```bash
python deploy_to_raspberry_pi.py
```

This will create the `odroid_h3_deployment/` folder with:
- `ffb_yolo.onnx` ⭐ **RECOMMENDED - Use this one**
- `ffb_yolo.tflite` (alternative)
- `ffb_yolo.mlmodel` (alternative)
- `DEPLOYMENT_INSTRUCTIONS.md` (detailed guide)

## Step 2: Files to Transfer to Odroid H3+

### Required Files:
1. **Model file** (choose one):
   - `odroid_h3_deployment/ffb_yolo.onnx` ⭐ **Recommended**
   - OR `odroid_h3_deployment/ffb_yolo.tflite` (if ONNX doesn't work)

2. **Inference script**:
   - `raspberry_pi_inference.py` (works on Odroid H3+)

3. **Requirements file** (optional, for easy install):
   - `odroid_h3_requirements.txt`

### Transfer Command:
```bash
# Create directory on Odroid H3+ first (SSH into it)
# Then from your computer:
scp odroid_h3_deployment/ffb_yolo.onnx odroid@<IP_ADDRESS>:~/ffb_detector/
scp raspberry_pi_inference.py odroid@<IP_ADDRESS>:~/ffb_detector/
scp odroid_h3_requirements.txt odroid@<IP_ADDRESS>:~/ffb_detector/
```

Or use a USB drive/SD card to transfer files.

## Step 3: Setup on Odroid H3+

### SSH into Odroid H3+:
```bash
ssh odroid@<IP_ADDRESS>
```

### Install Dependencies:
```bash
cd ~/ffb_detector

# Install Python packages
pip3 install -r odroid_h3_requirements.txt

# Or install manually:
pip3 install onnxruntime opencv-python numpy pillow
```

## Step 4: Test the Model

### Test with an image:
```bash
python3 raspberry_pi_inference.py path/to/test_image.jpg
```

### Test with camera:
```bash
python3 raspberry_pi_inference.py
# Press 'q' to quit, 's' to save frame
```

## File Structure on Odroid H3+

```
~/ffb_detector/
├── ffb_yolo.onnx          # Model file
├── raspberry_pi_inference.py  # Inference script
├── odroid_h3_requirements.txt  # Dependencies
└── detection_result.jpg    # Output (after testing)
```

## Quick Summary

**Minimum files needed:**
- ✅ `ffb_yolo.onnx` (the model)
- ✅ `raspberry_pi_inference.py` (the script)

**That's it!** Everything else can be installed via pip.
