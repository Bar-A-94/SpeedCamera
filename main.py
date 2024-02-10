from tkinter import simpledialog, messagebox

import pandas as pd
from ultralytics import YOLO
from vidgear.gears import CamGear

from draw import *
from setup import setup
from speed_check import *
from tracker import *


def detect_objects(frame, model, class_list):
    """
    Detects objects in the given frame using a pre-trained model.

    Parameters:
        - frame (numpy.ndarray): The input image frame.
        - model: The pre-trained object detection model.
        - class_list (list): List of class labels corresponding to the model output.

    Returns:
        list: A list of detected objects, where each object is represented as [x1, y1, x2, y2],
              denoting the bounding box coordinates of the object.
    """
    results = model.predict(frame, verbose=False)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    objects = []

    for index, row in px.iterrows():
        c = class_list[int(row[5])]
        if 'car' in c:
            objects.append([int(row[0]), int(row[1]), int(row[2]), int(row[3])])

    return objects


# Configuration Constants
FRAME_SKIP = 4
RESIZE_DIMENSIONS = (1020, 500)

# Model init
model = YOLO('yolov8s.pt')
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
tracker = Tracker()

# Starting parameters
line1 = [(260, 200), (715, 200)]
line2 = [(144, 301), (850, 301)]
count = 0

# Ask the user for his preference
# Set up the stream, speed lines and the distance between them
user_source = messagebox.askquestion("Set-up", "Do you want to enter your own video link?")
if user_source == "yes":
    source = simpledialog.askstring("Source", "Write down the link to your video")
else:
    source = 'https://www.youtube.com/watch?v=DnUFAShZKus'
user_lines = messagebox.askquestion("Set-up", "Do you want to mark your own speed lines?")
if user_lines == "yes":
    user_set = setup(source, line1, line2)
    line1 = user_set.line1
    line2 = user_set.line2
    meter = user_set.distance
else:
    meter = 17

# Prepare the speed check class
speed = speed_check(line1, line2, meter)

# Start streaming
stream = CamGear(source=source, stream_mode=True, logging=False).start()
cv2.namedWindow('Speed camera')

while True:
    frame = stream.read()
    # Act every fourth frame to improve latency
    count += 1
    if count % FRAME_SKIP != 0:
        continue
    frame = cv2.resize(frame, RESIZE_DIMENSIONS)

    # Monitor the items and determine whether any of them were recognized in the previous frames.
    objects = detect_objects(frame, model, class_list)
    bbox_idx = tracker.update(objects)

    for bbox in bbox_idx:
        x1, y1, x2, y2, id_num = bbox
        cx = int(x1 + x2) // 2
        cy = int(y1 + y2) // 2
        speed.check(id_num, cx, cy)
        draw_object_info(frame, x1, y1, x2, y2, id_num, speed, cx, cy)

    draw_lines(frame, line1, line2)
    cv2.imshow("Speed camera", frame)

    # Wait for escape to end the streaming
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
