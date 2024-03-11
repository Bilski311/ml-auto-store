from torchvision import transforms
from PIL import Image
def transform_image(image):
    torch_transforms = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),  # Convert to grayscale
        transforms.Resize((256, 256)),  # Resize to 256x256 Convert to tensor
    ])

    return torch_transforms(image)