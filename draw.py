import cv2
import cvzone


def draw_lines(frame, line1, line2):
    """
    Draws two lines on the given frame and adds labels for each line.

     Parameters:
        - frame (numpy.ndarray): The input image frame.
        - line1 (tuple): Coordinates of the first line as ((x1, y1), (x2, y2)).
        - line2 (tuple): Coordinates of the second line as ((x1, y1), (x2, y2)).
    """
    cv2.line(frame, line1[0], line1[1], (255, 255, 255), 1)
    cv2.line(frame, line2[0], line2[1], (255, 255, 255), 1)
    cvzone.putTextRect(frame, 'Line1', (line1[0][0], line1[0][1] + 20), 1, 1)
    cvzone.putTextRect(frame, 'Line2', (line2[0][0], line2[0][1] + 20), 1, 1)


def draw_object_info(frame, x1, y1, x2, y2, id_num, speed, cx, cy):
    """
    Draws information about a detected object on the given frame.

    Parameters:
        - frame (numpy.ndarray): The input image frame.
        - x1, y1, x2, y2 (int): Coordinates of the rectangle bounding the object.
        - id_num (int): ID number of the detected object.
        - speed (SpeedCheck): SpeedCheck instance containing final_speed information.
        - cx, cy (int): Coordinates of the center of the detected object.
    """
    # Draw a dot in the middle of the object, rectangle around it, and id_number num aside it
    cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
    cvzone.putTextRect(frame, f'{id_num}', (x1, y1), 1, 1)

    # If speed could be calculated then add it to the video
    if id_num in speed.final_speed:
        cv2.putText(frame, str(speed.final_speed[id_num]) + ' km/h', (x2, y2), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                    (255, 255, 255), 2)
