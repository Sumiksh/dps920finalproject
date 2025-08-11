# visualizer.py
"""
Visualization functions for displaying motion detection and viewport tracking results.
"""

import os
import cv2
import numpy as np


def visualize_results(frames, motion_results, viewport_positions, viewport_size, output_dir):
    """
    Create visualization of motion detection and viewport tracking results.

    Args:
        frames: List of video frames
        motion_results: List of motion detection results for each frame
        viewport_positions: List of viewport center positions for each frame
        viewport_size: Tuple (width, height) of the viewport
        output_dir: Directory to save visualization results
    """
    # Create output directory for frames
    frames_dir = os.path.join(output_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    print("frames directory:", frames_dir)

    viewport_dir = os.path.join(output_dir, "viewport")
    os.makedirs(viewport_dir, exist_ok=True)

    # Get dimensions for the output video
    height, width = frames[0].shape[:2]

    # Create video writers
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_path = os.path.join(output_dir, "motion_detection.mp4")
    video_writer = cv2.VideoWriter(video_path, fourcc, 5, (width, height))

    viewport_video_path = os.path.join(output_dir, "viewport_tracking.mp4")
    vp_width, vp_height = viewport_size
    viewport_writer = cv2.VideoWriter(
        viewport_video_path, fourcc, 5, (vp_width, vp_height)
    )

    # Implement visualization
    for i, frame in enumerate(frames):
        # a) Create a copy of the frame for visualization
        vis = frame.copy()

        # b) Draw bounding boxes around motion regions (green)
        if i < len(motion_results):
            boxes = motion_results[i]
        else:
            boxes = []
        for (x, y, w, h) in boxes:
            cv2.rectangle(vis, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # c) Draw the viewport rectangle (blue)
        # Determine viewport center for this frame; fall back to center if missing
        if i < len(viewport_positions):
            cx, cy = viewport_positions[i]
        else:
            cx, cy = (width // 2, height // 2)

        half_w = vp_width // 2
        half_h = vp_height // 2

        # Clamp center so the viewport stays inside image bounds
        # Clamp horizontally
        if cx < half_w:
            cx = half_w
        elif cx > (width - half_w):
            cx = width - half_w

        # Clamp vertically
        if cy < half_h:
            cy = half_h
        elif cy > (height - half_h):
            cy = height - half_h

        # Compute viewport rectangle
        x1 = cx - half_w
        y1 = cy - half_h
        x2 = x1 + vp_width
        y2 = y1 + vp_height

        # Safety clamp (handles odd sizes / edge cases)
        x1 = max(0, min(x1, width - vp_width))
        y1 = max(0, min(y1, height - vp_height))
        x2 = x1 + vp_width
        y2 = y1 + vp_height

        cv2.rectangle(vis, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # d) Extract the viewport content (crop)
        crop = frame[y1:y2, x1:x2].copy()

        # e) Add frame number to the visualization
        cv2.putText(
            vis,
            f"Frame {i+1}/{len(frames)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        # f) Save visualization frames and viewport frames as images
        cv2.imwrite(os.path.join(frames_dir, f"frame_{i:04d}.jpg"), vis)
        cv2.imwrite(os.path.join(viewport_dir, f"viewport_{i:04d}.jpg"), crop)

        # g) Write frames to both video writers
        video_writer.write(vis)
        viewport_writer.write(crop)

    # 2) Release the video writers when done
    video_writer.release()
    viewport_writer.release()

    print(f"Visualization saved to {video_path}")
    print(f"Viewport video saved to {viewport_video_path}")
    print(f"Individual frames saved to {frames_dir} and {viewport_dir}")
