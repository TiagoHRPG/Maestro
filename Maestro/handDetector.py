import mediapipe as mp
import time
from Maestro.utils import normalized_to_pixel_coordinates
import math

class HandDetector():
    def __init__(self):        
        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path='Maestro/models/hand_landmarker.task'),
            running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
            result_callback=self.update_result,
            num_hands=2)
        
        self.landmarker = mp.tasks.vision.HandLandmarker.create_from_options(options) 

        self.bboxes = []

        self.result = None

    def detect_async(self, mp_image):
        timestamp = int(round(time.time() * 1000))
        self.landmarker.detect_async(mp_image, timestamp)


    # Create a hand landmarker instance with the live stream mode:
    def update_result(self, result, output_image: mp.Image, timestamp_ms: int):
        self.result = result

        self.update_bboxes()


    def update_bboxes(self):
        bboxes = []
        
        for hand in self.result.hand_landmarks:
            xmin = math.inf
            ymin = math.inf
            xmax = 0
            ymax = 0
            for point in hand:
                if point.x < xmin:
                    xmin = point.x
                if point.x > xmax:
                    xmax = point.x
                if point.y < ymin:
                    ymin = point.y
                if point.y > ymax:
                    ymax = point.y

            bboxes.append((xmin, ymin, xmax, ymax))
        
        self.bboxes = bboxes

