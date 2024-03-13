import os


def create_directories(destination_directories):
    for directory in destination_directories.values():
        os.makedirs(directory, exist_ok=True)
        print(f"Directory '{directory}' is created or already exists.")

def create_rotated_copies(image_files):
    for image_index, image_file in enumerate(image_files):
        print(image_file)


destination_directories = {
    'image': 'augmented_data/images',
    'labels': 'augmented_data/labels'
}

if __name__ == "__main__":
    create_directories(destination_directories)
    image_files = sorted([f for f in os.listdir("manually_rotated_images/images") if f.endswith('.jpg')])
    create_rotated_copies(image_files)