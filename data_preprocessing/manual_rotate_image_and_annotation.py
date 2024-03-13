import cv2
import os
import argparse

from bounding_box import BoundingBox
from annotations import parse_annotation_file, rotate_annotation_90_left


def show_image_with_annotation(name, _class, frame, bounding_box):
    display_frame = frame.copy()
    cv2.rectangle(display_frame,
                  (bounding_box.top_left_corner.x, bounding_box.top_left_corner.y),
                  (bounding_box.bottom_right_corner.x, bounding_box.bottom_right_corner.y),
                  (255, 0, 0), 2)
    cv2.putText(display_frame, str(_class), (bounding_box.top_left_corner.x, bounding_box.top_left_corner.y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow(name, display_frame)
    return cv2.waitKey(0)


def rotate_image(number_of_rotations, bounding_box, frame, _class):
    new_bounding_box = bounding_box
    new_frame = frame
    for _ in range(number_of_rotations):
        new_bounding_box = rotate_annotation_90_left(new_bounding_box, new_frame.shape[1])
        new_frame = cv2.rotate(new_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    return new_frame, new_bounding_box


def get_action_based_on_key(key):
    if key == 49:
        return 'ROTATE', 1
    elif key == 50:
        return 'ROTATE', 2
    elif key == 51:
        return 'ROTATE', 3
    elif key == 96:
        return 'ROTATE', 0
    elif key == 113:
        return 'GO_TO_IMAGE'
    elif key == 27:
        return 'EXIT_PROGRAM'


def save_image(file_name, frame, bounding_box, _class, destination_paths):
    cv2.imwrite(destination_paths['image'] + file_name + ".jpg", frame)
    x_center_norm, y_center_norm, width_norm, height_norm = bounding_box.normalize(frame.shape[1],
                                                                                       frame.shape[0])
    with open(destination_paths['annotation'] + file_name + ".txt", 'w') as file:
        file.write(f"{_class} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n")


def rotate_images(image_files, source_paths, destination_paths):
    print(image_files)
    file_index = 0
    while True:
        image_file = image_files[file_index]
        file_name = os.path.splitext(image_file)[0]
        image_path = os.path.join(source_paths['image'] + image_file)
        annotation_path = os.path.join(source_paths['annotation'] + file_name + ".txt")
        annotations = parse_annotation_file(annotation_path)
        frame = cv2.imread(image_path)

        if frame is None:
            continue
        _class, *normalized_coordinates = annotations[0]
        bounding_box = BoundingBox.from_normalized_coordinates(normalized_coordinates, frame)
        key = show_image_with_annotation(image_file, _class, frame, bounding_box)
        action = get_action_based_on_key(key)
        match action:
            case 'ROTATE', number_of_rotations:
                new_frame, new_bounding_box = rotate_image(number_of_rotations, bounding_box, frame, _class)
                key = show_image_with_annotation(image_file, _class, new_frame, new_bounding_box)
                if key == 13:
                    save_image(file_name, new_frame, new_bounding_box, _class, destination_paths)
                    file_index += 1
                    cv2.destroyAllWindows()
            case 'GO_TO_IMAGE':
                file_index = int(input('Enter image number: ')) - 1
                cv2.destroyAllWindows()
            case 'EXIT_PROGRAM':
                break


source_paths = {
    'image': '../dataset/images_before_processing/',
    'annotation': '../dataset/labels_before_processing/'
}

destination_paths = {
    'image': './manually_rotated_images/images/',
    'annotation': './manually_rotated_images/labels/'
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process images and annotations.')
    parser.add_argument('--overwrite', action='store_true',
                        help='Modify images and annotations in destination directory(default behaviour takes from source and saves to destination)')

    args = parser.parse_args()
    if args.overwrite:
        source_paths = destination_paths
    image_files = sorted([f for f in os.listdir("../dataset/images_before_processing") if f.endswith('.jpg')])
    rotate_images(image_files, source_paths, destination_paths)