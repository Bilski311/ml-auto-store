import os

from utils.utils import clear_directory
import cv2
import numpy as np


def apply_custom_distortions(image_path, image_number):
    img = cv2.imread(image_path)
    distortion_params = [(15, 2, False), (-15, 2, False), (15, 0.5, True), (-15, 0.5, True)]

    outputs = [apply_custom_distortion(amplitude, frequency, img, is_vertical) for (amplitude, frequency, is_vertical) in distortion_params]
    outputs = [*outputs, img]
    for index, output in enumerate(outputs):
        file_number = (image_number * len(outputs)) + index
        cv2.imwrite(f'dataset/tmp/image{file_number:05}.jpg', output)


def apply_custom_distortion(amplitude, frequency, img, is_vertical=False):
    rows, cols, _ = img.shape
    output = np.zeros(img.shape, dtype=img.dtype)
    for y in range(rows):
        for x in range(cols):
            new_x = distort_x(x, y, amplitude, frequency, rows, is_vertical)
            new_y = distort_y(x, y, amplitude, frequency, cols, is_vertical)
            if 0 <= new_x < cols and 0 <= new_y < rows:
                output[y, x] = img[new_y, new_x]
            else:
                output[y, x] = 255

    return output


def distort_x(x, y, amplitude, frequency, rows, is_vertical=False):
    if is_vertical:
        return x
    else:
        return x + int(amplitude * np.sin(2 * np.pi * y / (rows * frequency)))


def distort_y(x, y, amplitude, frequency, cols, is_vertical=False):
    if is_vertical:
        return y + int(amplitude * np.sin(2 * np.pi * x / (cols / frequency)))
    else:
        return y


if __name__ == '__main__':
    tmp_directory = "dataset/tmp"
    img_directory = "../detected_barcodes/img"
    clear_directory(tmp_directory)
    for index, file_name in enumerate(sorted(os.listdir(img_directory))):
        print(f'{index}: {file_name}')
        apply_custom_distortions(os.path.join(img_directory, file_name), index)