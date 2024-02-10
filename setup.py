from tkinter import simpledialog

import cv2
import cvzone
import pyautogui
from vidgear.gears import CamGear


class setup:
    def __init__(self, source, line1, line2):
        self.click_counter = 0
        self.source = source
        self.line1 = line1
        self.line2 = line2
        self.distance = 0
        self.set_pref()

    def RGB(self, event, x, y, _, __):
        if event == cv2.EVENT_LBUTTONDOWN:
            colorsBGR = [x, y]
            print(colorsBGR)
            match self.click_counter:
                case 0:
                    self.line1[0] = colorsBGR
                case 1:
                    self.line1[1] = colorsBGR
                case 2:
                    self.line2[0] = colorsBGR
                case 3:
                    self.line2[1] = colorsBGR
            pyautogui.press("space")
            self.click_counter = (self.click_counter + 1) % 4

    def set_pref(self):
        setup_stream = CamGear(source=self.source, stream_mode=True, logging=False).start()
        cv2.namedWindow('SetUp')
        cv2.setMouseCallback('SetUp', self.RGB)
        setup_count = 0
        # Draw the lines
        while True:
            setup_frame = setup_stream.read()
            setup_count += 1
            if setup_count % 2 != 0:
                continue
            setup_frame = cv2.resize(setup_frame, (1020, 500))
            cv2.line(setup_frame, self.line1[0], self.line1[1], (255, 255, 255), 1)
            cv2.line(setup_frame, self.line2[0], self.line2[1], (255, 255, 255), 1)
            cvzone.putTextRect(setup_frame, 'Line1', (self.line1[0][0], self.line1[0][1]+20), 1, 1)
            cvzone.putTextRect(setup_frame, 'Line2', (self.line2[0][0], self.line2[0][1]+20), 1, 1)
            cv2.imshow("SetUp", setup_frame)
            if cv2.waitKey(0) & 0xFF == 27:
                break
        # Define the distance between the lines
        self.distance = simpledialog.askfloat("Distance Measurement",
                                              "What is the distance between the lines (in meters)?")
        setup_stream.stop()
        cv2.destroyAllWindows()
