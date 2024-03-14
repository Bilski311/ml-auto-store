import os

import cv2


def save_image(file_name, frame, bounding_box, _class, destination_paths):
    image_path = os.path.join(destination_paths['image'], file_name + ".jpg")
    annotation_path = os.path.join(destination_paths['annotation'], file_name + ".txt")
    cv2.imwrite(image_path, frame)
    x_center_norm, y_center_norm, width_norm, height_norm = bounding_box.normalize(frame.shape[1],
                                                                                       frame.shape[0])
    with open(annotation_path, 'w') as file:
        file.write(f"{_class} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n")