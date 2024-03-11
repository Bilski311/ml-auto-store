import torch
from PIL import Image

from transforms import transform_image

def infer_from_image(image, model):
    transformed_image = transform_image(image).to('mps')
    prediction = model(transformed_image)
    print(prediction)
    print(prediction.argmax(1).item())


model = torch.load('model.pth')
image1 = Image.open('img.png')
image2 = Image.open('img2.jpg')

infer_from_image(image1, model)
infer_from_image(image2, model)