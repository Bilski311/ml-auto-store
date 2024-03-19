import os

import torch

from PIL import Image
from transforms import transform_image
from neural_network import BarcodeDecoderNeuralNetwork


def infer_from_image(image, image_name, model):
    transformed_image = transform_image(image).unsqueeze(0).to('mps')
    prediction = model(transformed_image)

    print(f'Image: {image_name}\n'
          f'Prediction: {prediction.argmax(2).tolist()}')


if __name__ == '__main__':
    model = BarcodeDecoderNeuralNetwork().to('mps')
    model.load_state_dict(torch.load('model_state_dict.pth'))
    for image_name in sorted(os.listdir('dataset/validation/images')):
        image = Image.open(f'dataset/validation/images/{image_name}')
        infer_from_image(image, image_name, model)