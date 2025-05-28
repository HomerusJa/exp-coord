"""Generate four aruco markers and save them in this folder under the filenames aruco_marker_*.png

Run this using uv: `uv run --script create_aruco_markers.py`
"""

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "numpy",
#     "opencv-contrib-python",
# ]
# ///

import cv2
import numpy as np

# Select the ArUco dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

# Set marker size in pixels (e.g., 1000 px for high-res printing)
marker_size_px = 1000

# Generate and save eight unique markers (IDs 0-7)
for marker_id in range(8):
    marker_img = np.zeros((marker_size_px, marker_size_px), dtype=np.uint8)
    cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size_px, marker_img, 1)
    filename = f"aruco_marker_{marker_id}.png"
    cv2.imwrite(filename, marker_img)
    print(f"Saved {filename}")

print("All markers generated and saved.")
