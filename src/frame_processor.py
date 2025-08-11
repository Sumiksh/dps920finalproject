# frame_processor.py
"""
Frame processing functions for the motion detection project.
"""

import cv2
import numpy as np


def process_video(video_path, target_fps=5, resize_dim=(1280, 720)):
    """
    Extract frames from a video at approximately target_fps and resize them.

    Args:
        video_path: Path to the video file
        target_fps: Target frames per second to extract
        resize_dim: Dimensions to resize frames to (width, height)

    Returns:
        List of extracted frames (BGR np.ndarray)
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {video_path}")

    # Source FPS from metadata (fallback to 30 if missing/invalid)
    src_fps = cap.get(cv2.CAP_PROP_FPS)
    if src_fps is None or src_fps <= 0 or np.isnan(src_fps):
        src_fps = 30.0
    print("Frames per second (source):", src_fps)

    # Decide stride using simple if/else
    # If target_fps < src_fps -> skip frames to downsample
    # Else -> keep every frame
    if target_fps < src_fps:
        stride = round(src_fps / float(target_fps))
    else:
        stride = 1
    print("Sampling stride (keep 1 of every N frames):", stride)

    frames = []
    frame_index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Keep frame according to stride
        if frame_index % stride == 0:
            if resize_dim is not None:
                w, h = resize_dim
                frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_LINEAR)
            frames.append(frame)

        frame_index += 1

    cap.release()
    return frames
