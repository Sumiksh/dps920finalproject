# motion_detector.py
"""
Motion detection functions for the sports video analysis project.
"""

import cv2
import numpy as np

def detect_motion(frames, frame_idx, threshold=25, min_area=100):
    """
    Detect motion in the current frame by comparing with previous frame.

    Args:
        frames: List of video frames
        frame_idx: Index of the current frame
        threshold: Threshold for frame difference detection
        min_area: Minimum contour area to consider

    Returns:
        List of bounding boxes for detected motion regions
    """
    # We need at least 2 frames to detect motion
    if frame_idx < 1 or frame_idx >= len(frames):
        return []

    # Get current and previous frame
    current_frame = frames[frame_idx]
    prev_frame = frames[frame_idx - 1]

    # TODO: Implement motion detection
    # 1. Convert frames to grayscale
    # 2. Apply Gaussian blur to reduce noise (hint: cv2.GaussianBlur)
    # 3. Calculate absolute difference between frames (hint: cv2.absdiff)
    # 4. Apply threshold to highlight differences (hint: cv2.threshold)
    # 5. Dilate the thresholded image to fill in holes (hint: cv2.dilate)
    # 6. Find contours in the thresholded image (hint: cv2.findContours)
    # 7. Filter contours by area and extract bounding boxes

   # 1. Convert frames to grayscale
    gray_curr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    gray_prev = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # 2. Apply Gaussian blur to reduce noise
    # (fixed kernel per assignment hint; do not change function signature)
    blur_ksize = (5, 5)
    gray_curr = cv2.GaussianBlur(gray_curr, blur_ksize, 0)
    gray_prev = cv2.GaussianBlur(gray_prev, blur_ksize, 0)

    # 3. Calculate absolute difference between frames
    diff = cv2.absdiff(gray_prev, gray_curr)

    # 4. Apply threshold to highlight differences
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    print("thresh",thresh)

    # 5. Dilate the thresholded image to fill in holes
    kernel = np.ones((3, 3), dtype=np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=2)
    print("new thresh",thresh)

    # 6. Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Example starter code:
    motion_boxes = []
    for cnt in contours:
        if cv2.contourArea(cnt) < min_area:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        motion_boxes.append((x, y, w, h))
    # Your implementation here
    print("motion_boxes", motion_boxes)
    return motion_boxes