import cv2
import sys

cascPath = './cascades/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)


def IsFaceDetected(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    return True if len(faces) > 0 else False
