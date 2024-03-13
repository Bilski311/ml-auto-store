import cv2
import os

from bounding_box import BoundingBox
from annotations import parse_annotation_file
from image_display import show_image_with_annotation


def show_dataset(image_files, main_directory):
    for image_file in image_files:
        file_name = os.path.splitext(image_file)[0]
        image_path = os.path.join(main_directory + "/images/" + image_file)
        annotation_path = os.path.join(main_directory + "/labels/" + file_name + ".txt")
        annotations = parse_annotation_file(annotation_path)
        frame = cv2.imread(image_path)

        if frame is None:
            continue
        annotation = annotations[0]
        _class, x_center, y_center, width, height = annotation
        # Convert normalized coordinates to pixel coordinates
        x_center *= frame.shape[1]
        y_center *= frame.shape[0]
        width *= frame.shape[1]
        height *= frame.shape[0]

        # Calculate the bounding box's top-left and bottom-right coordinates
        bounding_box = BoundingBox(x_center, y_center, width, height)

        # Draw the bounding box and class label on the image
        key = show_image_with_annotation("Original frame", _class, frame, bounding_box)
        if key == 27:
            break

main_directory = "new_dataset"
image_files = sorted([f for f in os.listdir(main_directory + "/images") if f.endswith('.jpg')])
show_dataset(image_files, main_directory)