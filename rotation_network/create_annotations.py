import os
import csv

if __name__ == '__main__':
    img_directory = "../detected_barcodes/img"
    annotations_directory = "../detected_barcodes/annotation"
    annotations_file = os.path.join(annotations_directory, "annotations.csv")
    os.makedirs(annotations_directory, exist_ok=True)
    img_filenames = [f for f in os.listdir(img_directory) if
                     os.path.isfile(os.path.join(img_directory, f)) and not f.startswith('.')]
    with open(annotations_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["image_path", "label"])

        for i, filename in enumerate(sorted(img_filenames)):
            label = i % 4
            writer.writerow([filename, label])

    print(f"Annotations CSV file has been created at {annotations_file}")