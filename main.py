import time
from tkinter import simpledialog, messagebox
import cv2
import cvzone
import pandas as pd
import pyautogui
from ultralytics import YOLO
from vidgear.gears import CamGear

from tracker import *


def RGB(event, x, y, _, __):
    global click_counter
    if event == cv2.EVENT_LBUTTONDOWN:
        colorsBGR = [x, y]
        print(colorsBGR)
        match click_counter:
            case 0:
                line1[0] = colorsBGR
            case 1:
                line1[1] = colorsBGR
            case 2:
                line2[0] = colorsBGR
            case 3:
                line2[1] = colorsBGR
        pyautogui.press("space")

        click_counter = (click_counter + 1) % 4


def setup():
    # set desired quality as 360p
    setup_stream = CamGear(source=source, stream_mode=True, logging=False).start()
    cv2.namedWindow('SetUp')
    cv2.setMouseCallback('SetUp', RGB)
    setup_count = 0
    # Draw the lines
    while True:
        setup_frame = setup_stream.read()
        setup_count += 1
        if setup_count % 2 != 0:
            continue
        setup_frame = cv2.resize(setup_frame, (1020, 500))
        cv2.line(setup_frame, line1[0], line1[1], (255, 255, 255), 1)
        cv2.line(setup_frame, line2[0], line2[1], (255, 255, 255), 1)
        cvzone.putTextRect(setup_frame, 'Line1', (line1[0][0], line1[0][1]), 1, 1)
        cvzone.putTextRect(setup_frame, 'Line2', (line2[0][0], line2[0][1]), 1, 1)
        cv2.imshow("SetUp", setup_frame)
        if cv2.waitKey(0) & 0xFF == 27:
            break
    # Define the distance between the lines
    distance = simpledialog.askfloat("Distance Measurement",
                                     "What is the distance between the lines (in meters)?")
    setup_stream.stop()
    cv2.destroyAllWindows()
    return distance


# Model init
model = YOLO('yolov8s.pt')
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
tracker = Tracker()

# Starting parameters
line1 = [(366, 225), (643, 225)]
line2 = [(320, 301), (714, 301)]
start_time = {}
elapsed_time = {}
click_counter = 0
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
    meter = setup()
else:
    meter = 13
stream = CamGear(source=source, stream_mode=True, logging=False).start()
cv2.namedWindow('Speed camera')
# Calculate the equations of the lines
m1 = (line1[1][1] - line1[0][1]) / (line1[1][0] - line1[0][0])
n1 = line1[0][1] - m1 * line1[0][0]
m2 = (line2[1][1] - line2[0][1]) / (line2[1][0] - line2[0][0])
n2 = line2[0][1] - m2 * line2[0][0]

while True:
    frame = stream.read()
    # Act every second frame to improve latency
    count += 1
    if count % 4 != 0:
        continue
    objects = []
    frame = cv2.resize(frame, (1020, 500))

    # Detect the objects in the frame using the model
    results = model.predict(frame, verbose=False)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")

    # Draw the lines
    cv2.line(frame, line1[0], line1[1], (255, 255, 255), 1)
    cv2.line(frame, line2[0], line2[1], (255, 255, 255), 1)
    cvzone.putTextRect(frame, 'Line1', (line1[0][0], line1[0][1]), 1, 1)
    cvzone.putTextRect(frame, 'Line2', (line2[0][0], line2[0][1]), 1, 1)

    # Go through the objects and store only busses, trucks and cars
    for index, row in px.iterrows():
        c = class_list[int(row[5])]
        if 'car' in c:
            objects.append([int(row[0]), int(row[1]), int(row[2]), int(row[3])])

    # Monitor the items and determine whether any of them were recognized in the preceding frame.
    bbox_idx = tracker.update(objects)

    for bbox in bbox_idx:
        x1, y1, x2, y2, id_num = bbox
        cx = int(x1 + x2) // 2
        cy = int(y1 + y2) // 2

        # Calculate the distance of the center point from each line
        d1 = abs((m1 * cx - cy + n1) / math.sqrt(m1 * m1 + 1))
        d2 = abs((m2 * cx - cy + n2) / math.sqrt(m2 * m2 + 1))
        if d1 < 10:
            if id_num not in start_time:
                start_time[id_num] = (time.perf_counter(), d1, False)
            elif not start_time[id_num][2] and start_time[id_num][1] >= d1:
                start_time[id_num] = (time.perf_counter(), d1, False)
            elif start_time[id_num][2]:
                if start_time[id_num][1] >= d1 or not start_time[id_num][1]:
                    elapsed_time[id_num] = time.perf_counter() - start_time[id_num][0]
                    start_time[id_num] = (start_time[id_num][0], d1, start_time[id_num][2])
        if d2 < 10:
            if id_num not in start_time:
                start_time[id_num] = (time.perf_counter(), False, d2)
            elif not start_time[id_num][1] and start_time[id_num][2] >= d2:
                start_time[id_num] = (time.perf_counter(), False, d2)
            elif start_time[id_num][1]:
                if start_time[id_num][2] >= d2 or not start_time[id_num][2]:
                    elapsed_time[id_num] = time.perf_counter() - start_time[id_num][0]
                    start_time[id_num] = (start_time[id_num][0], start_time[id_num][1], d2)

        # Draw a dot in the middle of the object, rectangle around it, and id num aside it
        cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
        cvzone.putTextRect(frame, f'{id_num}', (x1, y1), 1, 1)
        # If speed could be calculated then add it to the video
        if id_num in elapsed_time:
            speed = int(3.6 * meter / elapsed_time[id_num])
            cv2.putText(frame, str(speed) + ' km/h', (x2, y2), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
    cv2.imshow("Speed camera", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()
