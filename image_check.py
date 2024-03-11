import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import zbarlight

def read_barcode(index, image):
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    image_pil = image_pil.convert('L')
    codes = zbarlight.scan_codes(['ean13', 'code128'], image_pil)
    if codes:
        print(f"Detected Barcodes in image {index}: {codes}")

def show_dataset(path, model):
    image = cv2.imread(path)
    detection_result = model(image)[0]
    bounding_boxes = detection_result.boxes
    bounding_box_frames = np.array(bounding_boxes.xyxy.cpu(), dtype="int")
    classes = np.array(bounding_boxes.cls.cpu(), dtype="int")
    confidences = np.array(bounding_boxes.conf.cpu().numpy())
    for index, (_class, bounding_box, confidence) in enumerate(zip(classes, bounding_box_frames, confidences)):
        x, y, x2, y2 = bounding_box
        cropped_image = image[y:y2, x:x2]
        read_barcode(index, cropped_image)
        read_barcode(index, image)
        output_filename = f"output_class_{_class}_confidence_{confidence:.2f}_{index}.jpg"
        cv2.imwrite(output_filename, cropped_image)
        print(f"Saved: {output_filename}")
        cv2.rectangle(image, (x, y), (x2, y2), (255, 0, 0), 2)
        cv2.putText(image, str(_class), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(image, str(confidence), (x, y2 - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("frame", image)
    cv2.waitKey(0)

# Load a model
model = YOLO("/Users/dominik.bilski/ml-auto-store/runs/detect/train14/weights/best.pt")  # load a pretrained model (recommended for training)
show_dataset("test_image5.jpg", model)
cv2.destroyAllWindows()