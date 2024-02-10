from tkinter import simpledialog

import cv2
import cvzone
import pyautogui
from vidgear.gears import CamGear


class setup:
    """
    This class facilitates the setup process for marking lines in the video stream and specifying the distance between them.
    It uses the CamGear library for streaming, OpenCV for drawing lines and displaying frames, and tkinter for user input.

    Attributes:
    - click_counter (int): Counter for mouse clicks during the line setup process.
    - source (str): Source for the video stream (e.g., URL or file path).
    - line1 (list): List containing two points defining the first line.
    - line2 (list): List containing two points defining the second line.
    - distance (float): Distance between the lines in meters.

    Methods:
    - __init__(self, source, line1, line2): Initializes the Setup instance with source, line1, and line2 parameters.
    - RGB(self, event, x, y, _, __): Callback function for handling mouse clicks to define line points.
    - set_pref(self): Sets up the environment for line marking and distance input.
    """

    def __init__(self, source, line1, line2):
        """
            Initializes the Setup instance with source, line1, and line2 parameters.

            Args:
                - source (str): Source for the video stream (e.g., URL or file path).
                - line1 (list): List containing two points defining the first line.
                - line2 (list): List containing two points defining the second line.
        """
        self.click_counter = 0
        self.source = source
        self.line1 = line1
        self.line2 = line2
        self.distance = 0
        self.set_pref()

    def RGB(self, event, x, y, _, __):
        """
            Callback function for handling mouse clicks to define line points.

            Args:
                - event: The type of mouse event (e.g., cv2.EVENT_LBUTTONDOWN).
                - x (int): x-coordinate of the mouse click.
                - y (int): y-coordinate of the mouse click.
                - _: Additional parameters (not used).
                - __: Additional parameters (not used).
        """
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
        """
            Sets up the environment for line marking and distance input.
        """
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
