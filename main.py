import cv2
import numpy as np
import torch
import os
from ultralytics import YOLO

def parse_annotation_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        annotations = [list(map(float, line.split())) for line in lines]  # Convert each line to a list of floats
    return annotations

print(torch.backends.mps.is_available())
image_files = [f for f in os.listdir("./dataset") if f.endswith('.jpg')]
model = YOLO("yolov8m.pt")

for image_file in image_files:
    image_path = os.path.join("./dataset", image_file)
    annotation_path = os.path.splitext(image_path)[0] + '.txt'
    annotations = parse_annotation_file(annotation_path)
    frame = cv2.imread(image_path)


    if frame is None:
        continue
    for annotation in annotations:
        _class, x_center, y_center, width, height = annotation
        # Convert normalized coordinates to pixel coordinates
        x_center *= frame.shape[1]
        y_center *= frame.shape[0]
        width *= frame.shape[1]
        height *= frame.shape[0]

        # Calculate the bounding box's top-left and bottom-right coordinates
        x = int(x_center - width / 2)
        y = int(y_center - height / 2)
        x2 = int(x_center + width / 2)
        y2 = int(y_center + height / 2)

        # Draw the bounding box and class label on the image
        cv2.rectangle(frame, (x, y), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, str(_class), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    detection_result = model(frame)[0]
    bounding_boxes = detection_result.boxes
    bounding_box_frames = np.array(bounding_boxes.xyxy.cpu(), dtype="int")
    classes = np.array(bounding_boxes.cls.cpu(), dtype="int")
    cv2.imshow("frame", frame)

    key = cv2.waitKey(0)
    if key == 27:
        break

cv2.destroyAllWindows()