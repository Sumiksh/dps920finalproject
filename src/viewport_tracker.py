# viewport_tracker.py
"""
Viewport tracking functions for creating a smooth "virtual camera".
Uses a SIMPLE MOVING AVERAGE (SMA) for smoothing.
"""

import cv2
import numpy as np


def calculate_region_of_interest(motion_boxes, frame_shape):
    """
    Pick the primary region of interest (largest motion box by area).
    Returns (cx, cy, w, h) where (cx, cy) is the CENTER.
    """
    if not motion_boxes:
        h, w = frame_shape[:2]
        return (w // 2, h // 2, 0, 0)

    # Find largest box
    # print("motion_boxes are:",motion_boxes)
    largest_box = motion_boxes[0] # every frame start from 0th motion box which is some object 
    # print(largest_box , "largest_box")
    largest_area = largest_box[2] * largest_box[3] #largest box area
    for box in motion_boxes[1:]:
        x, y, bw, bh = box
        area = bw * bh
        if area > largest_area:
            largest_area = area
            largest_box = box
            # print("largest box in the loop" , largest_box)

    x, y, w_box, h_box = largest_box
    print("largest box", largest_box)
    cx = x + w_box // 2 # x y are coordinates of leftmost box and add the half of width and height we center point
    cy = y + h_box // 2
    # print("cx, cy, w_box, h_box", cx, cy, w_box, h_box)
    return (cx, cy, w_box, h_box)


def track_viewport(frames, motion_results, viewport_size):
    viewport_positions = []

    if not frames:
        return viewport_positions

    height, width = frames[0].shape[:2]
    vp_w, vp_h = viewport_size
    half_w = vp_w // 2
    half_h = vp_h // 2

    # Running totals for cumulative average
    total_x, total_y = 0, 0
    count = 0

    for i, frame in enumerate(frames):
        # Get motion boxes for this frame
        if i < len(motion_results):
            boxes = motion_results[i]
        else:
            boxes = []
        
        print("boxes",boxes)
        # Get current target center
        cx, cy, _, _ = calculate_region_of_interest(boxes, frame.shape)

        # Update running totals
        total_x += cx
        total_y += cy
        count += 1

        # Average so far
        sm_x = int(round(total_x / count))
        sm_y = int(round(total_y / count))
        # print("sm_x, sm_y",sm_x, sm_y)

        # Clamp horizontally
        if sm_x < half_w: # so if center average of largest box  x coordinate <  the center of the viewport
            sm_x = half_w
        elif sm_x > (width - half_w):
            sm_x = width - half_w

        # Clamp vertically
        if sm_y < half_h:
            sm_y = half_h
        elif sm_y > (height - half_h):
            sm_y = height - half_h

        viewport_positions.append((sm_x, sm_y))

    return viewport_positions
