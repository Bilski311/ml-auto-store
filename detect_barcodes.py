import cv2
import numpy as np
from ultralytics import YOLO
import os



def detect_barcode(path, model, fileNumber):
    image = cv2.imread(path)
    detection_result = model(image)[0]
    bounding_boxes = detection_result.boxes
    bounding_box_frames = np.array(bounding_boxes.xyxy.cpu(), dtype="int")
    classes = np.array(bounding_boxes.cls.cpu(), dtype="int")
    confidences = np.array(bounding_boxes.conf.cpu().numpy())

    max_confidence = 0
    best_bbox = None
    best_index = None

    for index, (_class, bounding_box, confidence) in enumerate(zip(classes, bounding_box_frames, confidences)):
        if confidence > max_confidence:
            max_confidence = confidence
            best_bbox = bounding_box
            best_index = index

    if best_bbox is not None:
        x, y, x2, y2 = best_bbox
        cropped_image = image[y:y2, x:x2]
        output_filename = f"detected_barcodes/tmp/DetectedBarcode_{fileNumber:03}_confidence_{max_confidence:.2f}_{best_index}.jpg"
        cv2.imwrite(output_filename, cropped_image)
        print(f"Saved: {output_filename}")

def scan_directory_for_jpgs(directory_path, model):
    sorted_files = sorted(os.listdir(directory_path))
    for index, filename in enumerate(sorted_files):
        if filename.endswith(".jpg"):
            image_path = os.path.join(directory_path, filename)
            detect_barcode(image_path, model, index)


# Load a model
model = YOLO("/Users/dominik.bilski/ml-auto-store/runs/detect/train3/weights/best.pt")  # load a pretrained model (recommended for training)
directory_path = 'dataset/images'
scan_directory_for_jpgs(directory_path, model)
cv2.destroyAllWindows()