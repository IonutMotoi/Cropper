# Cropper
A Python tool for non-overlapping patch (square) or bounding box selection and cropping from images, useful for data preparation in machine learning tasks.

## Instructions

### Prerequisites:
- Python
- OpenCV (cv2)

### Installation:
```
pip install -r requirements.txt
```
   
### Patch Cropper Usage:
```
python patch_cropper.py -i <path_to_images> -o <path_to_patches> -s <size_of_patches>
```
Replace placeholders:
- <path_to_images>: Directory containing your source images.
- <path_to_patches>: Desired output directory for cropped patches.
- <size_of_patches>: Pixel dimensions of the patches (e.g., 512 for 512x512).

### Bounding Box Cropper Usage:
```
python bbox_cropper.py -i <path_to_images> -o <path_to_bboxes>
```
Replace placeholders:
- <path_to_images>: Directory containing your source images.
- <path_to_bboxes>: Desired output directory for cropped bounding boxes.

## Commands
- Mouse:
  - `Hover`: Preview patch or bounding box area.
  - `Left click`: Draw a new patch or bounding box (non-overlapping only).
  - `Middle click`: Delete an existing patch or bounding box.
  - `Right click`: Cancel the current bounding box drawing (only for bounding box cropper).
 
- Keyboard:
  - `s`: Save crops from the drawn shapes.
  - `a`: Previous image.
  - `d`: Next image.
  - `q`: Quit the application.
