import cv2
import os

from bounding_box import BoundingBox
from coordinate import Coordinate


def parse_annotation_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        annotations = [list(map(float, line.split())) for line in lines]
    return annotations


def rotate_annotation_90_left(bounding_box, image_width):
    new_top_left_x = bounding_box.top_left_corner.y
    new_top_left_y = image_width - bounding_box.top_left_corner.x - bounding_box.width
    new_top_left = Coordinate(new_top_left_x, new_top_left_y)
    new_bottom_right_x = bounding_box.bottom_right_corner.y
    new_bottom_right_y = image_width - bounding_box.bottom_right_corner.x + bounding_box.width
    new_bottom_right = Coordinate(new_bottom_right_x, new_bottom_right_y)
    new_bounding_box = BoundingBox.from_corners(new_top_left, new_bottom_right)

    return new_bounding_box


def show_image_with_annotation(name, _class, frame, bounding_box):
    display_frame = frame.copy()
    cv2.rectangle(display_frame,
                  (bounding_box.top_left_corner.x, bounding_box.top_left_corner.y),
                  (bounding_box.bottom_right_corner.x, bounding_box.bottom_right_corner.y),
                  (255, 0, 0), 2)
    cv2.putText(display_frame, str(_class), (bounding_box.top_left_corner.x, bounding_box.top_left_corner.y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow(name, display_frame)
    return cv2.waitKey(0)


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