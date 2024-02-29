import os
from PIL import Image
import zbarlight

def detect_barcode_in_image(image_path):
    """Detects barcodes in a given image using zbarlight and returns the decoded information."""
    with Image.open(image_path) as img:
        # Convert the image to grayscale as required by zbarlight
        img = img.convert('L')

        # Scan the image for barcodes
        codes = zbarlight.scan_codes(['ean13', 'code128'], img)  # Add or remove barcode types as needed

        if codes:
            for code in codes:
                print(f"Detected Barcode: {code.decode('utf-8')}, in Image: {image_path}")
                return True
        else:
            print(f"No Barcodes Detected in Image: {image_path}")
            return False


def scan_directory_for_jpgs(directory_path):
    sorted_files = sorted(os.listdir(directory_path))
    total = len(sorted_files)
    detected_barcodes = 0
    undetected_barcodes = 0
    for filename in sorted_files:
        if filename.endswith(".jpg"):
            image_path = os.path.join(directory_path, filename)
            is_barcode_detected = detect_barcode_in_image(image_path)
            if is_barcode_detected:
                detected_barcodes += 1
            else:
                undetected_barcodes += 1

    print(f"Total Barcodes: {total}")
    print(f"Found {detected_barcodes}")
    print(f"Not found {undetected_barcodes}")
    print(f"Recall: {detected_barcodes / total}")


if __name__ == "__main__":
    directory_path = 'dataset/images'
    scan_directory_for_jpgs(directory_path)
