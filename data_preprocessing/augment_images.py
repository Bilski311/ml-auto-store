import os

import cv2

from annotations import parse_annotation_file
from bounding_box import BoundingBox
from image_rotation import rotate_image
from image_io import save_image


def create_directories(destination_directories):
    for directory in destination_directories.values():
        os.makedirs(directory, exist_ok=True)
        print(f"Directory '{directory}' is created or already exists.")


def calculate_file_number(image_index, number_of_rotations, length_of_dataset):
    image_index += 1
    offset = length_of_dataset * number_of_rotations

    return image_index + offset


def create_rotated_copies(image_files, source_paths, destination_paths):
    for image_index, image_file in enumerate(image_files):
        file_name = os.path.splitext(image_file)[0]
        image_path = os.path.join(source_paths['image'], image_file)
        annotation_path = os.path.join(source_paths['annotation'], file_name + ".txt")
        annotations = parse_annotation_file(annotation_path)
        _class, *normalized_coordinates = annotations[0]
        frame = cv2.imread(image_path)
        bounding_box = BoundingBox.from_normalized_coordinates(normalized_coordinates, frame)
        for number_of_rotations in range(0, 4):
            new_frame, new_bounding_box = rotate_image(number_of_rotations, bounding_box, frame, _class)
            file_number = calculate_file_number(image_index, number_of_rotations, len(image_files))
            save_image(f'ProductBarcode{file_number:04}', new_frame, new_bounding_box, _class, destination_paths)



destination_directories = {
    'image': 'augmented_data/images',
    'annotation': 'augmented_data/labels'
}

source_paths = {
    'image': 'manually_rotated_images/images',
    'annotation': 'manually_rotated_images/labels'
}

if __name__ == "__main__":
    create_directories(destination_directories)
    image_files = sorted([f for f in os.listdir("manually_rotated_images/images") if f.endswith('.jpg')])
    create_rotated_copies(image_files, source_paths, destination_directories)
