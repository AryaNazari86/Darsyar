import cv2
import numpy as np
from pdf2image import convert_from_path
import os

# Convert PDF to images
def pdf_to_images(pdf_path, output_folder, poppler_path):
    pages = convert_from_path(pdf_path, poppler_path=poppler_path)
    image_paths = []
    for i, page in enumerate(pages):
        image_path = os.path.join(output_folder, f'page_{i + 1}.png')
        page.save(image_path, 'PNG')
        image_paths.append(image_path)
    return image_paths

# Detect lines using Hough Line Transform and cut images based on them
def detect_and_cut_lines(image_path, output_folder, min_line_length, angle_tolerance, min_segment_height):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape

    # Apply binary thresholding
    _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)

    # Use Canny Edge Detection
    edges = cv2.Canny(binary, 50, 150, apertureSize=3)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=min_line_length, maxLineGap=10)
    
    if lines is None:
        print(f"No lines detected in {image_path}")
        return

    # Filter lines based on angle tolerance
    filtered_lines = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            if abs(angle) <= angle_tolerance:
                filtered_lines.append((x1, y1, x2, y2))
    
    # Sort y positions of the lines
    y_positions = sorted(set([min(y1, y2) for x1, y1, x2, y2 in filtered_lines]))

    # Add the top and bottom of the image as potential cut positions
    y_positions = [0] + y_positions + [height]

    # Save each segment
    base_filename = os.path.basename(image_path).split('.')[0]
    for i in range(len(y_positions) - 1):
        y1, y2 = y_positions[i], y_positions[i + 1]
        segment_height = y2 - y1
        if segment_height > min_segment_height:  # Save only segments with height greater than the minimum height
            segment = img[y1:y2, :]
            segment_path = os.path.join(output_folder, f'{base_filename}_segment_{i + 1}.png')
            cv2.imwrite(segment_path, segment)

# Main function to convert and process PDF
def process_pdf(pdf_path, output_folder, poppler_path, min_line_length, angle_tolerance, min_segment_height):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_paths = pdf_to_images(pdf_path, output_folder, poppler_path)
    for image_path in image_paths:
        detect_and_cut_lines(image_path, output_folder, min_line_length, angle_tolerance, min_segment_height)

# Example usage
pdf_path = './a.pdf'
output_folder = './output_images'
poppler_path = r'D:\proppler\poppler-24.07.0\Library\bin'  # Update this path to the location of your Poppler bin directory
min_line_length = 400  # Set the minimum line length to filter short lines
angle_tolerance = 25  # Set the angle tolerance to detect slightly tilted horizontal lines
min_segment_height = 70  # Set the minimum height for segments to be saved
process_pdf(pdf_path, output_folder, poppler_path, min_line_length, angle_tolerance, min_segment_height)
