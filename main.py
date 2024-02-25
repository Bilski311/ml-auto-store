import cv2
import numpy as np
import torch
from ultralytics import YOLO

print(torch.backends.mps.is_available())
video_capture = cv2.VideoCapture("dogs.mp4")
model = YOLO("yolov8m.pt")

while True:
    next_frame_exists, frame = video_capture.read()
    if not next_frame_exists:
        break
    detection_result = model(frame)[0]
    bounding_boxes = detection_result.boxes
    bounding_box_frames = np.array(bounding_boxes.xyxy.cpu(), dtype="int")
    classes = np.array(bounding_boxes.cls.cpu(), dtype="int")
    print(bounding_box_frames)
    print(classes)
    for _class, bounding_box in zip(classes, bounding_box_frames):
        x, y, x2, y2 = bounding_box
        cv2.rectangle(frame, (x, y), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, str(_class), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

video_capture.release()
cv2.destroyAllWindows()