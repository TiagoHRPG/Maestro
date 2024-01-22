import Maestro.handDetector as hd
import cv2
import Maestro.utils as utils
import Maestro.gestureRecognizer
import Maestro.controller 

import mediapipe as mp

def put_gesture_text(image, gesture):
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    fontScale              = 0.7

    cv2.putText(image,f'hand gesture: {gesture}', 
        (10, 30), 
        font, 
        fontScale,
        (255,255,255),
        2,
        2)
    return image


handDetector = Maestro.handDetector.HandDetector()
gestureRecognizer = Maestro.gestureRecognizer.GestureRecognizer()
controller = Maestro.controller.Controller()


# The landmarker is initialized. Use it here.
capture = cv2.VideoCapture(0)

while capture.isOpened():
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    
    handDetector.detect_async(mp_image)

    if handDetector.result is not None:
        annotated_image = utils.draw_landmarks_on_image(frame, handDetector.result)
        
        gesture = gestureRecognizer.recognize(handDetector)

        put_gesture_text(annotated_image, gesture)
        if gesture == "pause":
            controller.pause()
        elif gesture == "play":
            controller.play()
        elif gesture == "next":
            controller.next()
        elif gesture == "previous":
            controller.previous()

        cv2.imshow('Frame', annotated_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        

capture.release()
cv2.destroyAllWindows()
