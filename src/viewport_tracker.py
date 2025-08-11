# # # viewport_tracker.py
# # """
# # Viewport tracking functions for creating a smooth "virtual camera".
# # """

# # import cv2
# # import numpy as np


# # def calculate_region_of_interest(motion_boxes, frame_shape):
# #     """
# #     Calculate the primary region of interest based on motion boxes.

# #     Args:
# #         motion_boxes: List of motion detection bounding boxes
# #         frame_shape: Shape of the video frame (height, width)

# #     Returns:
# #         Tuple (x, y, w, h) representing the region of interest center point and dimensions
# #     """
# #     # TODO: Implement region of interest calculation
# #     # 1. Choose a strategy for determining the main area of interest
# #     #    - You could use the largest motion box
# #     #    - Or combine nearby boxes
# #     #    - Or use a weighted average of all motion boxes
# #     # 2. Return the coordinates of the chosen region

# #     # Example starter code:
# #     if not motion_boxes:
# #         # If no motion is detected, use the center of the frame
# #         height, width = frame_shape[:2]
# #         return (width // 2, height // 2, 0, 0)

# #     # Your implementation here

# #     return (0, 0, 0, 0)  # Placeholder


# # def track_viewport(frames, motion_results, viewport_size, smoothing_factor=0.3):
# #     """
# #     Track viewport position across frames with smoothing.

# #     Args:
# #         frames: List of video frames
# #         motion_results: List of motion detection results for each frame
# #         viewport_size: Tuple (width, height) of the viewport
# #         smoothing_factor: Factor for smoothing viewport movement (0-1)
# #                           Lower values create smoother movement

# #     Returns:
# #         List of viewport positions for each frame as (x, y) center coordinates
# #     """
# #     # TODO: Implement viewport tracking with smoothing
# #     # 1. For each frame, determine the region of interest based on motion_results
# #     # 2. Apply smoothing to avoid jerky movements
# #     #    - Use previous viewport positions to smooth the movement
# #     #    - Consider implementing a simple exponential moving average
# #     #    - Or a more advanced approach like Kalman filtering
# #     # 3. Ensure the viewport stays within the frame boundaries
# #     # 4. Return the list of viewport positions for all frames

# #     # Example starter code:
# #     viewport_positions = []

# #     # Initialize with center of first frame if available
# #     if frames:
# #         height, width = frames[0].shape[:2]
# #         prev_x, prev_y = width // 2, height // 2
# #     else:
# #         return []

# #     # Your implementation here

# #     return viewport_positions


# # viewport_tracker.py
# """
# Viewport tracking functions for creating a smooth "virtual camera".
# """

# import cv2
# import numpy as np


# def calculate_region_of_interest(motion_boxes, frame_shape):
#     """
#     Calculate the primary region of interest based on motion boxes.

#     Args:
#         motion_boxes: List of motion detection bounding boxes
#         frame_shape: Shape of the video frame (height, width)

#     Returns:
#         Tuple (x, y, w, h) representing the region of interest center point and dimensions
#         where (x, y) is the CENTER of the chosen region.
#     """
#     # 1) Strategy: choose the largest motion box by area as the primary region
#     if not motion_boxes:
#         # drops RGB channel
#         height, width = frame_shape[:2]
#         return (width // 2, height // 2, 0, 0)

#     # Find the largest box by area
#     areas = []
#     for box in motion_boxes:
#         _, _, w, h = box # drop x-y coordinates
#         areas.append(w * h) 

#     idx = int(np.argmax(areas)) #  finds the index of the largest area in areas
#     print("idx", idx)
#     x, y, w, h = motion_boxes[idx] # 

#     # Convert to center coordinates
#     cx = x + w // 2
#     cy = y + h // 2

#     # Return center + size
#     return (cx, cy, w, h)


# def track_viewport(frames, motion_results, viewport_size, smoothing_factor=0.3):
#     """
#     Track viewport position across frames with interpolation smoothing.
#     """
#     viewport_positions = []

#     if frames:
#         height, width = frames[0].shape[:2]
#         prev_x, prev_y = width // 2, height // 2
#     else:
#         return []

#     vp_w, vp_h = viewport_size
#     half_w = vp_w // 2
#     half_h = vp_h // 2
#     print(vp_w, vp_h)

#     for i, frame in enumerate(frames):
#         if i < len(motion_results):
#             boxes = motion_results[i]
#         else:
#             boxes = []
#         cx, cy, _, _ = calculate_region_of_interest(boxes, frame.shape)

#         # Interpolation smoothing
#         sm_x = int((1.0 - smoothing_factor) * prev_x + smoothing_factor * cx)
#         sm_y = int((1.0 - smoothing_factor) * prev_y + smoothing_factor * cy)

#         # Clamp to frame boundaries
#         sm_x = max(half_w, min(width - half_w, sm_x))
#         sm_y = max(half_h, min(height - half_h, sm_y))

#         viewport_positions.append((sm_x, sm_y))
#         prev_x, prev_y = sm_x, sm_y

#     return viewport_positions


# # def track_viewport(frames, motion_results, viewport_size, smoothing_factor=0.3):
# #     """
# #     Track viewport position across frames with smoothing.

# #     Args:
# #         frames: List of video frames
# #         motion_results: List of motion detection results for each frame
# #         viewport_size: Tuple (width, height) of the viewport
# #         smoothing_factor: Factor for smoothing viewport movement (0-1)
# #                           Lower values create smoother movement

# #     Returns:
# #         List of viewport positions for each frame as (x, y) center coordinates
# #     """
# #     viewport_positions = []

# #     # Initialize with center of first frame if available
# #     if frames:
# #         print("frames[0]:",frames[0].shape)
# #         height, width = frames[0].shape[:2]
# #         prev_x, prev_y = width // 2, height // 2
# #     else:
# #         return []

# #     # Ensure smoothing_factor is within [0,1]
# #     alpha = float(np.clip(smoothing_factor, 0.0, 1.0))

# #     vp_w, vp_h = viewport_size
# #     half_w = vp_w // 2
# #     half_h = vp_h // 2

# #     for i, frame in enumerate(frames):
# #         # 1) Determine region of interest for this frame
# #         boxes = motion_results[i] if i < len(motion_results) else []
# #         cx, cy, _, _ = calculate_region_of_interest(boxes, frame.shape)

# #         # 2) Apply smoothing (Exponential Moving Average)
# #         sm_x = int((1.0 - alpha) * prev_x + alpha * cx)
# #         sm_y = int((1.0 - alpha) * prev_y + alpha * cy)

# #         # 3) Ensure the viewport stays within the frame boundaries
# #         # Clamp the center so that the viewport rectangle [center ± half_size] is inside
# #         sm_x = max(half_w, min(width - half_w, sm_x))
# #         sm_y = max(half_h, min(height - half_h, sm_y))

# #         viewport_positions.append((sm_x, sm_y))

# #         # Update previous smoothed position
# #         prev_x, prev_y = sm_x, sm_y

# #     print("all viewport positions", viewport_positions)
# #     # 4) Return all viewport centers
# #     return viewport_positions


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
