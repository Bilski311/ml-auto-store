import cv2

from coordinate import Coordinate
from bounding_box import BoundingBox


def rotate_image(number_of_rotations, bounding_box, frame, _class):
    new_bounding_box = bounding_box
    new_frame = frame
    for _ in range(number_of_rotations):
        new_bounding_box = rotate_annotation_90_left(new_bounding_box, new_frame.shape[1])
        new_frame = cv2.rotate(new_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    return new_frame, new_bounding_box


def rotate_annotation_90_left(bounding_box, image_width):
    new_top_left_x = bounding_box.top_left_corner.y
    new_top_left_y = image_width - bounding_box.top_left_corner.x - bounding_box.width
    new_top_left = Coordinate(new_top_left_x, new_top_left_y)
    new_bottom_right_x = bounding_box.bottom_right_corner.y
    new_bottom_right_y = image_width - bounding_box.bottom_right_corner.x + bounding_box.width
    new_bottom_right = Coordinate(new_bottom_right_x, new_bottom_right_y)
    new_bounding_box = BoundingBox.from_corners(new_top_left, new_bottom_right)

    return new_bounding_box
