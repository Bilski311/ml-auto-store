import os

from pyzbar.pyzbar import decode
from PIL import Image

def read_barcode(image):
    decoded_objects = decode(image)
    print(decoded_objects)
    if decoded_objects:
        return True
    else:
        return False

def measure_accuracy(source_directory):
    correct = 0
    sorted_filenames = sorted(os.listdir(source_directory))
    # Load the image
    for image in sorted_filenames:
        image = Image.open(f'{source_directory}/{image}')
        correct += read_barcode(image)

    print(f'{correct / len(sorted_filenames)}')


cropped_images_directory = 'dataset/images_cropped_to_barcodes'
raw_images_directory = 'dataset/images_before_processing'

measure_accuracy(cropped_images_directory)
measure_accuracy(raw_images_directory)
