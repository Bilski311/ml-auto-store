import os

import cv2
from ultralytics import YOLO
from PIL import Image
import zbarlight

def read_barcode(index, image):
    bd = cv2.barcode.BarcodeDetector()
    retval, _, _ = bd.detectAndDecode(image)
    if retval:
        return True
    else:
        return False


# Load a model
correct = 0
# image_directory = 'data_preprocessing/augmented_data/images'
# image_directory = 'data_preprocessing/manually_rotated_images/images'
# image_directory = 'dataset/images_before_processing'
# image_directory = 'dataset/images'
image_directory = 'dataset/images_cropped_to_barcodes'
for index, image_name in enumerate(sorted(os.listdir(image_directory))):
    image = cv2.imread(f'{image_directory}/{image_name}')
    correct += read_barcode(index, image)
print(f'Accuracy :{correct/len(os.listdir(image_directory))}')