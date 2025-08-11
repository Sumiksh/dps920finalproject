# Sports Motion Detection & Tracking

This project implements a system for detecting motion in sports videos and visualizes a viewport that follows the action. It is useful for automating analysis or focusing on the most interesting parts (ROI) of sport videos.

## File: `main.py`

**Purpose:**  
Serves as the **entry point** for the Sports Motion Detection & Viewport Tracking pipeline. It orchestrates the complete process — parsing inputs, extracting frames, detecting motion, tracking the viewport, and visualizing results.

---

### Functions Overview

#### 1. `parse_args()`
**Description:**  
Parses command-line arguments to configure the pipeline.

**Returns:**  
- An `argparse.Namespace` object containing:
  - `video` (str): Path to input video file (required).  
  - `output` (str): Output directory for results (default: `output`).  
  - `fps` (int): Target frames per second for processing (default: 5).  
  - `viewport_size` (str): Size of the viewport in `WIDTHxHEIGHT` format (default: `"720x480"`).  

---

#### 2. `main()`
**Description:**  
Main function to execute the processing steps in sequence.

**Workflow:**  
1. **Parse command-line arguments** via `parse_args()`.  
2. **Validate and parse viewport size**, falling back to `720x480` if invalid.  
3. **Create the output directory** if it doesn't exist.  
4. **Extract frames from the video** using `process_video()` from `frame_processor.py`.  
5. **Detect motion in each frame** using `detect_motion()` from `motion_detector.py`.  
6. **Track viewport positions** over time based on motion detection results using `track_viewport()` from `viewport_tracker.py`.  
7. **Visualize and save results** (annotated frames, viewport videos, cropped viewport frames) using `visualize_results()` from `visualizer.py`.  
8. **Print completion message** once processing is complete.  

**Returns:**  
- None (side effects: writes images/videos to disk).  

---
### Execution Command Example
python main.py --video path/to/video.mp4 --output results --fps 5 --viewport_size 800x600


## File: `frame_processor.py`
## Overview
This module provides frame processing utilities for the motion detection project.  
It focuses on extracting frames from video files at a specified frame rate and resizing them to the desired dimensions.

---

## Functions

### `process_video(video_path, target_fps=5, resize_dim=(1280, 720))`
**Description:**  
Extracts frames from a given video file at approximately the specified frames per second and resizes them.

**Args:**
- `video_path` *(str)*: Path to the input video file.
- `target_fps` *(int, optional)*: Desired frames per second to extract (default: `5`).
- `resize_dim` *(tuple, optional)*: Target width and height for resizing frames (default: `(1280, 720)`).

**Returns:**
- *(list of np.ndarray)*: List of extracted frames in **BGR** format (as used by OpenCV).

**Details:**
- Reads video metadata to determine the source FPS.
- Calculates a sampling stride to match the target FPS.
- Resizes frames if `resize_dim` is provided.
- Returns frames suitable for further processing in motion detection.


## File: `motion_detector.py`
Provides functionality to detect motion between consecutive video frames and return bounding boxes around detected moving regions.

#### Functions:
- **`detect_motion(frames, min_area=500)`**
  - **Description:** Compares consecutive frames to detect motion by identifying regions with significant pixel changes.
  - **Args:**
    - `frames`: List of video frames.
    - `min_area`: Minimum area threshold for a contour to be considered motion.
  - **Returns:** List of lists containing bounding boxes `(x, y, w, h)` for each frame.

---

## File: `viewport_tracker.py`
Tracks a smooth "virtual camera" viewport following the largest detected motion region, with optional smoothing and clamping to frame boundaries.

#### Functions:
- **`calculate_region_of_interest(motion_boxes, frame_shape)`**
  - **Description:** Identifies the largest motion bounding box by area and returns its center coordinates and size.
  - **Args:**
    - `motion_boxes`: List of bounding boxes `(x, y, w, h)`.
    - `frame_shape`: Shape of the video frame `(height, width, channels)`.
  - **Returns:** `(cx, cy, w, h)` where `(cx, cy)` is the center of the largest motion box.

- **`track_viewport(frames, motion_results, viewport_size)`**
  - **Description:** Tracks the viewport position across frames using a cumulative moving average for smoothing, ensuring it stays within frame boundaries.
  - **Args:**
    - `frames`: List of video frames.
    - `motion_results`: List of motion detection results for each frame.
    - `viewport_size`: Tuple `(width, height)` for the viewport size.
  - **Returns:** List of `(x, y)` viewport center positions for each frame.

---

## File: `visualizer.py`
Generates visualizations for motion detection and viewport tracking, saving both annotated full frames and cropped viewport frames as images and videos.

#### Functions:
- **`visualize_results(frames, motion_results, viewport_positions, viewport_size, output_dir)`**
  - **Description:** Draws motion bounding boxes and viewport rectangles on frames, saves annotated frames and cropped viewport content, and writes two video files:
    - Motion detection visualization.
    - Viewport tracking output.
  - **Args:**
    - `frames`: List of video frames.
    - `motion_results`: List of bounding boxes per frame.
    - `viewport_positions`: List of `(x, y)` viewport center positions.
    - `viewport_size`: Tuple `(width, height)` for the viewport.
    - `output_dir`: Directory to save results.
  - **Outputs:** Images and MP4 videos saved under `output_dir`.








