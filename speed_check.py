import math
import time


class speed_check:
    def __init__(self, line1, line2, meter):
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
