import math
import time


class speed_check:
    """
        This class is responsible for calculating the speed of objects based on their crossing events across two lines.
        It utilizes the equations of the lines (y = mx + n) and calculates the distance from the center point of the object
        to each line. Speed is then calculated based on the time taken for the object to cross the distance.

        Attributes:
        - meter (float): The meter value representing the distance between the two lines.
        - m1, n1, m2, n2 (float): Coefficients for the equations of the lines representing crossing events.
        - start_time (dict): Dictionary to store the start time of objects crossing the lines.
        - elapsed_time (dict): Dictionary to store the elapsed time for objects to cross the distance.
        - final_speed (dict): Dictionary to store the final calculated speed for each object.

        Methods:
        - __init__(self, line1, line2, meter): Initializes the SpeedCheck instance with line equations and dictionaries.
        - check(self, id_number, cx, cy): Checks if an object with a given ID has crossed the lines and updates
                                         the timing and speed calculations accordingly.
        """
    def __init__(self, line1, line2, meter):
        """
            Initializes the SpeedCheck instance with line equations and dictionaries.

            Args:
                - line1 (tuple): Tuple containing two points defining the first line.
                - line2 (tuple): Tuple containing two points defining the second line.
                - meter (float): The meter value representing the distance between the two lines.
        """
        self.meter = meter
        # Calculate the equations of the lines (y = mx + n) for crossing events
        self.m1 = (line1[1][1] - line1[0][1]) / (line1[1][0] - line1[0][0])
        self.n1 = line1[0][1] - self.m1 * line1[0][0]
        self.m2 = (line2[1][1] - line2[0][1]) / (line2[1][0] - line2[0][0])
        self.n2 = line2[0][1] - self.m2 * line2[0][0]

        # Start a new dictionary for time calculation
        self.start_time = {}
        self.elapsed_time = {}
        self.final_speed = {}

    def check(self, id_number, cx, cy):
        """
            Checks if an object with a given ID has crossed the lines and updates timing and speed calculations.

            Args:
                - id_number (int): The unique identifier of the object.
                - cx (int): x-coordinate of the center point of the object.
                - cy (int): y-coordinate of the center point of the object.
        """
        # Calculate the distance from the center point to each line
        d1 = abs((self.m1 * cx - cy + self.n1) / math.sqrt(self.m1 * self.m1 + 1))
        d2 = abs((self.m2 * cx - cy + self.n2) / math.sqrt(self.m2 * self.m2 + 1))

        if d1 < 10:
            if id_number not in self.start_time:
                self.start_time[id_number] = (time.perf_counter(), d1, False)
            elif not self.start_time[id_number][2] and self.start_time[id_number][1] >= d1:
                self.start_time[id_number] = (time.perf_counter(), d1, False)
            elif self.start_time[id_number][2]:
                if self.start_time[id_number][1] >= d1 or not self.start_time[id_number][1]:
                    self.elapsed_time[id_number] = time.perf_counter() - self.start_time[id_number][0]
                    self.final_speed[id_number] = int(3.6 * self.meter / self.elapsed_time[id_number])
                    self.start_time[id_number] = (self.start_time[id_number][0], d1, self.start_time[id_number][2])
        if d2 < 10:
            if id_number not in self.start_time:
                self.start_time[id_number] = (time.perf_counter(), False, d2)
            elif not self.start_time[id_number][1] and self.start_time[id_number][2] >= d2:
                self.start_time[id_number] = (time.perf_counter(), False, d2)
            elif self.start_time[id_number][1]:
                if self.start_time[id_number][2] >= d2 or not self.start_time[id_number][2]:
                    self.elapsed_time[id_number] = time.perf_counter() - self.start_time[id_number][0]
                    self.final_speed[id_number] = int(3.6 * self.meter / self.elapsed_time[id_number])
                    self.start_time[id_number] = (self.start_time[id_number][0], self.start_time[id_number][1], d2)
