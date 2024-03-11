from torchvision import transforms
def transform_image(image):
    torch_transforms = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
    ])

    return torch_transforms(image)