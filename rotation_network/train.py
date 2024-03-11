from torchvision.transforms import ToTensor

from rotation_dataset import RotationDataset
from transforms import transform_image
import matplotlib.pyplot as plt


if __name__ == '__main__':
    dataset = RotationDataset(
        annotations_file='../detected_barcodes/annotation/annotations.csv',
        img_dir='../detected_barcodes/img',
        transform=transform_image
    )


