import cv2
import numpy as np
import torch
from ultralytics import YOLO
from PIL import Image

from rotation_network.transforms import transform_image
from rotation_network.neural_network import NeuralNetwork

import zbarlight

def read_barcode(barcode):
    barcode_pil = Image.fromarray(cv2.cvtColor(barcode, cv2.COLOR_BGR2RGB))
    barcode_pil = barcode_pil.convert('L')
    codes = zbarlight.scan_codes(['ean13', 'code128'], barcode_pil)
    if codes:
        for code in codes:
            print(f"Detected Barcode: {code.decode('utf-8')}")



def detect_barcodes(path, model):
    image = cv2.imread(path)
    detection_result = model(image)[0]
    bounding_boxes = detection_result.boxes
    bounding_box_frames = [np.array(bounding_box.xyxy.cpu(), dtype="int") for bounding_box in bounding_boxes]
    barcodes = [image[y:y2, x:x2] for (x, y, x2, y2) in bounding_box_frames]

    return barcodes


def rotate_barcodes(model, barcodes):
    rotated_barcodes = []
    for barcode in barcodes:
        barcode_pil = Image.fromarray(cv2.cvtColor(barcode, cv2.COLOR_BGR2RGB))
        transformed_image = transform_image(barcode_pil).unsqueeze(0).to('mps')
        prediction = model(transformed_image)
        number_of_clockwise_rotations = prediction.argmax(1).item()
        for _ in range(number_of_clockwise_rotations):
            barcode = cv2.rotate(barcode, cv2.ROTATE_90_CLOCKWISE)
        rotated_barcodes.append(barcode)

    return rotated_barcodes


if __name__ == '__main__':
    detection_model = YOLO("/Users/dominik.bilski/ml-auto-store/runs/detect/train22/weights/best.pt")
    barcodes = detect_barcodes('test_image_multiple.jpg', detection_model)
    rotation_model = NeuralNetwork().to('mps')
    rotation_model.load_state_dict(torch.load('rotation_network/model_state_dict.pth'))
    rotation_model.eval()
    rotated_barcodes = rotate_barcodes(rotation_model, barcodes)

    for barcode in rotated_barcodes:
        read_barcode(barcode)
        cv2.imshow("frame", barcode)
        cv2.waitKey(0)