import math


class Tracker:
    def __init__(self):
        # Store the center positions of the objects and the width and height
        self.center_points = {}
        # Keep the count of the IDs - each time a new object id_num detected, the count will increase
        self.id_count = 0
        # every 10 frames clean old id_num's
        self.num_of_frames = 0
        self.new_center_points = {}

    def update(self, objects_rect):
        # Object boxes and ids
        objects_bbs_ids = []

        # Get center point of an object
        for rect in objects_rect:
            x, y, new_w, new_h = rect
            new_cx = (x + x + new_w) // 2
            new_cy = (y + y + new_h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for prev_id, prev_points in self.center_points.items():
                prev_cx, prev_cy, prev_w, prev_h = prev_points
                dist = math.hypot(new_cx - prev_cx, new_cy - prev_cy)

                if dist < 70 and (7 / 8) * prev_w / prev_h < new_w / new_h < (9 / 8) * prev_w / prev_h:
                    self.center_points[prev_id] = (new_cx, new_cy, new_w, new_h)
                    objects_bbs_ids.append([x, y, new_w, new_h, prev_id])
                    same_object_detected = True
                    break

            # New object is detected, so we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (new_cx, new_cy, new_w, new_h)
                objects_bbs_ids.append([x, y, new_w, new_h, self.id_count])
                self.id_count += 1

        # Save the objects into the new dictionary
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            self.new_center_points[object_id] = center

        self.num_of_frames += 1
        if self.num_of_frames % 100 == 0:
            # Clean the dictionary by center points to remove IDS not used anymore
            self.new_center_points = {}

            # Update dictionary with IDs not used removed
            self.center_points = self.new_center_points.copy()
            self.num_of_frames = 0

        return objects_bbs_ids
