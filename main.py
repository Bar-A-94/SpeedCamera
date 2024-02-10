from tkinter import simpledialog, messagebox

import cv2
import cvzone
import pandas as pd
from ultralytics import YOLO
from vidgear.gears import CamGear

from setup import setup
from speed_check import *
from tracker import *

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
    if count % 4 != 0:
        continue
    objects = []
    frame = cv2.resize(frame, (1020, 500))

    # Detect the objects in the frame using the model
    results = model.predict(frame, verbose=False)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")

    # Go through the objects and store only cars
    for index, row in px.iterrows():
        c = class_list[int(row[5])]
        if 'car' in c:
            objects.append([int(row[0]), int(row[1]), int(row[2]), int(row[3])])

    # Monitor the items and determine whether any of them were recognized in the previous frames.
    bbox_idx = tracker.update(objects)

    for bbox in bbox_idx:
        x1, y1, x2, y2, id_num = bbox
        cx = int(x1 + x2) // 2
        cy = int(y1 + y2) // 2
        speed.check(id_num, cx, cy)

        # Draw a dot in the middle of the object, rectangle around it, and id_number num aside it
        cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
        cvzone.putTextRect(frame, f'{id_num}', (x1, y1), 1, 1)

        # If speed could be calculated then add it to the video
        if id_num in speed.final_speed:
            cv2.putText(frame, str(speed.final_speed[id_num]) + ' km/h', (x2, y2), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                        (255, 255, 255), 2)

    # Draw the lines
    cv2.line(frame, line1[0], line1[1], (255, 255, 255), 1)
    cv2.line(frame, line2[0], line2[1], (255, 255, 255), 1)
    cvzone.putTextRect(frame, 'Line1', (line1[0][0], line1[0][1]+20), 1, 1)
    cvzone.putTextRect(frame, 'Line2', (line2[0][0], line2[0][1]+20), 1, 1)

    cv2.imshow("Speed camera", frame)

    # Wait for escape to end the streaming
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()
