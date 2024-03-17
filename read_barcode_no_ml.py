import os

import cv2
from ultralytics import YOLO
from PIL import Image
import zbarlight

def read_barcode(index, image):
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    image_pil = image_pil.convert('L')
    codes = zbarlight.scan_codes(['ean13', 'code128'], image_pil)
    if codes:
        print(f"Detected Barcodes in image {index}: {codes}")
        return True
    print(f'Failed to detect barcode for image: {index}')
    return False


# Load a model
correct = 0
# image_directory = 'data_preprocessing/augmented_data/images'
image_directory = 'data_preprocessing/manually_rotated_images/images'
for index, image_name in enumerate(sorted(os.listdir(image_directory))):
    image = cv2.imread(f'{image_directory}/{image_name}')
    correct += read_barcode(index, image)
print(f'Accuracy :{correct/len(os.listdir(image_directory))}')