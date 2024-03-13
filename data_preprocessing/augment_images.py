import os


def create_directories():
    directories = ['augmented_data/images', 'augmented_data/labels']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory '{directory}' is created or already exists.")


if __name__ == "__main__":
    create_directories()
    image_files = sorted([f for f in os.listdir("manually_rotated_images/images") if f.endswith('.jpg')])
    create_rotated_copies(image_files)