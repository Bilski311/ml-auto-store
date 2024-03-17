import os
import csv
import math

from utils.utils import clear_directory, copy_files

if __name__ == '__main__':
    tmp_directory = "../detected_barcodes/tmp"
    img_directory = "../detected_barcodes/img"
    annotations_directory = "../detected_barcodes/annotation"
    clear_directory(img_directory)
    clear_directory(annotations_directory)
    copy_files(tmp_directory, img_directory)

    annotations_file = os.path.join(annotations_directory, "annotations.csv")
    os.makedirs(annotations_directory, exist_ok=True)
    img_filenames = [f for f in os.listdir(img_directory) if
                     os.path.isfile(os.path.join(img_directory, f)) and not f.startswith('.')]
    dataset_size = len(img_filenames)
    number_of_images_in_group = math.ceil(dataset_size / 4)
    with open(annotations_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["image_path", "label"])

        for i, filename in enumerate(sorted(img_filenames)):
            if i < number_of_images_in_group:
                label = 0
            elif i < 2 * number_of_images_in_group:
                label = 1
            elif i < 3 * number_of_images_in_group:
                label = 2
            else:
                label = 3
            writer.writerow([filename, label])

    print(f"Annotations CSV file has been created at {annotations_file}")