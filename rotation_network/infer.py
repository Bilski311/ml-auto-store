from transforms import transform_image

def infer_from_image(image, image_name, model):
    transformed_image = transform_image(image).to('mps')
    prediction = model(transformed_image)

    print(f'Image: {image_name}\n'
          f'Prediction: {prediction.argmax(1).item()}')
