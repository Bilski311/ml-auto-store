import torch
import numpy as np
from torchvision import transforms
def transform_image(image):
    torch_transforms = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
    ])

    return torch_transforms(image)


def transform_target_barcode(barcode):
    barcode = str(barcode)
    if len(barcode) != 13:
        raise ValueError('Wrong length of barcode')
    return torch.tensor([int(digit) for digit in barcode])
