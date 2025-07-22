"""Generate `NUM_MARKERS` aruco markers and save them in this folder under the
filenames `aruco_marker_*.png`. Also create a PDF called
`aruco_markers_labeled.pdf` containing all the generated aruco markers with the
size `PDF_MARKER_SIZE_CM` and a label below to easily print them.

Run this using uv: `uv run --script create_aruco_markers.py`
"""

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "numpy",
#     "opencv-contrib-python",
#     "fpdf",
# ]
# ///

import os
from pathlib import Path

import cv2
import numpy as np
from fpdf import FPDF

# === CONSTANTS ===
# TODO: Turn this into a command line script
MARKER_SIZE_PX = 1000  # Marker image size in pixels
NUM_MARKERS = 8  # Number of unique markers to generate
PDF_MARKER_SIZE_CM = 10  # Marker size on PDF in centimeters

CREATE_PDF = True
DELETE_IMAGES = True

if DELETE_IMAGES and not CREATE_PDF:
    raise ValueError("The images can't be deleted when no PDF will be created.")

BASE_PATH = Path(__file__).parent.resolve()
print(f"Base path: {BASE_PATH}")

# === ARUCO DICTIONARY ===
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

# === GENERATE MARKERS AND SAVE AS PNG ===
marker_images = []
for marker_id in range(NUM_MARKERS):
    marker_img = np.zeros((MARKER_SIZE_PX, MARKER_SIZE_PX), dtype=np.uint8)
    cv2.aruco.generateImageMarker(aruco_dict, marker_id, MARKER_SIZE_PX, marker_img, 1)
    image_path = BASE_PATH / f"aruco_marker_{marker_id}.png"
    cv2.imwrite(image_path, marker_img)
    marker_images.append(image_path)
    print(f"Saved {image_path}")

# === CREATE PDF WITH EACH MARKER CENTERED AND LABELLED ===
if CREATE_PDF:
    pdf_output_path = BASE_PATH / "aruco_markers_labeled.pdf"
    if os.path.exists(pdf_output_path):
        os.remove(pdf_output_path)
    pdf = FPDF(unit="cm", format="A4")
    pdf.set_font("Arial", "B", 16)
    for marker_id, img_path in enumerate(marker_images):
        pdf.add_page()
        x = (21 - PDF_MARKER_SIZE_CM) / 2  # A4 width is 21cm
        y = (29.7 - PDF_MARKER_SIZE_CM) / 2  # A4 height is 29.7cm
        pdf.image(str(img_path), x=x, y=y, w=PDF_MARKER_SIZE_CM, h=PDF_MARKER_SIZE_CM)
        label_y = y + PDF_MARKER_SIZE_CM + 0.5  # 0.5 cm below the image
        pdf.set_xy(x, label_y)
        # Label with both marker ID and filename
        pdf.cell(PDF_MARKER_SIZE_CM, 1, f"Marker ID: {marker_id} ({img_path.stem})", align="C")

    pdf.output(pdf_output_path)
    print(f"PDF saved as {pdf_output_path}")
else:
    print("No PDF was created.")

# === DELETE IMAGES ===
if DELETE_IMAGES:
    for img_path in marker_images:
        os.remove(img_path)
        print(f"Removed {img_path}")
