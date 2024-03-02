import cv2
import os

from bounding_box import BoundingBox
from coordinate import Coordinate


def parse_annotation_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        annotations = [list(map(float, line.split())) for line in lines]
    return annotations


def rotate_annotation_90_left(bounding_box, image_width, image_height):
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


def show_dataset(image_files):
    for image_file in image_files:
        file_name = os.path.splitext(image_file)[0]
        image_path = os.path.join("../dataset" + "/images/" + image_file)
        annotation_path = os.path.join("../dataset" + "/labels/" + file_name + ".txt")
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
        number_of_rotations = 0
        new_bounding_box = bounding_box
        new_frame = frame
        if key == 49:
            print("Rotate left once")
            number_of_rotations += 1
        elif key == 50:
            print("Rotate left twice")
            number_of_rotations += 2
        elif key == 51:
            print("Rotate left thrice")
            number_of_rotations += 3
        elif key == 113:
            print("Do not rotate left")
        if key == 27:
            break
        for _ in range(number_of_rotations):
            new_bounding_box = rotate_annotation_90_left(new_bounding_box, new_frame.shape[1], new_frame.shape[0])
            new_frame = cv2.rotate(new_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        show_image_with_annotation("Rotated", _class, new_frame, new_bounding_box)
        cv2.imwrite("./new_dataset/images/" + file_name + ".jpg", new_frame)
        x_center_norm, y_center_norm, width_norm, height_norm = new_bounding_box.normalize(new_frame.shape[1], new_frame.shape[0])
        with open("new_dataset/labels/" + file_name + ".txt", 'w') as file:
            file.write(f"{_class} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n")

image_files = sorted([f for f in os.listdir("../dataset/images") if f.endswith('.jpg')])
show_dataset(image_files)