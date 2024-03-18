import numpy as np
from torchvision import transforms
def transform_image(image):
    torch_transforms = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
    ])

    return torch_transforms(image)


def transform_barcode_to_one_hot(barcode):
    barcode = str(barcode)
    digits = [int(digit) for digit in barcode]
    one_hot_digits = [digit_to_one_hot(digit) for digit in digits]

    return one_hot_digits

def digit_to_one_hot(digit):
    zeros = np.zeros(10)
    zeros[digit] = 1

    return zeros