<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:203a43,100:2c5364&height=180&section=header&text=Speed%20Camera&fontSize=40&fontColor=ffffff&fontAlignY=36&animation=fadeIn&desc=Vehicle%20detection%2C%20tracking%20and%20speed%20estimation&descSize=15&descAlignY=58" width="100%" />

**A speed camera built on YOLOv8 object detection and a custom tracker**

<img src="https://img.shields.io/badge/Python-30363d?style=for-the-badge&logo=python&logoColor=FFD43B" />
<img src="https://img.shields.io/badge/YOLOv8-30363d?style=for-the-badge&logo=yolo&logoColor=00FFFF" />
<img src="https://img.shields.io/badge/OpenCV-30363d?style=for-the-badge&logo=opencv&logoColor=5C3EE8" />

</div>

<br/>

<p align="center">
  <img src="SpeedCamera-1-Thumbnail.jpg" width="80%" alt="Speed camera demo" />
</p>

> [!NOTE]
> Point it at any video stream, draw your own speed lines, and it detects, tracks and measures the speed of every vehicle.

## ✨ Features

| | Feature | |
|:-:|---|---|
| 📹 | **Any video source** | Plug in your own stream URL (CamGear) |
| 📏 | **Your own speed lines** | Mark the lines used for speed measurement to fit any road |
| 🎯 | **Custom tracker** | Assigns and updates IDs per vehicle, matches them across frames and drops them when they leave |
| ⏱️ | **Live speed** | Speed from distance and time between lines, drawn on the video |

<p align="center">
  <img src="Speed-camera.png" width="70%" alt="Speed lines setup" />
</p>

## 🚀 Get started

1. Download YOLOv8 weights (e.g. `yolov8s.pt`) into the project folder.
2. Run:

```bash
python main.py
```

3. Follow the prompts to set the video source and draw the speed lines.

## 🗂️ Structure

| File | Role |
|---|---|
| [`main.py`](main.py) | Runs the pipeline: setup, detection, tracking and display |
| [`setup.py`](setup.py) | Prompts for the video URL and the speed lines |
| [`tracker.py`](tracker.py) | Vehicle tracking and ID management |
| [`speed_check.py`](speed_check.py) | `SpeedCheck` class: speed from line crossings |
| [`draw.py`](draw.py) | Drawing lines and labels on frames |
| [`coco.txt`](coco.txt) | COCO class names |

## 🙏 Built with

[YOLOv8](https://github.com/ultralytics/ultralytics) (Ultralytics) · [CamGear](https://github.com/abhiTronix/vidgear) (VidGear) · [OpenCV](https://opencv.org/) · [cvzone](https://github.com/cvzone/cvzone)

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2c5364,50:203a43,100:0f2027&height=100&section=footer" width="100%" />
