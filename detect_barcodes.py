import cv2
import numpy as np
from ultralytics import YOLO
import os

from utils.utils import clear_directory


def detect_barcode(path, model, fileNumber, output_directory):
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
        output_filename = f"{output_directory}/DetectedBarcode_{fileNumber:04}_confidence_{max_confidence:.2f}_{best_index}.jpg"
        cv2.imwrite(output_filename, cropped_image)
        print(f"Saved: {output_filename}")

def scan_directory_for_jpgs(directory_path, model, output_directory):
    sorted_files = sorted(os.listdir(directory_path))
    for index, filename in enumerate(sorted_files):
        if filename.endswith(".jpg"):
            image_path = os.path.join(directory_path, filename)
            detect_barcode(image_path, model, index, output_directory)


def check_and_fix_missing_files(directory, total_files):
    for file_number in range(total_files):
        expected_filename = f"DetectedBarcode_{file_number:03}_"
        matching_files = [filename for filename in os.listdir(directory) if filename.startswith(expected_filename)]

        if len(matching_files) == 0:
            prev_file_number = file_number - 1
            prev_file_pattern = f"DetectedBarcode_{prev_file_number:03}_"
            prev_files = [filename for filename in os.listdir(directory) if filename.startswith(prev_file_pattern)]

            if prev_files:
                prev_file_to_use = sorted(prev_files)[-1]
                prev_image_path = os.path.join(directory, prev_file_to_use)
                image = cv2.imread(prev_image_path)

                rotated_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

                missing_file_name = f"DetectedBarcode_{file_number:03}_confidence_.jpg"
                missing_file_path = os.path.join(directory, missing_file_name)
                cv2.imwrite(missing_file_path, rotated_image)
                print(f"Created missing file by rotating previous image: {missing_file_name}")


# Load a model
model = YOLO("/Users/dominik.bilski/ml-auto-store/runs/detect/train22/weights/best.pt")  # load a pretrained model (recommended for training)
# directory_path = 'dataset/images'
# output_directory = 'detected_barcodes/img'
# directory_path = 'dataset/validation/images'
# output_directory = 'rotation_network/validation/images'
output_directory = 'dataset/images_cropped_to_barcodes'
directory_path = 'data_preprocessing/manually_rotated_images/images'
clear_directory(output_directory)
scan_directory_for_jpgs(directory_path, model, output_directory)
total_files = len([name for name in os.listdir(directory_path) if name.endswith('.jpg')])
check_and_fix_missing_files(output_directory, total_files)
cv2.destroyAllWindows()