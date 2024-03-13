from coordinate import Coordinate
from bounding_box import BoundingBox


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