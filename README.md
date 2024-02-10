# Speed Camera with Object Detection

## Overview

This project implements a speed camera using object detection techniques. It leverages the YOLOv8 model for object detection, CamGear for video streaming, and OpenCV for image processing. The system is designed to detect and track vehicles, calculate their speeds, and display the results on the video stream.

## Features

### 1. Customizable Video Source

Users have the flexibility to insert their own video source URL, allowing this speed camera system to be adapted for any camera setup. This feature enables users to monitor traffic from various sources beyond the provided example video.

### 2. User-Defined Speed Lines

Users can mark up their own speed lines, defining the specific regions for speed calculations. This customization allows for the adaptation of the system to diverse road configurations and user preferences.

### 3. Enhanced Tracker

The tracker module has been significantly improved with the following features:

- **Improved Object ID Assignment:** The tracker now utilizes a more robust algorithm to assign and update unique IDs to detected objects, ensuring accurate tracking even in challenging scenarios.
  
- **Efficient Object Matching:** Enhancements in object matching algorithms contribute to improved accuracy in identifying and tracking vehicles across consecutive frames.
  
- **Dynamic ID Management:** The tracker dynamically manages the assignment and removal of object IDs based on movement patterns, resulting in a more adaptive and reliable tracking system.

- **Streamlined Integration:** The tracker seamlessly integrates with the overall speed camera system, providing real-time updates on object positions and enabling accurate speed calculations.

These improvements collectively contribute to a more effective and responsive tracking system tailored for the specific demands of the speed camera application.

## Setup

Download the YOLOv8 model weights (e.g., yolov8s.pt) and place them in the project directory.

Run the main script

## Dependencies
YOLOv8
CamGear
OpenCV
cvzone
License


## Acknowledgments
YOLOv8 - Ultralytics
CamGear - AbhiTronix
OpenCV - OpenCV team
cvzone - Augmented Startups

## Contributing
Feel free to contribute by opening issues or pull requests. Your feedback and suggestions are highly appreciated!
