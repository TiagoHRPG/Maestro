import mediapipe as mp
import math
import time

class GestureRecognizer:
    def __init__(self):
        self.hold_time = 0.5
        self.start_time = None

        self.current_gesture = None
        
        self.process_gesture = None

    def detect_gesture(self, hand_detector):
        if self.is_pause_gesture(hand_detector):
            return "pause"
        
        elif self.is_play_gesture(hand_detector):
            return "play"
        
        elif self.is_previous_gesture(hand_detector):
            return "previous"
        
        elif self.is_next_gesture(hand_detector):
            return "next"

        else:
            return None

    
    def recognize(self, hand_detector):
        if self.process_gesture is None:
            self.process_gesture = self.detect_gesture(hand_detector)
            self.start_time = time.time()

        else:
            if (time.time() - self.start_time) > self.hold_time:
                temp = self.process_gesture
                self.process_gesture = None
                return temp
            else:
                if self.process_gesture != self.detect_gesture(hand_detector):
                    self.process_gesture = None
                return None
        
    def is_next_gesture(self, hand_detector):
        return self.check_peace_gesture(hand_detector) == ["Right"]
    
    def is_previous_gesture(self, hand_detector):
        return self.check_peace_gesture(hand_detector) == ["Left"]
        
    def is_play_gesture(self, hand_detector):
        return self.check_open_palm(hand_detector) == ["Right"]

    def is_pause_gesture(self, hand_detector):
        return self.check_open_palm(hand_detector) == ["Left"]


    def check_peace_gesture(self, hand_detector):
        result = hand_detector.result

        mp_hands = mp.solutions.hands

        peace_gesture = []
        for i, hand in enumerate(result.hand_landmarks):
            fingertips_enum = [mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]
            
            fingers_up = 0
            for finger_tip in fingertips_enum:
                if finger_tip == mp_hands.HandLandmark.THUMB_TIP:
                    #ignore thumb
                    continue
                if hand[finger_tip].y < hand[finger_tip-2].y:
                    fingers_up += 1
            if fingers_up == 2:
                peace_gesture.append(result.handedness[i][0].category_name)

        print(peace_gesture)
        return peace_gesture

    def check_open_palm(self, hand_detector):
        result = hand_detector.result
        bboxes = hand_detector.bboxes

        mp_hands = mp.solutions.hands

        open_palms = []
        for i, hand in enumerate(result.hand_landmarks):
            

            fingertips_enum = [mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]

            fingertips_list = [hand[i] for i in fingertips_enum]
            
            bbox_width = bboxes[i][2] - bboxes[i][0]
            if self.is_every_element_far(fingertips_list, bbox_width*0.27):
                open_palms.append(result.handedness[i][0].category_name)
        
        print(open_palms)
        return open_palms
    
    def is_every_element_far(self, elements, threshold):
        for i in range(len(elements)):
            for j in range(len(elements)):
                if i != j:
                    if self.get_euclidian_distance(elements[i], elements[j]) < threshold:
                        return False
                    
        return True
        
    def get_euclidian_distance(self, point1, point2):
        return math.sqrt((point1.x-point2.x)**2 + (point1.y-point2.y)**2)