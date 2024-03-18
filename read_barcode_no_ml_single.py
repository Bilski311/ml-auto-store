from pyzbar.pyzbar import decode
from PIL import Image

def read_barcode(image):
    decoded_objects = decode(image)
    print(decoded_objects)
    if decoded_objects:
        return True
    else:
        return False



cropped_images_directory = 'dataset/images_cropped_to_barcodes'
raw_images_directory = 'dataset/images_before_processing'



image = Image.open(f'test_image5.jpg')
read_barcode(image)
