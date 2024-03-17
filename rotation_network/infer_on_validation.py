import os

import torch
from PIL import Image

from infer import infer_from_image


model = torch.load('model.pth')
for image_name in sorted(os.listdir('validation/images')):
    image = Image.open(f'validation/images/{image_name}')
    infer_from_image(image, image_name, model)
